import requests # type: ignore
import json 
import base64
import hashlib
import secrets

# Authorization Code with PKCE Flow
# Code Challenge generation from a Code Verifier.
# Request authorization from the user and retrieve the authorization code.
# Request an access token from the authorization code.
# Finally, use the access token to make API calls.

# Prompt user for Client ID and Client Secret from Spotify App Dashboard
CLIENT_ID = str(input("Please Enter the CLIENT ID: "))
CLIENT_SECRET = str(input("Please Enter the CLIENT SECRET: "))

# Redirect URI I entered when first making app in spotify dashboard
REDIRECT_URI = 'http://127.0.0.1:3000'

# Creating code verifier
# A secure random string (43-128 chars)
def get_code_verifier() -> str:
    code_verifier = secrets.token_urlsafe(64)
    return code_verifier

# creating code challenge 
# once code verifier is generated, hash is using SHA256 algorithim
def get_code_challenge(code_verifier):
    # calculate sha256 hash of the verifier
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    # base64-url encode the result 
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=','')
    return code_challenge

verifier = get_code_verifier()
challenge = get_code_challenge(verifier)
print(f'verifier: {verifier}')
print(f'challenge: {challenge}')



# # Create OAuth Link 
# def create_oauth_link():
#     params = {
#         "client_id": CLIENT_ID,
#         "response_type": "code",
#         "redirect_uri": REDIRECT_URI,
#         "scope": 

#     }

# def get_token() -> dict:
#     url = "https://accounts.spotify.com/api/token"
#     data = {"grant_type":"client_credentials"}
#     response = requests.post(url, data=data, auth=(CLIENT_ID, CLIENT_SECRET)) # Post request to get access token

#     if response.status_code != 200: # successful requests.post equals 200, anyting but is a failure
#         raise Exception(f"Token request failed: {response.text}")
    
#     token_data = response.json() # convert request.Response object to json so python reads it as dict
#     return token_data['access_token'] # return the value in key 'access_tokens'

