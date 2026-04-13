"""
Seed script: populates the database with sample music data.
Run with: python scripts/seed_data.py
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal, engine, Base
from app.models.models import Artist, Album, Track, Playlist

Base.metadata.create_all(bind=engine)

SAMPLE_DATA = [
    {
        "artist": {"name": "Radiohead", "genre": "Alternative Rock", "country": "UK", "followers": 7800000, "popularity": 82.0},
        "albums": [
            {
                "title": "OK Computer", "release_year": 1997, "total_tracks": 12,
                "tracks": [
                    {"title": "Airbag", "duration_ms": 294000, "danceability": 0.31, "energy": 0.62, "valence": 0.24, "tempo": 84.0, "popularity": 72.0},
                    {"title": "Paranoid Android", "duration_ms": 383000, "danceability": 0.28, "energy": 0.78, "valence": 0.19, "tempo": 83.0, "popularity": 82.0},
                    {"title": "Karma Police", "duration_ms": 262000, "danceability": 0.44, "energy": 0.45, "valence": 0.31, "tempo": 75.0, "popularity": 84.0},
                    {"title": "No Surprises", "duration_ms": 228000, "danceability": 0.52, "energy": 0.29, "valence": 0.55, "tempo": 75.0, "popularity": 80.0},
                ]
            },
            {
                "title": "Kid A", "release_year": 2000, "total_tracks": 10,
                "tracks": [
                    {"title": "Everything in Its Right Place", "duration_ms": 254000, "danceability": 0.40, "energy": 0.35, "valence": 0.16, "tempo": 72.0, "popularity": 74.0},
                    {"title": "How to Disappear Completely", "duration_ms": 357000, "danceability": 0.22, "energy": 0.18, "valence": 0.08, "tempo": 60.0, "popularity": 71.0},
                ]
            }
        ]
    },
    {
        "artist": {"name": "Daft Punk", "genre": "Electronic", "country": "France", "followers": 12500000, "popularity": 88.0},
        "albums": [
            {
                "title": "Random Access Memories", "release_year": 2013, "total_tracks": 13,
                "tracks": [
                    {"title": "Get Lucky", "duration_ms": 369000, "danceability": 0.85, "energy": 0.72, "valence": 0.96, "tempo": 116.0, "popularity": 91.0},
                    {"title": "Instant Crush", "duration_ms": 337000, "danceability": 0.60, "energy": 0.55, "valence": 0.40, "tempo": 107.0, "popularity": 80.0},
                    {"title": "Lose Yourself to Dance", "duration_ms": 354000, "danceability": 0.88, "energy": 0.66, "valence": 0.78, "tempo": 100.0, "popularity": 78.0},
                    {"title": "Within", "duration_ms": 230000, "danceability": 0.44, "energy": 0.28, "valence": 0.55, "tempo": 82.0, "popularity": 63.0},
                ]
            },
            {
                "title": "Discovery", "release_year": 2001, "total_tracks": 14,
                "tracks": [
                    {"title": "One More Time", "duration_ms": 320000, "danceability": 0.82, "energy": 0.78, "valence": 0.90, "tempo": 123.0, "popularity": 89.0},
                    {"title": "Harder Better Faster Stronger", "duration_ms": 224000, "danceability": 0.79, "energy": 0.88, "valence": 0.72, "tempo": 123.0, "popularity": 87.0},
                    {"title": "Digital Love", "duration_ms": 301000, "danceability": 0.76, "energy": 0.80, "valence": 0.88, "tempo": 124.0, "popularity": 85.0},
                ]
            }
        ]
    },
    {
        "artist": {"name": "Billie Eilish", "genre": "Indie Pop", "country": "USA", "followers": 31000000, "popularity": 92.0},
        "albums": [
            {
                "title": "When We All Fall Asleep, Where Do We Go?", "release_year": 2019, "total_tracks": 14,
                "tracks": [
                    {"title": "bad guy", "duration_ms": 194000, "danceability": 0.70, "energy": 0.43, "valence": 0.56, "tempo": 135.0, "popularity": 95.0},
                    {"title": "bury a friend", "duration_ms": 193000, "danceability": 0.60, "energy": 0.52, "valence": 0.11, "tempo": 137.0, "popularity": 82.0},
                    {"title": "when the party's over", "duration_ms": 196000, "danceability": 0.33, "energy": 0.19, "valence": 0.12, "tempo": 76.0, "popularity": 85.0},
                ]
            },
            {
                "title": "Happier Than Ever", "release_year": 2021, "total_tracks": 16,
                "tracks": [
                    {"title": "Happier Than Ever", "duration_ms": 295000, "danceability": 0.34, "energy": 0.37, "valence": 0.15, "tempo": 68.0, "popularity": 86.0},
                    {"title": "NDA", "duration_ms": 217000, "danceability": 0.55, "energy": 0.38, "valence": 0.28, "tempo": 74.0, "popularity": 77.0},
                ]
            }
        ]
    },
    {
        "artist": {"name": "Kendrick Lamar", "genre": "Hip-Hop", "country": "USA", "followers": 18000000, "popularity": 93.0},
        "albums": [
            {
                "title": "To Pimp a Butterfly", "release_year": 2015, "total_tracks": 16,
                "tracks": [
                    {"title": "Alright", "duration_ms": 219000, "danceability": 0.72, "energy": 0.55, "valence": 0.62, "tempo": 119.0, "popularity": 87.0},
                    {"title": "King Kunta", "duration_ms": 234000, "danceability": 0.78, "energy": 0.62, "valence": 0.57, "tempo": 97.0, "popularity": 84.0},
                    {"title": "These Walls", "duration_ms": 318000, "danceability": 0.65, "energy": 0.43, "valence": 0.41, "tempo": 86.0, "popularity": 76.0},
                ]
            },
            {
                "title": "DAMN.", "release_year": 2017, "total_tracks": 14,
                "tracks": [
                    {"title": "HUMBLE.", "duration_ms": 177000, "danceability": 0.90, "energy": 0.62, "valence": 0.42, "tempo": 150.0, "popularity": 91.0},
                    {"title": "DNA.", "duration_ms": 185000, "danceability": 0.77, "energy": 0.77, "valence": 0.46, "tempo": 142.0, "popularity": 86.0},
                    {"title": "LOVE.", "duration_ms": 213000, "danceability": 0.81, "energy": 0.50, "valence": 0.68, "tempo": 100.0, "popularity": 84.0},
                ]
            }
        ]
    },
    {
        "artist": {"name": "Fleetwood Mac", "genre": "Classic Rock", "country": "UK", "followers": 9200000, "popularity": 80.0},
        "albums": [
            {
                "title": "Rumours", "release_year": 1977, "total_tracks": 11,
                "tracks": [
                    {"title": "Go Your Own Way", "duration_ms": 218000, "danceability": 0.53, "energy": 0.72, "valence": 0.83, "tempo": 136.0, "popularity": 83.0},
                    {"title": "Dreams", "duration_ms": 257000, "danceability": 0.62, "energy": 0.52, "valence": 0.73, "tempo": 120.0, "popularity": 85.0},
                    {"title": "The Chain", "duration_ms": 271000, "danceability": 0.48, "energy": 0.68, "valence": 0.59, "tempo": 152.0, "popularity": 82.0},
                    {"title": "Gold Dust Woman", "duration_ms": 291000, "danceability": 0.36, "energy": 0.42, "valence": 0.22, "tempo": 77.0, "popularity": 72.0},
                ]
            }
        ]
    },
]


def seed():
    db = SessionLocal()
    try:
        # Check if already seeded
        if db.query(Artist).count() > 0:
            print("Database already has data. Skipping seed.")
            return

        for entry in SAMPLE_DATA:
            # Create artist
            artist = Artist(**entry["artist"])
            db.add(artist)
            db.flush()

            for album_data in entry["albums"]:
                tracks_data = album_data.pop("tracks")
                album = Album(**album_data, artist_id=artist.id)
                db.add(album)
                db.flush()

                for track_data in tracks_data:
                    track = Track(**track_data, album_id=album.id)
                    db.add(track)

        # Create a sample playlist
        playlist = Playlist(name="Best of All Time", description="Hand-picked classics across genres")
        db.add(playlist)
        db.flush()

        # Add some tracks to the playlist
        first_tracks = db.query(Track).limit(6).all()
        playlist.tracks.extend(first_tracks)

        db.commit()
        print(f"✅ Seeded {len(SAMPLE_DATA)} artists with albums and tracks.")
        print(f"✅ Created 1 sample playlist.")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
