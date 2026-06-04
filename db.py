import dotenv #type:ignore
import os
from sqlalchemy import create_engine, text #type:ignore

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
    def create_insert_table_tracks(self, tracks_df):
        # creating the table tracks 
        create_table_tracks_sql = """
        DROP TABLE IF EXISTS tables;
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
            print("Error occured with creating table 'tracks: ", e)

        # inserting tracks_df into table 'tracks'
        # when using sql alchemy to INSERT into tables, no commit is needed
        # since to_sql() is in auto commit mode
        tracks_df.to_sql("tracks", self.engine, if_exists='replace', index=False)