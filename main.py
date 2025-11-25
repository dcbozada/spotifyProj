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

    # url is to get user 50 tracks from users liked songs playlists, only first 50
    my_tracks_url = "https://api.spotify.com/v1/me/tracks?limit=50"
    headers={f"Authorization": f"Bearer {access_token}"}
    
    # request with GET and turn result into JSON
    result = requests.get(my_tracks_url, headers=headers)
    tracks_df = etl.jsonToDf(file_name=TRACKS, proc_what='tracks',
                             result=result)
    print(tracks_df)

 
if __name__ == "__main__":
    main()

