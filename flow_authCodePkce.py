import requests # type: ignore
import json 

# Prompt user for Client ID and Client Secret from Spotify App Dashboard
CLIENT_ID = str(input("Please Enter the CLIENT ID: "))
CLIENT_SECRET = str(input("Please Enter the CLIENT SECRET: "))

def get_token() -> dict:
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type":"client_credentials"}
    response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET)) # Post request to get access token

    if response.status_code != 200: # successful requests.post equals 200, anyting but is a failure
        raise Exception(f"Token request failed: {response.text}")
    
    token_data = response.json() # convert request.Response object to json so python reads it as dict
    return token_data['access_token'] # return the value in key 'access_tokens'

