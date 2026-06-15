# Spotify ETL Pipeline

A Python pipeline that pulls your Spotify listening data from the Spotify API and loads it into a local PostgreSQL database running in Docker.

## What It Does

- Fetches your 50 most recently played tracks
- Fetches **all** of your saved/liked tracks via paginated API calls
- Fetches artist and album details for every saved track, batched to respect API limits
- Transforms the raw API responses into structured DataFrames
- Loads the data into a PostgreSQL database across 4 tables

## Prerequisites

- Python 3.10+
- Docker Desktop
- A [Spotify Developer App](https://developer.spotify.com/dashboard) with a registered redirect URI

## Setup

### 1. Clone the repo and install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your `.env` file

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

**Spotify API**
- `CLIENT_ID` and `CLIENT_SECRET` — from your Spotify Developer App
- `REDIRECT_URI` — must match what's registered in your Spotify app (e.g. `http://127.0.0.1:8080`)
- `AUTH_URL` — `https://accounts.spotify.com/authorize`
- `API_TOKEN_URL` — `https://accounts.spotify.com/api/token`

**PostgreSQL / Docker**
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`, `DB_CONTAINER_NAME`

### 3. Start the database

```bash
bash start_db.sh
```

This creates and starts a PostgreSQL Docker container on first run, or restarts the existing one on subsequent runs.

### 4. Run the pipeline

```bash
python main.py
```

On the first run you will be prompted to visit a Spotify OAuth URL in your browser. After authorizing, paste the redirect URL back into the terminal. Your tokens are saved to `.env` and auto-refreshed on future runs.

## Project Structure

```
├── main.py           # Entry point — orchestrates the full pipeline
├── get_token.py      # Spotify OAuth2 with PKCE — handles auth and token refresh
├── api.py            # All Spotify API calls — returns pandas DataFrames
├── etl.py            # Transforms raw API responses into DataFrames
├── db.py             # PostgreSQL interactions via SQLAlchemy
├── start_db.sh       # Shell script to create/start the Docker container
├── requirements.txt  # Python dependencies
└── .env.example      # Template for required environment variables
```

## Data Flow

```
Spotify API → raw JSON files → pandas DataFrames → PostgreSQL
```

## Database

Data is loaded into a PostgreSQL database running in Docker. All 4 tables are dropped and recreated on each run.

| Table     | Columns                                                                          |
|-----------|----------------------------------------------------------------------------------|
| `tracks`  | `tracks_id`, `tracks_name`, `artist_id`, `album_id`, `duration_ms`, `added_at`  |
| `history` | `played_at`, `track_id`, `context_type`, `context_uri`                           |
| `artists` | `artist_id`, `artist_name`, `artist_genre`, `artist_followers`, `artist_popularity` |
| `albums`  | `album_id`, `name`, `release_date`, `album_type`, `total_tracks`, `image_url`   |

### Querying the database

```powershell
docker exec -it <DB_CONTAINER_NAME> psql -U <POSTGRES_USER> -d <POSTGRES_DB>
```
