import requests # type: ignore
import subprocess
import json 


def get_token() -> None:
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type":"client_credentials"}
    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET))

    if response.status_code != 200:
        raise Exception(f"Token request failed: {response.text}")
    
    token_data = response.json()
    return token_data


foo = get_token()
print(foo)