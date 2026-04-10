from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routers import artists, albums, tracks, playlists, analytics, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SpotifyInsights API",
    description="""
## 🎵 SpotifyInsights API

A data-driven music analytics API built with FastAPI and PostgreSQL.

### Features
- Full CRUD for Artists, Albums, Tracks, and Playlists
- Analytics endpoints: genre trends, mood-based recommendations, top charts
- JWT Authentication for protected write routes
- Pagination and filtering support
    """,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(artists.router, prefix="/artists", tags=["Artists"])
app.include_router(albums.router, prefix="/albums", tags=["Albums"])
app.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
app.include_router(playlists.router, prefix="/playlists", tags=["Playlists"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to SpotifyInsights API 🎵",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
