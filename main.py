from api import Spotify

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
 
if __name__ == "__main__":
    main()

