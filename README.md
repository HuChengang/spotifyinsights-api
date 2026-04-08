# 🎵 SpotifyInsights API

A data-driven music analytics REST API built with **FastAPI** and **SQLAlchemy**, featuring full CRUD operations, JWT authentication, and advanced analytics endpoints.

> **XJCO3011 Web Services and Web Data – Coursework 1**

---

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Running the API](#running-the-api)
- [API Documentation](#api-documentation)
- [Running Tests](#running-tests)
- [Importing Kaggle Data](#importing-kaggle-data)
- [Project Structure](#project-structure)

---

## Features

- ✅ Full **CRUD** for Artists, Albums, Tracks, and Playlists
- ✅ **JWT Authentication** protecting all write operations
- ✅ **Analytics endpoints**: genre trends, mood-based recommendations, decade trends, artist profiles
- ✅ **Pagination and filtering** on all list endpoints
- ✅ Auto-generated **Swagger UI** at `/docs`
- ✅ **SQLite** (dev) and **PostgreSQL** (production) support
- ✅ Kaggle dataset import script included

---

## Tech Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| Framework | FastAPI | Auto Swagger docs, async support, modern Python |
| Database | SQLite (dev) / PostgreSQL (prod) | Relational, ACID-compliant |
| ORM | SQLAlchemy 2.0 | Industry standard, clean query syntax |
| Auth | JWT via python-jose | Stateless, scalable |
| Testing | Pytest + HTTPX | Fast, readable tests |

---

## Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/spotifyinsights-api.git
cd spotifyinsights-api

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env if needed (defaults work out of the box with SQLite)

# 5. Seed sample data
python scripts/seed_data.py
```

---

## Running the API

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

---

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

A PDF export of the API documentation is available in `docs/api_documentation.pdf`.

---

## Authentication

Write operations (POST, PUT, DELETE) require a JWT token.

```bash
# 1. Get a token
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'

# 2. Use the token
curl -X POST http://localhost:8000/artists/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Artist", "genre": "Pop"}'
```

---

## Endpoints Overview

### CRUD
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/artists/` | List artists (paginated, filter by genre) |
| POST | `/artists/` | Create artist 🔒 |
| GET | `/artists/{id}` | Get artist by ID |
| PUT | `/artists/{id}` | Update artist 🔒 |
| DELETE | `/artists/{id}` | Delete artist 🔒 |
| GET/POST/PUT/DELETE | `/albums/` | Albums CRUD 🔒 |
| GET/POST/PUT/DELETE | `/tracks/` | Tracks CRUD 🔒 |
| GET/POST/PUT/DELETE | `/playlists/` | Playlists CRUD 🔒 |
| POST | `/playlists/{id}/tracks/{track_id}` | Add track to playlist 🔒 |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/summary` | DB overview stats |
| GET | `/analytics/genre-trends` | Popularity by genre |
| GET | `/analytics/top-tracks?sort_by=energy` | Ranked tracks by audio feature |
| GET | `/analytics/mood-recommendations?mood=happy` | Mood-based track suggestions |
| GET | `/analytics/artist-stats/{id}` | Full artist audio profile |
| GET | `/analytics/decade-trends` | How music changed across decades |

---

## Running Tests

```bash
pytest tests/ -v
```

---

## Importing Kaggle Data

Download the [Spotify Dataset from Kaggle](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks), then run:

```bash
python scripts/import_kaggle.py --file path/to/tracks.csv --limit 5000
```

---

## Project Structure

```
spotifyinsights-api/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   ├── config.py        # Settings (env vars)
│   │   ├── database.py      # SQLAlchemy engine & session
│   │   └── auth.py          # JWT authentication
│   ├── models/
│   │   └── models.py        # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── schemas.py       # Pydantic request/response schemas
│   └── routers/
│       ├── artists.py       # /artists CRUD
│       ├── albums.py        # /albums CRUD
│       ├── tracks.py        # /tracks CRUD
│       ├── playlists.py     # /playlists CRUD
│       ├── analytics.py     # /analytics endpoints
│       └── auth.py          # /token endpoint
├── scripts/
│   ├── seed_data.py         # Sample data seeder
│   └── import_kaggle.py     # Kaggle CSV importer
├── tests/
│   └── test_api.py          # Pytest test suite
├── .env.example
├── requirements.txt
└── README.md
```
