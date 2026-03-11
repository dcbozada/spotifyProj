import requests # type: ignore
import pandas as pd # type: ignore
from get_token import Token
from etl import ETL

# setting json file names as global constants
HISTORY = "listening_history.json"
TRACKS = "tracks.json"
ARTISTS = "artists.json"
ALBUMS = "albums.json"

class Spotify():
    def __init__(self):
        self.token = Token()
        self.etl = ETL()
        self.access_token = self.token.get_token()
        self.headers = {f"Authorization": f"Bearer {self.access_token}"}

    def get_history(self):
        # url is to get users 50 most recently listed to tracks - the engine of database
        listening_history_url = "https://api.spotify.com/v1/me/player/recently-played?limit=50"

        # request listening info with GET and turn result in JSON
        result = requests.get(listening_history_url, headers=self.headers)
        history_df = self.etl.jsonToDf(file_name=HISTORY, proc_what='history',
                                result=result)
        return history_df
    
    def get_my_tracks(self):
        # url is to get user 50 tracks from users liked songs playlists, only first 50
        my_tracks_url = "https://api.spotify.com/v1/me/tracks?limit=50"
        
        # request tracks info with GET and turn result into JSON
        result = requests.get(my_tracks_url, headers=self.headers)
        tracks_df = self.etl.jsonToDf(file_name=TRACKS, proc_what='tracks',
                             result=result)
        return tracks_df
    
    def get_artists(self, tracks_df: pd.DataFrame):
        # empty string to append to for when I pull multiple artists
        artist_ids = ""
        for i in tracks_df.index:
            artist_ids += f'{tracks_df.loc[i, 'artist_id']},'
        # seting string to exclude the last character(it ends with a comma)
        artist_ids = artist_ids[:-1]
        
        # request artists info with GET and turn results into JSON
        artist_url = f"https://api.spotify.com/v1/artists?ids={artist_ids}"
        result = requests.get(artist_url, headers=self.headers)
        artists_df = self.etl.jsonToDf(file_name = ARTISTS, proc_what='artists',
                                result=result)
        return artists_df
    
    def get_albums(self, tracks_df:pd.DataFrame):
        # empty string to append to for when I pull multiple albums
        album_ids_1 = ""
        album_ids_2 = ""
        album_ids_3 = ""
        for i in tracks_df.index:
            if i > 0 and i <= 19:
                album_ids_1 += f"{tracks_df.loc[i, 'album_id']},"
            elif i >= 20 and i <= 39:
                album_ids_2 += f"{tracks_df.loc[i, 'album_id']},"
            else:
                album_ids_3 += f"{tracks_df.loc[i, 'album_id']},"
        album_ids_1 = album_ids_1[:-1]
        album_ids_2 = album_ids_2[:-1]
        album_ids_3 = album_ids_3[:-1]
        # request album endpoint and turn JSON to df
        # we have to append the results and make multiple calls due to 20 LIMIT max 
        album_url_1 = f"https://api.spotify.com/v1/albums?ids={album_ids_1}"
        album_url_2 = f"https://api.spotify.com/v1/albums?ids={album_ids_2}"
        album_url_3 = f"https://api.spotify.com/v1/albums?ids={album_ids_3}"
        result_1 = requests.get(album_url_1,headers=self.headers)
        result_2 = requests.get(album_url_2,headers=self.headers)
        result_3 = requests.get(album_url_3,headers=self.headers)
        album_df = pd.concat(
            [
                self.etl.jsonToDf(file_name=ALBUMS, proc_what='albums', result=result_1),
                self.etl.jsonToDf(file_name=ALBUMS, proc_what='albums', result=result_2),
                self.etl.jsonToDf(file_name=ALBUMS, proc_what='albums', result=result_3),
            ], ignore_index=True
        )
        return album_df