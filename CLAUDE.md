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
- **`db.py`** — `DB` class. Owns all PostgreSQL interactions via SQLAlchemy. Reads credentials from `.env`. Methods: `test_connection()` (runs `SELECT 1` to verify the DB is reachable), `create_insert_table_tracks(tracks_df)` (drops/recreates the `tracks` table and loads the DataFrame into it via `to_sql()`).
- **`main.py`** — Entry point. Instantiates `Spotify()` and calls its four methods in sequence, then instantiates `DB()` and calls `test_connection()` and `create_insert_table_tracks()`.

## Data Flow

1. Spotify API → raw JSON files (`listening_history.json`, `tracks.json`, `artists.json`, `albums.json`)
2. JSON files → pandas DataFrames via `ETL.jsonToDf()`
3. DataFrames → PostgreSQL via `DB.create_insert_table_tracks(tracks_df)`

### Albums endpoint note
The Spotify `/albums` endpoint has a max of 20 IDs per request. `get_albums()` splits the 50 tracks across three batched requests and concatenates the results with `pd.concat(..., ignore_index=True)`.

## Database

PostgreSQL running in Docker — credentials are loaded from `.env`. Current active table: `tracks`. SQLAlchemy is used for the DB layer via the `DB` class in `db.py`. The `create_insert_table_tracks()` method uses `DROP TABLE IF EXISTS` + `CREATE TABLE` then `DataFrame.to_sql()` with `if_exists='replace'`.

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
