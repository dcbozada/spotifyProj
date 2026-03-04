# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Project

```bash
python main.py
```

On first run (or after token expiry), the Token class will prompt you to visit an OAuth URL in the browser. After authorizing, paste the redirect URL back into the terminal. Tokens are stored in `.env` and auto-refreshed on subsequent runs.

## Architecture

Three-file pipeline with clear separation of concerns:

- **`get_token.py`** — `Token` class handles Spotify OAuth2 with PKCE. Reads/writes `ACCESS_TOKEN` and `REFRESH_TOKEN` to `.env`. Validates the current token on each run and refreshes if expired (HTTP 401).
- **`etl.py`** — `ETL` class with `w_result_to_json()` (writes raw API response to disk) and `jsonToDf(proc_what=...)` (reads JSON → pandas DataFrame). The `proc_what` parameter accepts `'history'`, `'tracks'`, or `'artists'`.
- **`main.py`** — Orchestrates the pipeline: gets token → calls three Spotify endpoints → writes JSON → converts to DataFrames.

## Data Flow

1. Spotify API → raw JSON files (`listening_history.json`, `tracks.json`, `artists.json`)
2. JSON files → pandas DataFrames via `ETL.jsonToDf()`
3. DataFrames → PostgreSQL (code exists in `etl.py` but is currently commented out)

## Database

PostgreSQL target connection: `postgresql://dylan:wooli@localhost:5432/spotify`

Three planned tables: `history`, `tracks`, `artists`. SQLAlchemy is used for the DB layer. The DB insertion code in `etl.py` is commented out and ready to be re-enabled.

## Environment Variables (`.env`)

Required keys — see `.env.example`:
- `CLIENT_ID`, `REDIRECT_URI`, `AUTH_URL`, `API_TOKEN_URL`
- `ACCESS_TOKEN`, `REFRESH_TOKEN` (populated automatically after first auth)

## Key Dependencies

- `pandas` — DataFrames
- `requests` — Spotify API HTTP calls
- `python-dotenv` — `.env` read/write
- `sqlalchemy` — PostgreSQL integration (inactive)

## Spotify API Scopes Used

`user-library-read`, `user-read-recently-played`, `user-read-private`, `user-read-email`, `user-top-read`, `playlist-read-private`, `playlist-read-collaborative`
