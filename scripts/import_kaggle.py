"""
Kaggle Dataset Import Script
=============================
Imports tracks from the Spotify dataset CSV into the database.

Dataset: https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks
Expected CSV columns: artists, name, release_date, danceability, energy, valence, tempo, popularity

Usage:
    pip install pandas
    python scripts/import_kaggle.py --file path/to/tracks.csv --limit 5000
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    import pandas as pd
except ImportError:
    print("Please install pandas: pip install pandas")
    sys.exit(1)

from app.core.database import SessionLocal, engine, Base
from app.models.models import Artist, Album, Track

Base.metadata.create_all(bind=engine)


def import_csv(filepath: str, limit: int = 5000):
    db = SessionLocal()

    print(f"📂 Loading CSV: {filepath}")
    df = pd.read_csv(filepath).head(limit)
    print(f"📊 Loaded {len(df)} rows")

    # Normalise column names
    df.columns = [c.lower().strip() for c in df.columns]

    # Extract release year
    if "release_date" in df.columns:
        df["year"] = pd.to_numeric(df["release_date"].str[:4], errors="coerce").fillna(0).astype(int)
    else:
        df["year"] = 0

    artist_cache = {}   # name -> Artist.id
    album_cache = {}    # (artist_id, year) -> Album.id
    imported = 0

    for _, row in df.iterrows():
        try:
            # ── Artist ────────────────────────────────────────────────────
            raw_artists = str(row.get("artists", row.get("artist_name", "Unknown")))
            # Handle list-like strings e.g. "['Artist A', 'Artist B']"
            artist_name = raw_artists.strip("[]'\"").split("','")[0].strip("'\"") if raw_artists.startswith("[") else raw_artists.strip()

            if artist_name not in artist_cache:
                artist = db.query(Artist).filter(Artist.name == artist_name).first()
                if not artist:
                    artist = Artist(name=artist_name, genre="Unknown", popularity=float(row.get("popularity", 0) or 0))
                    db.add(artist)
                    db.flush()
                artist_cache[artist_name] = artist.id

            artist_id = artist_cache[artist_name]
            year = int(row.get("year", 0))

            # ── Album ─────────────────────────────────────────────────────
            album_key = (artist_id, year)
            if album_key not in album_cache:
                album_title = f"{artist_name} – {year}" if year else f"{artist_name} – Singles"
                album = db.query(Album).filter(Album.title == album_title).first()
                if not album:
                    album = Album(title=album_title, release_year=year if year else None, artist_id=artist_id)
                    db.add(album)
                    db.flush()
                album_cache[album_key] = album.id

            album_id = album_cache[album_key]

            # ── Track ─────────────────────────────────────────────────────
            track_name = str(row.get("name", row.get("track_name", "Unknown Track")))
            duration = int(row.get("duration_ms", 0) or 0)

            track = Track(
                title=track_name,
                duration_ms=duration,
                album_id=album_id,
                danceability=float(row.get("danceability", 0.5) or 0.5),
                energy=float(row.get("energy", 0.5) or 0.5),
                valence=float(row.get("valence", 0.5) or 0.5),
                tempo=float(row.get("tempo", 120.0) or 120.0),
                popularity=float(row.get("popularity", 0) or 0),
            )
            db.add(track)
            imported += 1

            if imported % 500 == 0:
                db.commit()
                print(f"  ✅ {imported} tracks imported...")

        except Exception as e:
            print(f"  ⚠️  Skipped row: {e}")
            continue

    db.commit()
    print(f"\n🎵 Import complete: {imported} tracks from {len(artist_cache)} artists.")
    db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Import Spotify Kaggle dataset")
    parser.add_argument("--file", required=True, help="Path to the CSV file")
    parser.add_argument("--limit", type=int, default=5000, help="Max rows to import (default: 5000)")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    import_csv(args.file, args.limit)
