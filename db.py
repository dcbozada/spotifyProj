import dotenv #type:ignore
import os
from sqlalchemy import create_engine, text #type:ignore
import pandas as pd #type:ignore

# loading environment variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
DB_CONTAINER_NAME=os.getenv("DB_CONTAINER_NAME")

# creating class DB() to handle work with docker psql db
class DB():
    def __init__(self):
        # connection to local postgres db
        self.engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
            )


    # function to test the connection to database
    def test_connection(self) -> str:
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1;"))
                print("Successful Connection to DB 'spotify'", result.scalar())
        except Exception as e:
            print("Failed to connect to DB 'spotify'")

    # funtion to create/insert into table 'tracks'
    def create_insert_table_tracks(self, tracks_df: pd.DataFrame):
        # creating the table tracks
        create_table_tracks_sql = """
        DROP TABLE IF EXISTS tracks;
        CREATE TABLE IF NOT EXISTS tracks (
        tracks_id VARCHAR PRIMARY KEY,
        tracks_name VARCHAR,
        artist_id VARCHAR,
        album_id VARCHAR,
        duration_ms VARCHAR,
        added_at VARCHAR)"""

        # create tracks table
        # when creating/dropping tables w/ sql alchemy, commit must be used (conn.commit())
        # BUT you do not have to set the executed statement to a varibale
        # THIS IS ONLY FOR CREATING/DROPPING TABLES
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_tracks_sql))
                conn.commit()
                print("Table 'tracks' created")
        except Exception as e:
            print("Error occured with creating table 'tracks': ", e)

        # inserting tracks_df into table 'tracks'
        # when using sql alchemy to INSERT into tables, no commit is needed
        # since to_sql() is in auto commit mode
        tracks_df.to_sql("tracks", self.engine, if_exists='replace', index=False)

    # creating/inserting the history table
    def create_insert_table_history(self, history_df:pd.DataFrame):
        create_table_history_sql = """
        DROP TABLE IF EXISTS history;
        CREATE TABLE IF NOT EXISTS history (
        played_at TIMESTAMPTZ,
        track_id VARCHAR,
        context_type VARCHAR,
        context_uri VARCHAR)"""

        # create history table
        # when creating/dropping tables w/ sql alchemy, commit must be used (conn.commit())
        # BUT you do not have to set the executed statement to a varibale
        # THIS IS ONLY FOR CREATING/DROPPING TABLES
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_history_sql))
                conn.commit()
                print("Table 'history' created")
        except Exception as e:
            print("Error with creating table 'history': ",e)

        # inserting history_df into table 'history'
        # when using sql alchemy to INSERT into tables, no commit is needed
        # since to_sql() is in auto commit mode
        history_df.to_sql("history", self.engine, if_exists='replace', index=False)

    # creating/inserting the artists table
    def create_insert_table_artists(self, artists_df: pd.DataFrame):
        create_table_artists_sql = """
        DROP TABLE IF EXISTS artists;
        CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR PRIMARY KEY,
        artist_name VARCHAR,
        artist_genre VARCHAR,
        artist_followers VARCHAR,
        artist_popularity VARCHAR)"""

        # create artists table
        # when creating/dropping tables w/ sql alchemy, commit must be used (conn.commit())
        # BUT you do not have to set the executed statement to a varibale
        # THIS IS ONLY FOR CREATING/DROPPING TABLES
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_artists_sql))
                conn.commit()
                print("Table 'artists' created")
        except Exception as e:
            print("Error with creating table 'artists': ", e)

        # inserting artists_df into table 'artists'
        # when using sql alchemy to INSERT into tables, no commit is needed
        # since to_sql() is in auto commit mode
        artists_df.to_sql("artists", self.engine, if_exists='replace', index=False)

    # creating/inserting the albums table
    def create_insert_table_albums(self, albums_df: pd.DataFrame):
        create_table_albums_sql = """
        DROP TABLE IF EXISTS albums;
        CREATE TABLE IF NOT EXISTS albums (
        album_id VARCHAR PRIMARY KEY,
        name VARCHAR,
        release_date VARCHAR,
        album_type VARCHAR,
        total_tracks VARCHAR,
        image_url VARCHAR)"""

        # create albums table
        # when creating/dropping tables w/ sql alchemy, commit must be used (conn.commit())
        # BUT you do not have to set the executed statement to a varibale
        # THIS IS ONLY FOR CREATING/DROPPING TABLES
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_table_albums_sql))
                conn.commit()
                print("Table 'albums' created")
        except Exception as e:
            print("Error with creating table 'albums': ", e)

        # inserting albums_df into table 'albums'
        # when using sql alchemy to INSERT into tables, no commit is needed
        # since to_sql() is in auto commit mode
        albums_df.to_sql("albums", self.engine, if_exists='replace', index=False)
