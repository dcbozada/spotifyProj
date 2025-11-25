import requests # type: ignore
import json 
import base64
import hashlib
import secrets
from urllib.parse import urlparse, parse_qs

# Authorization Code with PKCE Flow
# Code Challenge generation from a Code Verifier.
# Request authorization from the user and retrieve the authorization code.
# Request an access token from the authorization code.
# Finally, use the access token to make API calls.

# Prompt user for Client ID and Client Secret from Spotify App Dashboard
CLIENT_ID = str(input("Please Enter the CLIENT ID: "))
CLIENT_SECRET = str(input("Please Enter the CLIENT SECRET: "))
# Redirect URI I entered when first making app in spotify dashboard
REDIRECT_URI = 'http://127.0.0.1:8080'
# Scopes of user data I want to use
SCOPE = (
    "user-read-private "
    "user-read-email "
    "user-library-read "
    "user-top-read "
    "playlist-read-private "
    "playlist-read-collaborative "
)
AUTH_URL = 'https://accounts.spotify.com/authorize'
API_URL = "https://accounts.spotify.com/api/token"

class Token():

    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.scope = SCOPE
        self.redirect_uri = REDIRECT_URI
        self.auth_url = AUTH_URL
        self.api_url = API_URL


    # Creating code verifier
    # A secure random string (43-128 chars)
    def get_code_verifier(self) -> str:
        code_verifier = secrets.token_urlsafe(64)
        return code_verifier

    # creating code challenge 
    # once code verifier is generated, hash is using SHA256 algorithim
    def get_code_challenge(self, code_verifier) -> str:
        # calculate sha256 hash of the verifier
        code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
        # base64-url encode the result 
        code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=','')
        return code_challenge

    # Create OAuth Link 
    def create_oauth_link(self) -> tuple[str,str]:
        verifier = self.get_code_verifier()
        challenge = self.get_code_challenge(code_verifier=verifier)
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "code_challenge_method": "S256",
            "code_challenge": challenge
        }
        url = requests.Request('GET', self.auth_url, params=params).prepare().url
        return url, verifier

    def get_token(self, code_verifier: str) -> str:
        redirect_url = input('Please copy/paste the redirect URL: ')
        parsed_url = urlparse(redirect_url) # parse redirect url into sections
        auth_code = parse_qs(parsed_url.query).get("code",[None])[0] #turn query parameters into a dict
        payload = {
            "grant_type":"authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "code_verifier": code_verifier
        }
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        try:
            response = requests.post(self.api_url, data=payload, headers=headers) # post request to get access_token
            if response.status_code != 200:
                raise Exception(f"Token request failed: {response.text}")
            token_data = response.json() # convert response.Response object to json so python reads as dict
            return token_data['access_token'] # return the value in key 'access_token' of dict token_data
        except Exception as e:
            print("error in get_token()")

# def main():#
#     oauth_link, verifier = create_oauth_link()
#     print(f'Please use the below link to verify access to your Spotify data: \n\n {oauth_link}')
#     access_token = get_token(code_verifier=verifier)
#     print(f"Your access token is: {access_token}")
    

# if __name__ == "__main__":
#     main()



# def get_token() -> dict:
#     url = "https://accounts.spotify.com/api/token"
#     data = {"grant_type":"client_credentials"}
#     response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET)) # Post request to get access token

#     if response.status_code != 200: # successful requests.post equals 200, anyting but is a failure
#         raise Exception(f"Token request failed: {response.text}")
    
#     token_data = response.json() # convert request.Response object to json so python reads it as dict
#     return token_data['access_token'] # return the value in key 'access_tokens'

