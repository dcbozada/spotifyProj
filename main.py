import requests
from get_token import get_code_verifier, get_code_challenge, create_oauth_link, get_token

def main():#
    oauth_link, verifier = create_oauth_link()
    print(f"Please use following link to grant access to your Spotify data {oauth_link}")
    access_token = get_token(verifier)
    print(f"Your access token: {access_token}")
    url = "https://api.spotify.com/v1/me/tracks"
    
    my_tracks = requests.get()

if __name__ == "__main__":
    main()

