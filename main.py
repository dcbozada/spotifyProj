from api import Spotify
from db import DB

def main():
    spotify = Spotify()
    history_df = spotify.get_history()
    tracks_df = spotify.get_my_tracks()
    artists_df = spotify.get_artists(tracks_df=tracks_df)
    albums_df = spotify.get_albums(tracks_df=tracks_df)

    db = DB()
    db.test_connection()
    db.create_insert_table_tracks(tracks_df=tracks_df)
    db.create_insert_table_history(history_df=history_df)
    db.create_insert_table_artists(artists_df=artists_df)
    db.create_insert_table_albums(albums_df=albums_df)
            
 
if __name__ == "__main__":
    main()

