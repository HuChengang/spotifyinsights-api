"""
Test suite for SpotifyInsights API
Run with: pytest tests/ -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# Use an in-memory SQLite DB for tests
TEST_DB_URL = "sqlite:///./test_spotify.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_auth_token():
    response = client.post("/token", json={"username": "admin", "password": "password123"})
    return response.json()["access_token"]


def auth_headers():
    return {"Authorization": f"Bearer {get_auth_token()}"}


# ─── Root ─────────────────────────────────────────────────────────────────────

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "SpotifyInsights" in response.json()["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# ─── Authentication ───────────────────────────────────────────────────────────

def test_login_success():
    response = client.post("/token", json={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failure():
    response = client.post("/token", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401


def test_protected_route_without_token():
    response = client.post("/artists/", json={"name": "Test Artist"})
    assert response.status_code == 401


# ─── Artists CRUD ─────────────────────────────────────────────────────────────

def test_create_artist():
    response = client.post(
        "/artists/",
        json={"name": "Test Artist", "genre": "Pop", "country": "UK", "followers": 1000, "popularity": 75.0},
        headers=auth_headers(),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Artist"
    assert data["genre"] == "Pop"
    return data["id"]


def test_get_artist():
    # Create first
    create_resp = client.post(
        "/artists/",
        json={"name": "Get Test Artist", "genre": "Jazz"},
        headers=auth_headers(),
    )
    artist_id = create_resp.json()["id"]
    response = client.get(f"/artists/{artist_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Get Test Artist"


def test_get_artist_not_found():
    response = client.get("/artists/99999")
    assert response.status_code == 404


def test_update_artist():
    create_resp = client.post(
        "/artists/",
        json={"name": "Update Test", "genre": "Rock"},
        headers=auth_headers(),
    )
    artist_id = create_resp.json()["id"]
    response = client.put(
        f"/artists/{artist_id}",
        json={"followers": 999999},
        headers=auth_headers(),
    )
    assert response.status_code == 200
    assert response.json()["followers"] == 999999


def test_delete_artist():
    create_resp = client.post(
        "/artists/",
        json={"name": "Delete Me"},
        headers=auth_headers(),
    )
    artist_id = create_resp.json()["id"]
    response = client.delete(f"/artists/{artist_id}", headers=auth_headers())
    assert response.status_code == 204
    # Confirm deletion
    get_resp = client.get(f"/artists/{artist_id}")
    assert get_resp.status_code == 404


def test_list_artists():
    response = client.get("/artists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_artists_genre_filter():
    # Create a uniquely-named genre artist
    client.post(
        "/artists/",
        json={"name": "Filter Test Artist", "genre": "UniqueGenreXYZ"},
        headers=auth_headers(),
    )
    response = client.get("/artists/?genre=UniqueGenreXYZ")
    assert response.status_code == 200
    assert len(response.json()) >= 1


# ─── Tracks CRUD ──────────────────────────────────────────────────────────────

def _create_artist_and_album():
    artist = client.post("/artists/", json={"name": "Track Test Artist"}, headers=auth_headers()).json()
    album = client.post(
        "/albums/",
        json={"title": "Track Test Album", "artist_id": artist["id"], "release_year": 2020},
        headers=auth_headers(),
    ).json()
    return artist["id"], album["id"]


def test_create_track():
    _, album_id = _create_artist_and_album()
    response = client.post(
        "/tracks/",
        json={"title": "Test Track", "album_id": album_id, "danceability": 0.8, "energy": 0.9, "valence": 0.7, "tempo": 128.0, "popularity": 85.0},
        headers=auth_headers(),
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Track"


def test_get_track_not_found():
    response = client.get("/tracks/99999")
    assert response.status_code == 404


# ─── Analytics ────────────────────────────────────────────────────────────────

def test_analytics_summary():
    response = client.get("/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_artists" in data
    assert "total_tracks" in data


def test_analytics_mood_recommendations():
    response = client.get("/analytics/mood-recommendations?mood=happy")
    assert response.status_code == 200
    data = response.json()
    assert "mood" in data
    assert data["mood"] == "happy"


def test_analytics_mood_invalid():
    response = client.get("/analytics/mood-recommendations?mood=unknown_mood")
    assert response.status_code == 200
    assert "error" in response.json()


def test_analytics_top_tracks():
    response = client.get("/analytics/top-tracks?sort_by=energy&limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_analytics_genre_trends():
    response = client.get("/analytics/genre-trends")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
