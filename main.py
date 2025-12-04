import requests # type: ignore
import json
from get_token import Token
from etl import ETL

# setting json file names as global constants
TRACKS = "tracks.json"
ARTISTS = "artists.json"
ALBUMS = "albums.json"

def main():
    # create instances of necessary classes
    token = Token()
    etl = ETL()

    # create oauth link and get verifier 
    oauth_link, verifier = token.create_oauth_link()
    print(f"Please use following link to grant access to your Spotify data {oauth_link}")
    access_token = token.get_token(verifier)
    print(f"Your access token: {access_token}")

    # headers dictionary I will be using when making GET requests to api endpoints
    headers={f"Authorization": f"Bearer {access_token}"}

    # url is to get user 50 tracks from users liked songs playlists, only first 50
    my_tracks_url = "https://api.spotify.com/v1/me/tracks?limit=50"
    
    # request tracks info with GET and turn result into JSON
    result = requests.get(my_tracks_url, headers=headers)
    tracks_df = etl.jsonToDf(file_name=TRACKS, proc_what='tracks',
                             result=result)
    for i in tracks_df.columns:
        print(i)

    # empty string to append to for when I pull multiple artists
    artist_ids = ""
    for i in tracks_df.index:
        artist_ids += f'{tracks_df.loc[i, 'artist_id']},'
    # seting string to exclude the last character(it ends with a comma)
    artist_ids = artist_ids[:-1]
    
    # request artists info with GET and turn results into JSON
    artist_url = f"https://api.spotify.com/v1/artists?ids={artist_ids}"
    result = requests.get(artist_url, headers=headers)
    artists_df = etl.jsonToDf(file_name = ARTISTS, proc_what='artists',
                               result=result)
    for i in artists_df.columns:
        print(i)
    for i in artists_df.index:
        print(artists_df.loc[i, 'artist_genre'])



 
if __name__ == "__main__":
    main()

