from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import Track, Album
from app.schemas.schemas import TrackCreate, TrackUpdate, TrackResponse

router = APIRouter()


@router.get("/", response_model=List[TrackResponse], summary="List all tracks")
def list_tracks(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    album_id: Optional[int] = Query(None),
    min_energy: Optional[float] = Query(None, ge=0, le=1, description="Minimum energy score"),
    min_danceability: Optional[float] = Query(None, ge=0, le=1),
    db: Session = Depends(get_db),
):
    """List tracks with optional audio feature filters."""
    query = db.query(Track)
    if album_id:
        query = query.filter(Track.album_id == album_id)
    if min_energy is not None:
        query = query.filter(Track.energy >= min_energy)
    if min_danceability is not None:
        query = query.filter(Track.danceability >= min_danceability)
    return query.offset(skip).limit(limit).all()


@router.get("/{track_id}", response_model=TrackResponse, summary="Get track by ID")
def get_track(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail=f"Track with id {track_id} not found")
    return track


@router.post("/", response_model=TrackResponse, status_code=201, summary="Create track (Auth required)")
def create_track(
    track: TrackCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    album = db.query(Album).filter(Album.id == track.album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail=f"Album with id {track.album_id} not found")
    db_track = Track(**track.model_dump())
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


@router.put("/{track_id}", response_model=TrackResponse, summary="Update track (Auth required)")
def update_track(
    track_id: int,
    track_update: TrackUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail=f"Track with id {track_id} not found")
    for field, value in track_update.model_dump(exclude_unset=True).items():
        setattr(track, field, value)
    db.commit()
    db.refresh(track)
    return track


@router.delete("/{track_id}", status_code=204, summary="Delete track (Auth required)")
def delete_track(
    track_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail=f"Track with id {track_id} not found")
    db.delete(track)
    db.commit()
    return None
