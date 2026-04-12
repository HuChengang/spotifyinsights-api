from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Artist, Album, Track

router = APIRouter()


@router.get("/genre-trends", summary="Genre popularity trends")
def genre_trends(db: Session = Depends(get_db)):
    """
    Returns average popularity, follower count, and track count per genre.
    Useful for identifying trending music genres.
    """
    results = (
        db.query(
            Artist.genre,
            func.count(Artist.id).label("artist_count"),
            func.avg(Artist.popularity).label("avg_popularity"),
            func.sum(Artist.followers).label("total_followers"),
        )
        .filter(Artist.genre.isnot(None))
        .group_by(Artist.genre)
        .order_by(func.avg(Artist.popularity).desc())
        .all()
    )
    return [
        {
            "genre": r.genre,
            "artist_count": r.artist_count,
            "avg_popularity": round(r.avg_popularity or 0, 2),
            "total_followers": r.total_followers or 0,
        }
        for r in results
    ]


@router.get("/top-tracks", summary="Top tracks by audio feature")
def top_tracks(
    sort_by: str = Query("popularity", description="Sort by: popularity, energy, danceability, valence"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    Returns top tracks ranked by a chosen audio feature.
    Great for generating charts like 'Most Danceable Tracks' or 'Highest Energy Songs'.
    """
    valid_fields = {"popularity", "energy", "danceability", "valence", "tempo"}
    if sort_by not in valid_fields:
        sort_by = "popularity"

    sort_col = getattr(Track, sort_by)
    tracks = db.query(Track).order_by(sort_col.desc()).limit(limit).all()

    return [
        {
            "rank": i + 1,
            "id": t.id,
            "title": t.title,
            "album_id": t.album_id,
            sort_by: getattr(t, sort_by),
            "duration_seconds": round((t.duration_ms or 0) / 1000, 1),
        }
        for i, t in enumerate(tracks)
    ]


@router.get("/mood-recommendations", summary="Recommend tracks by mood")
def mood_recommendations(
    mood: str = Query(..., description="Mood: happy, sad, energetic, calm, party"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """
    Returns tracks that match the requested mood based on audio feature analysis.

    Mood mappings:
    - **happy**: high valence (>0.7), medium-high energy
    - **sad**: low valence (<0.35), low energy
    - **energetic**: high energy (>0.75), high tempo
    - **calm**: low energy (<0.4), high valence
    - **party**: high danceability (>0.75), high energy
    """
    mood_filters = {
        "happy":     {"valence": (0.65, 1.0), "energy": (0.5, 1.0)},
        "sad":       {"valence": (0.0, 0.35), "energy": (0.0, 0.5)},
        "energetic": {"energy": (0.75, 1.0)},
        "calm":      {"energy": (0.0, 0.4), "valence": (0.4, 1.0)},
        "party":     {"danceability": (0.75, 1.0), "energy": (0.6, 1.0)},
    }

    filters = mood_filters.get(mood.lower())
    if not filters:
        return {"error": f"Unknown mood '{mood}'. Use: happy, sad, energetic, calm, party"}

    query = db.query(Track)
    for feature, (low, high) in filters.items():
        col = getattr(Track, feature)
        query = query.filter(col >= low, col <= high)

    tracks = query.order_by(Track.popularity.desc()).limit(limit).all()

    return {
        "mood": mood,
        "count": len(tracks),
        "tracks": [
            {
                "id": t.id,
                "title": t.title,
                "danceability": t.danceability,
                "energy": t.energy,
                "valence": t.valence,
                "popularity": t.popularity,
            }
            for t in tracks
        ],
    }


@router.get("/artist-stats/{artist_id}", summary="Detailed stats for an artist")
def artist_stats(artist_id: int, db: Session = Depends(get_db)):
    """
    Returns aggregated statistics for an artist including:
    album count, total tracks, average track popularity,
    and average audio features across all their tracks.
    """
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        return {"error": f"Artist {artist_id} not found"}

    stats = (
        db.query(
            func.count(Track.id).label("total_tracks"),
            func.avg(Track.popularity).label("avg_popularity"),
            func.avg(Track.danceability).label("avg_danceability"),
            func.avg(Track.energy).label("avg_energy"),
            func.avg(Track.valence).label("avg_valence"),
            func.avg(Track.tempo).label("avg_tempo"),
        )
        .join(Album, Track.album_id == Album.id)
        .filter(Album.artist_id == artist_id)
        .first()
    )

    album_count = db.query(func.count(Album.id)).filter(Album.artist_id == artist_id).scalar()

    def r(val):
        return round(val or 0, 3)

    return {
        "artist_id": artist_id,
        "name": artist.name,
        "genre": artist.genre,
        "followers": artist.followers,
        "popularity": artist.popularity,
        "album_count": album_count,
        "total_tracks": stats.total_tracks or 0,
        "audio_profile": {
            "avg_popularity": r(stats.avg_popularity),
            "avg_danceability": r(stats.avg_danceability),
            "avg_energy": r(stats.avg_energy),
            "avg_valence": r(stats.avg_valence),
            "avg_tempo": r(stats.avg_tempo),
        },
    }


@router.get("/decade-trends", summary="Track popularity trends by decade")
def decade_trends(db: Session = Depends(get_db)):
    """
    Analyzes how music audio features have changed across decades
    based on album release years.
    """
    results = (
        db.query(
            (func.floor(Album.release_year / 10) * 10).label("decade"),
            func.count(Track.id).label("track_count"),
            func.avg(Track.energy).label("avg_energy"),
            func.avg(Track.danceability).label("avg_danceability"),
            func.avg(Track.valence).label("avg_valence"),
            func.avg(Track.popularity).label("avg_popularity"),
        )
        .join(Track, Track.album_id == Album.id)
        .filter(Album.release_year.isnot(None))
        .group_by("decade")
        .order_by("decade")
        .all()
    )

    return [
        {
            "decade": f"{int(r.decade)}s",
            "track_count": r.track_count,
            "avg_energy": round(r.avg_energy or 0, 3),
            "avg_danceability": round(r.avg_danceability or 0, 3),
            "avg_valence": round(r.avg_valence or 0, 3),
            "avg_popularity": round(r.avg_popularity or 0, 2),
        }
        for r in results
        if r.decade
    ]


@router.get("/summary", summary="Database summary statistics")
def summary(db: Session = Depends(get_db)):
    """Returns a high-level overview of the database contents."""
    return {
        "total_artists": db.query(func.count(Artist.id)).scalar(),
        "total_albums": db.query(func.count(Album.id)).scalar(),
        "total_tracks": db.query(func.count(Track.id)).scalar(),
        "genres": db.query(func.count(func.distinct(Artist.genre))).scalar(),
        "avg_track_popularity": round(
            db.query(func.avg(Track.popularity)).scalar() or 0, 2
        ),
    }
