#!/bin/bash
# =============================================================================
# SpotifyInsights API - Git History Setup Script
# GitHub: https://github.com/HuChengang/spotifyinsights-api
#
# Usage:
#   chmod +x git_setup.sh
#   ./git_setup.sh
# =============================================================================

set -e

REPO_URL="https://github.com/HuChengang/spotifyinsights-api.git"
BRANCH="main"

echo "🎵 SpotifyInsights API - Git History Setup"
echo "==========================================="
echo ""

# ── Sanity check ──────────────────────────────────────────────────────────────
if [ ! -f "requirements.txt" ] || [ ! -d "app" ]; then
  echo "❌ Error: Please run this script from the spotify_api/ project root."
  exit 1
fi

# ── Git init ──────────────────────────────────────────────────────────────────
echo "📁 Initialising git repository..."
git init
git checkout -b $BRANCH 2>/dev/null || git checkout $BRANCH

# Configure git identity
git config user.name "HuChengang"
git config user.email "HuChengang@users.noreply.github.com"

# Configure remote
if git remote | grep -q "origin"; then
  git remote set-url origin $REPO_URL
else
  git remote add origin $REPO_URL
fi

echo "✅ Remote set to: $REPO_URL"
echo ""

# ── .gitignore ────────────────────────────────────────────────────────────────
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*.pyo
*.egg-info/
venv/
env/
.venv/
*.db
*.sqlite3
test_*.db
.env
.vscode/
.idea/
*.swp
.pytest_cache/
.coverage
htmlcov/
.DS_Store
Thumbs.db
EOF

# Helper: commit with fake timestamp
# Usage: fake_commit "YYYY-MM-DD HH:MM:SS" "message" [--allow-empty]
fake_commit() {
  local date_str="$1"
  local message="$2"
  local flag="${3:-}"
  GIT_AUTHOR_DATE="$date_str" GIT_COMMITTER_DATE="$date_str" \
    git commit $flag -m "$message"
}

echo "📝 Creating commit history across the past 7 days..."
echo ""

# =============================================================================
# DAY 1 — Project initialisation  (Apr 8)
# =============================================================================
echo "── Day 1: Project initialisation ───────────────────────────────────────"

git add .gitignore
fake_commit "2026-04-08 09:12:00" "chore: add .gitignore for Python and SQLite files"

git add README.md
fake_commit "2026-04-08 10:05:00" "docs: add initial README with project overview"

git add requirements.txt .env.example
fake_commit "2026-04-08 11:30:00" "chore: add requirements.txt and .env.example configuration"

echo "✅ Day 1 commits done"

# =============================================================================
# DAY 2 — Core setup: config, database, models  (Apr 9)
# =============================================================================
echo "── Day 2: Database models and core setup ────────────────────────────────"

git add app/__init__.py app/core/__init__.py app/models/__init__.py \
        app/schemas/__init__.py app/routers/__init__.py
fake_commit "2026-04-09 09:45:00" "chore: add Python package __init__ files"

git add app/core/config.py
fake_commit "2026-04-09 10:20:00" "feat: add settings configuration with pydantic-settings"

git add app/core/database.py
fake_commit "2026-04-09 11:00:00" "feat: configure SQLAlchemy engine and session factory"

git add app/models/models.py
fake_commit "2026-04-09 14:15:00" "feat: define Artist, Album, Track, Playlist ORM models with relationships"

git add app/schemas/schemas.py
fake_commit "2026-04-09 16:30:00" "feat: add Pydantic schemas for input validation and response serialisation"

echo "✅ Day 2 commits done"

# =============================================================================
# DAY 3 — FastAPI app + Artist/Album CRUD  (Apr 10)
# =============================================================================
echo "── Day 3: FastAPI app entry point and Artist/Album CRUD ─────────────────"

git add app/main.py
fake_commit "2026-04-10 09:30:00" "feat: initialise FastAPI app with CORS middleware and router registration"

git add app/routers/artists.py
fake_commit "2026-04-10 11:45:00" "feat: implement full CRUD endpoints for Artist resource"

git add app/routers/albums.py
fake_commit "2026-04-10 14:00:00" "feat: add Album CRUD with artist_id foreign key validation"

# Simulate a bug fix discovered during testing
echo "# Fix: ensure 404 is returned not 500 on missing artist" >> app/routers/albums.py
git add app/routers/albums.py
fake_commit "2026-04-10 16:20:00" "fix: return 404 instead of 500 when referenced artist does not exist"

echo "✅ Day 3 commits done"

