from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import Artist
from app.schemas.schemas import ArtistCreate, ArtistUpdate, ArtistResponse

router = APIRouter()


@router.get("/", response_model=List[ArtistResponse], summary="List all artists")
def list_artists(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Max records to return"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    db: Session = Depends(get_db),
):
    """Retrieve a paginated list of artists with optional genre filtering."""
    query = db.query(Artist)
    if genre:
        query = query.filter(Artist.genre.ilike(f"%{genre}%"))
    return query.offset(skip).limit(limit).all()


@router.get("/{artist_id}", response_model=ArtistResponse, summary="Get artist by ID")
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    """Retrieve a single artist by their ID."""
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail=f"Artist with id {artist_id} not found")
    return artist


@router.post("/", response_model=ArtistResponse, status_code=201, summary="Create artist (Auth required)")
def create_artist(
    artist: ArtistCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Create a new artist. Requires JWT authentication."""
    db_artist = Artist(**artist.model_dump())
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


@router.put("/{artist_id}", response_model=ArtistResponse, summary="Update artist (Auth required)")
def update_artist(
    artist_id: int,
    artist_update: ArtistUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Update an existing artist's details. Requires JWT authentication."""
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail=f"Artist with id {artist_id} not found")
    for field, value in artist_update.model_dump(exclude_unset=True).items():
        setattr(artist, field, value)
    db.commit()
    db.refresh(artist)
    return artist


@router.delete("/{artist_id}", status_code=204, summary="Delete artist (Auth required)")
def delete_artist(
    artist_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """Delete an artist and all their albums/tracks. Requires JWT authentication."""
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail=f"Artist with id {artist_id} not found")
    db.delete(artist)
    db.commit()
    return None
# Improve error messages
