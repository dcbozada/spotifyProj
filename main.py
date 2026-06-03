from api import Spotify
from sqlalchemy import create_engine, text #type:ignore

def main():
    spotify = Spotify()
    history_df = spotify.get_history()
    print(history_df.head())
    tracks_df = spotify.get_my_tracks()
    print(tracks_df.head())
    artists_df = spotify.get_artists(tracks_df=tracks_df)
    print(artists_df.head())
    albums_df = spotify.get_albums(tracks_df=tracks_df)
    print(albums_df.head())

    # testing postgres connection 
    # connecting to local postgres db
    engine = create_engine("postgresql://spotify_user:spotify_pass@localhost:5432/spotify")

    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("Successful connection to DB spotify: ", result.scalar())
    except Exception as e:
        print('Failure to connect to DB spotify: ', e)

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
        with engine.connect() as conn:
            conn.execute(text(create_table_tracks_sql))
            conn.commit()
            print("Table 'tracks' created")
    except Exception as e:
        print("Error occured with creating table 'tracks: ", e)

    # inserting tracks_df into table 'tracks'
    # when using sql alchemy to INSERT into tables, no commit is needed
    # since to_sql() is in auto commit mode
    tracks_df.to_sql("tracks", engine, if_exists='replace', index=False)

    # testing to see if tracks_df inserted into table 'tracks' correctly
    # to see result of a SELECT statement using engine.connect().execute()
    # a for statement must be used to view the result, and the executed statement
    # must be set to a variable
    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM tracks'))
    for row in result:
        print(row)
            
 
if __name__ == "__main__":
    main()

