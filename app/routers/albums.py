from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import Album, Artist
from app.schemas.schemas import AlbumCreate, AlbumUpdate, AlbumResponse

router = APIRouter()


@router.get("/", response_model=List[AlbumResponse], summary="List all albums")
def list_albums(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    artist_id: Optional[int] = Query(None, description="Filter by artist ID"),
    year: Optional[int] = Query(None, description="Filter by release year"),
    db: Session = Depends(get_db),
):
    """Retrieve albums with optional filtering by artist or release year."""
    query = db.query(Album)
    if artist_id:
        query = query.filter(Album.artist_id == artist_id)
    if year:
        query = query.filter(Album.release_year == year)
    return query.offset(skip).limit(limit).all()


@router.get("/{album_id}", response_model=AlbumResponse, summary="Get album by ID")
def get_album(album_id: int, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail=f"Album with id {album_id} not found")
    return album


@router.post("/", response_model=AlbumResponse, status_code=201, summary="Create album (Auth required)")
def create_album(
    album: AlbumCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    # Verify artist exists
    artist = db.query(Artist).filter(Artist.id == album.artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail=f"Artist with id {album.artist_id} not found")
    db_album = Album(**album.model_dump())
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


@router.put("/{album_id}", response_model=AlbumResponse, summary="Update album (Auth required)")
def update_album(
    album_id: int,
    album_update: AlbumUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail=f"Album with id {album_id} not found")
    for field, value in album_update.model_dump(exclude_unset=True).items():
        setattr(album, field, value)
    db.commit()
    db.refresh(album)
    return album


@router.delete("/{album_id}", status_code=204, summary="Delete album (Auth required)")
def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    album = db.query(Album).filter(Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail=f"Album with id {album_id} not found")
    db.delete(album)
    db.commit()
    return None
# Fix: ensure 404 is returned not 500 on missing artist
