# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Project

```bash
python main.py
```

On first run (or after token expiry), the Token class will prompt you to visit an OAuth URL in the browser. After authorizing, paste the redirect URL back into the terminal. Tokens are stored in `.env` and auto-refreshed on subsequent runs.

## Architecture

Five-file pipeline with clear separation of concerns:

- **`get_token.py`** — `Token` class handles Spotify OAuth2 with PKCE. Reads/writes `ACCESS_TOKEN` and `REFRESH_TOKEN` to `.env`. Validates the current token on each run and refreshes if expired (HTTP 401).
- **`api.py`** — `Spotify` class. Owns all HTTP calls to the Spotify API. Methods: `get_history()`, `get_my_tracks()`, `get_artists(tracks_df)`, `get_albums(tracks_df)`. Each method calls the relevant endpoint, passes the raw response to `ETL.jsonToDf()`, and returns a DataFrame.
- **`etl.py`** — `ETL` class with `w_result_to_json()` (writes raw API response to disk) and `jsonToDf(file_name, proc_what, result)` (writes JSON → reads JSON → returns a pandas DataFrame). The `proc_what` parameter accepts `'history'`, `'tracks'`, `'artists'`, or `'albums'`.
- **`db.py`** — `DB` class. Owns all PostgreSQL interactions via SQLAlchemy. Reads credentials from `.env`. Methods: `test_connection()` (runs `SELECT 1` to verify the DB is reachable), `create_insert_table_tracks()`, `create_insert_table_history()`, `create_insert_table_artists()`, `create_insert_table_albums()` — each drops/recreates its table and loads the DataFrame via `to_sql()`.
- **`main.py`** — Entry point. Instantiates `Spotify()` and calls its four methods in sequence, then instantiates `DB()` and calls `test_connection()` followed by all four `create_insert_table_*()` methods.

## Data Flow

1. Spotify API → raw JSON files (`listening_history.json`, `tracks.json`, `artists.json`, `albums.json`)
2. JSON files → pandas DataFrames via `ETL.jsonToDf()`
3. DataFrames → PostgreSQL via `DB.create_insert_table_tracks()`, `create_insert_table_history()`, `create_insert_table_artists()`, `create_insert_table_albums()`

### API batching notes
- `get_my_tracks()` paginates through the full saved tracks library using a while loop with `limit=50` and an incrementing `offset`, stopping when the offset exceeds the total track count returned by the API.
- `get_artists()` batches up to 50 IDs per request using a `chunks()` generator. Results are accumulated into `all_artists` and passed to `ETL.jsonToDf()` once after the loop.
- `get_albums()` batches up to 20 IDs per request (Spotify's max for this endpoint) using the same `chunks()` pattern. Results are accumulated into `all_albums` and passed to `ETL.jsonToDf()` once after the loop.

## Database

PostgreSQL running in Docker — credentials are loaded from `.env`. Active tables: `tracks`, `history`, `artists`, `albums`. SQLAlchemy is used for the DB layer via the `DB` class in `db.py`. Each `create_insert_table_*()` method uses `DROP TABLE IF EXISTS` + `CREATE TABLE` then `DataFrame.to_sql()` with `if_exists='replace'`.

### Starting the database (Docker)

```bash
bash start_db.sh
```

`start_db.sh` reads credentials from `.env` and either creates the container on first run or restarts it on subsequent runs.

## Environment Variables (`.env`)

Required keys — see `.env.example`:

**Spotify API**
- `CLIENT_ID`, `CLIENT_SECRET`, `REDIRECT_URI`, `AUTH_URL`, `API_TOKEN_URL`
- `ACCESS_TOKEN`, `REFRESH_TOKEN` (populated automatically after first auth)

**PostgreSQL / Docker**
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_PORT`, `DB_CONTAINER_NAME`

## Key Dependencies

- `pandas` — DataFrames
- `requests` — Spotify API HTTP calls
- `python-dotenv` — `.env` read/write
- `sqlalchemy` — PostgreSQL integration (active, used in `db.py`)

## Spotify API Scopes Used

`user-library-read`, `user-read-recently-played`, `user-read-private`, `user-read-email`, `user-top-read`, `playlist-read-private`, `playlist-read-collaborative`
