from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ─── Artist Schemas ───────────────────────────────────────────────────────────

class ArtistBase(BaseModel):
    name: str = Field(..., example="The Beatles")
    genre: Optional[str] = Field(None, example="Rock")
    country: Optional[str] = Field(None, example="UK")
    followers: Optional[int] = Field(0, example=1000000)
    popularity: Optional[float] = Field(0.0, ge=0, le=100, example=85.0)


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    genre: Optional[str] = None
    country: Optional[str] = None
    followers: Optional[int] = None
    popularity: Optional[float] = Field(None, ge=0, le=100)


class ArtistResponse(ArtistBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Album Schemas ────────────────────────────────────────────────────────────

class AlbumBase(BaseModel):
    title: str = Field(..., example="Abbey Road")
    release_year: Optional[int] = Field(None, example=1969)
    total_tracks: Optional[int] = Field(0, example=17)
    artist_id: int


class AlbumCreate(AlbumBase):
    pass


class AlbumUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    total_tracks: Optional[int] = None


class AlbumResponse(AlbumBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Track Schemas ────────────────────────────────────────────────────────────

class TrackBase(BaseModel):
    title: str = Field(..., example="Come Together")
    duration_ms: Optional[int] = Field(0, example=259000)
    album_id: int
    danceability: Optional[float] = Field(0.5, ge=0, le=1, example=0.72)
    energy: Optional[float] = Field(0.5, ge=0, le=1, example=0.85)
    valence: Optional[float] = Field(0.5, ge=0, le=1, example=0.63)
    tempo: Optional[float] = Field(120.0, example=100.0)
    popularity: Optional[float] = Field(0.0, ge=0, le=100, example=78.0)


class TrackCreate(TrackBase):
    pass


class TrackUpdate(BaseModel):
    title: Optional[str] = None
    duration_ms: Optional[int] = None
    danceability: Optional[float] = Field(None, ge=0, le=1)
    energy: Optional[float] = Field(None, ge=0, le=1)
    valence: Optional[float] = Field(None, ge=0, le=1)
    tempo: Optional[float] = None
    popularity: Optional[float] = Field(None, ge=0, le=100)


class TrackResponse(TrackBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Playlist Schemas ─────────────────────────────────────────────────────────

class PlaylistBase(BaseModel):
    name: str = Field(..., example="Workout Bangers")
    description: Optional[str] = Field("", example="High energy tracks for the gym")


class PlaylistCreate(PlaylistBase):
    pass


class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PlaylistResponse(PlaylistBase):
    id: int
    created_at: datetime
    tracks: List[TrackResponse] = []

    class Config:
        from_attributes = True


# ─── Auth Schemas ─────────────────────────────────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    username: str = Field(..., example="admin")
    password: str = Field(..., example="password123")