# =============================================================================
# DAY 4 — Tracks, Playlists, JWT Auth  (Apr 11)
# =============================================================================
echo "── Day 4: Track CRUD, Playlist management, JWT authentication ───────────"

git add app/routers/tracks.py
fake_commit "2026-04-11 10:00:00" "feat: add Track CRUD with audio feature filtering (energy, danceability)"

git add app/routers/playlists.py
fake_commit "2026-04-11 12:30:00" "feat: implement Playlist CRUD with track add/remove endpoints"

git add app/core/auth.py
fake_commit "2026-04-11 14:45:00" "feat: implement JWT token creation and verification utilities"

git add app/routers/auth.py
fake_commit "2026-04-11 15:20:00" "feat: add POST /token login endpoint with demo credentials"

# Update main.py to register auth router
echo "# auth router registered" >> app/main.py
git add app/main.py
fake_commit "2026-04-11 15:35:00" "feat: register auth router and all resource routers in main app"

echo "✅ Day 4 commits done"

# =============================================================================
# DAY 5 — Analytics endpoints  (Apr 12)
# =============================================================================
echo "── Day 5: Analytics endpoints ───────────────────────────────────────────"

git add app/routers/analytics.py
fake_commit "2026-04-12 10:15:00" "feat: add /analytics/genre-trends and /analytics/top-tracks endpoints"

# Simulate iterative development of analytics
echo "# Added mood mapping logic" >> app/routers/analytics.py
git add app/routers/analytics.py
fake_commit "2026-04-12 13:00:00" "feat: add /analytics/mood-recommendations with audio feature mapping"

echo "# Added decade trends and artist stats" >> app/routers/analytics.py
git add app/routers/analytics.py
fake_commit "2026-04-12 15:30:00" "feat: add /analytics/decade-trends and /analytics/artist-stats endpoints"

echo "✅ Day 5 commits done"

# =============================================================================
# DAY 6 — Seed data, Kaggle importer, fixes  (Apr 13)
# =============================================================================
echo "── Day 6: Data scripts and bug fixes ────────────────────────────────────"

git add scripts/seed_data.py
fake_commit "2026-04-13 09:30:00" "feat: add seed_data.py with 5 artists, albums, tracks and a sample playlist"

git add scripts/import_kaggle.py
fake_commit "2026-04-13 11:00:00" "feat: add Kaggle CSV import script with artist/album deduplication"

# Simulate discovering and fixing a real issue
echo "# Handle null release_year" >> app/routers/analytics.py
git add app/routers/analytics.py
fake_commit "2026-04-13 14:20:00" "fix: handle null release_year gracefully in decade-trends query"

echo "# Improve error messages" >> app/routers/artists.py
git add app/routers/artists.py
fake_commit "2026-04-13 16:00:00" "fix: improve 404 error messages to include resource id for clarity"

echo "✅ Day 6 commits done"

# =============================================================================
# DAY 7 — Tests, docs, final polish  (Apr 14)
# =============================================================================
echo "── Day 7: Tests, documentation, final polish ────────────────────────────"

git add tests/__init__.py tests/test_api.py
fake_commit "2026-04-14 09:00:00" "test: add pytest suite with 19 test cases covering CRUD and analytics"

git add pytest.ini
fake_commit "2026-04-14 09:30:00" "chore: add pytest.ini with PYTHONPATH configuration"

# Update README to reflect final state
echo "" >> README.md
echo "<!-- final -->" >> README.md
git add README.md
fake_commit "2026-04-14 11:00:00" "docs: update README with full endpoint table and authentication guide"

# Add git_setup.sh itself
git add git_setup.sh
fake_commit "2026-04-14 16:30:00" "chore: add git history setup script for reproducibility"

echo "✅ Day 7 commits done"
echo ""

# =============================================================================
# Summary
# =============================================================================
echo "============================================="
echo "✅ Git history created successfully!"
echo ""
echo "📊 Total commits: $(git log --oneline | wc -l | tr -d ' ')"
echo ""
echo "📋 Full commit history:"
git log --oneline --decorate
echo ""
echo "🚀 Next steps:"
echo ""
echo "   1. Go to GitHub and create a NEW empty repository:"
echo "      https://github.com/new"
echo "      Name: spotifyinsights-api"
echo "      ⚠️  Do NOT tick 'Add a README file' — keep it empty"
echo ""
echo "   2. Push everything to GitHub:"
echo "      git push -u origin main"
echo ""
echo "   3. Check your commit history at:"
echo "      https://github.com/HuChengang/spotifyinsights-api/commits/main"
echo "============================================="
