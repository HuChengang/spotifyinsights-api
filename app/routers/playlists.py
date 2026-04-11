from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import Playlist, Track
from app.schemas.schemas import PlaylistCreate, PlaylistUpdate, PlaylistResponse

router = APIRouter()


@router.get("/", response_model=List[PlaylistResponse], summary="List all playlists")
def list_playlists(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return db.query(Playlist).offset(skip).limit(limit).all()


@router.get("/{playlist_id}", response_model=PlaylistResponse, summary="Get playlist by ID")
def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail=f"Playlist with id {playlist_id} not found")
    return playlist


@router.post("/", response_model=PlaylistResponse, status_code=201, summary="Create playlist (Auth required)")
def create_playlist(
    playlist: PlaylistCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_playlist = Playlist(**playlist.model_dump())
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


@router.put("/{playlist_id}", response_model=PlaylistResponse, summary="Update playlist (Auth required)")
def update_playlist(
    playlist_id: int,
    playlist_update: PlaylistUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail=f"Playlist with id {playlist_id} not found")
    for field, value in playlist_update.model_dump(exclude_unset=True).items():
        setattr(playlist, field, value)
    db.commit()
    db.refresh(playlist)
    return playlist


@router.delete("/{playlist_id}", status_code=204, summary="Delete playlist (Auth required)")
def delete_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail=f"Playlist with id {playlist_id} not found")
    db.delete(playlist)
    db.commit()
    return None


@router.post("/{playlist_id}/tracks/{track_id}", response_model=PlaylistResponse, summary="Add track to playlist (Auth required)")
def add_track_to_playlist(
    playlist_id: int,
    track_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Add a track to a playlist."""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    if track not in playlist.tracks:
        playlist.tracks.append(track)
        db.commit()
        db.refresh(playlist)
    return playlist


@router.delete("/{playlist_id}/tracks/{track_id}", response_model=PlaylistResponse, summary="Remove track from playlist (Auth required)")
def remove_track_from_playlist(
    playlist_id: int,
    track_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Remove a track from a playlist."""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    if track in playlist.tracks:
        playlist.tracks.remove(track)
        db.commit()
        db.refresh(playlist)
    return playlist
