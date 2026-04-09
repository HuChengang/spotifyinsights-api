from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

# Many-to-many: Playlists <-> Tracks
playlist_tracks = Table(
    "playlist_tracks",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("track_id", Integer, ForeignKey("tracks.id"), primary_key=True),
)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    genre = Column(String)
    country = Column(String)
    followers = Column(Integer, default=0)
    popularity = Column(Float, default=0.0)  # 0-100
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    albums = relationship("Album", back_populates="artist", cascade="all, delete")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    release_year = Column(Integer)
    total_tracks = Column(Integer, default=0)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album", cascade="all, delete")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    duration_ms = Column(Integer, default=0)
    album_id = Column(Integer, ForeignKey("albums.id"), nullable=False)

    # Spotify audio features (0.0 - 1.0 scale)
    danceability = Column(Float, default=0.5)   # How suitable for dancing
    energy = Column(Float, default=0.5)          # Intensity and activity
    valence = Column(Float, default=0.5)         # Musical positiveness
    tempo = Column(Float, default=120.0)         # BPM
    popularity = Column(Float, default=0.0)      # 0-100

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    album = relationship("Album", back_populates="tracks")
    playlists = relationship("Playlist", secondary=playlist_tracks, back_populates="tracks")


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tracks = relationship("Track", secondary=playlist_tracks, back_populates="playlists")
