from api import Spotify
from db import DB
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

    db = DB()
    db.test_connection()
    db.create_insert_table_tracks(tracks_df=tracks_df)
    db.create_insert_table_history(history_df=history_df)
    db.create_insert_table_artists(artists_df=artists_df)
    db.create_insert_table_albums(albums_df=albums_df)
            
 
if __name__ == "__main__":
    main()

