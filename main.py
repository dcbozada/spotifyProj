import requests # type: ignore
import json
from get_token import get_code_verifier, get_code_challenge, create_oauth_link, get_token

def main():#
    oauth_link, verifier = create_oauth_link()
    print(f"Please use following link to grant access to your Spotify data {oauth_link}")
    access_token = get_token(verifier)
    print(f"Your access token: {access_token}")
    url = "https://api.spotify.com/v1/me/tracks?limit=20"
    headers={f"Authorization": f"Bearer {access_token}"}
    
    my_tracks = requests.get(url, headers=headers)
    my_tracks = my_tracks.json()
    print(my_tracks)

if __name__ == "__main__":
    main()

