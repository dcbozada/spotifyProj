import requests # type: ignore
import json
from get_token import Token
from etl import ETL

def main():
    # create instances of necessary classes
    token = Token()
    etl = ETL()

    # create oauth link and get verifier 
    oauth_link, verifier = token.create_oauth_link()
    print(f"Please use following link to grant access to your Spotify data {oauth_link}")
    access_token = token.get_token(verifier)
    print(f"Your access token: {access_token}")

    # url is to get user 50 tracks from users liked songs playlists
    url = "https://api.spotify.com/v1/me/tracks?limit=50"
    headers={f"Authorization": f"Bearer {access_token}"}
    
    # request with GET and turn result into JSON
    my_tracks = requests.get(url, headers=headers)
    my_tracks = my_tracks.json()
    # then dump my_tracks into a readable json file
    with open("my_tracks.json", "w") as f:
        # json.dump 
        json.dump(my_tracks, f, indent = 4)

    tracks_df = etl.jsonToDf()

 
if __name__ == "__main__":
    main()

