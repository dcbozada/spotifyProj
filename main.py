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
    print(albums_df)

    # testing postgres connection 
    # connecting to local postgres db
    engine = create_engine("postgresql://spotify_user:spotify_pass@localhost:5432/spotify")

    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("Successful connection to DB spotify: ", result.scalar())
    except Exception as e:
        print('Failure to connect to DB spotify: ',e)
 
if __name__ == "__main__":
    main()

