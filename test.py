import pandas as pd
import json
import requests
from etl import ETL
from get_token import Token


etl = ETL()
token = Token()

print(token.client_id)
print(token.redirect_uri)
print(token.auth_url)
print(token.api_url)

access_token = token.get_token()

# # headers dictionary I will be using when making GET requests to api endpoints
# headers={f"Authorization": f"Bearer {access_token}"}

# # url is to get user 50 tracks from users liked songs playlists, only first 50
# my_tracks_url = "https://api.spotify.com/v1/me/tracks?limit=50"

# # request tracks info with GET and turn result into JSON
# result = requests.get(my_tracks_url, headers=headers)
# if result.status_code == 401:
#     token.refresh_ac
# print(type(result))
# tracks_df = etl.jsonToDf(file_name=TRACKS, proc_what='tracks',
#                             result=result)
# for i in tracks_df.columns:
#     print(i)
