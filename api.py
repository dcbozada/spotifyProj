import requests # type: ignore
import pandas as pd # type: ignore
from get_token import Token
from etl import ETL
import json

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
        # first call to get total number of saved tracks
        # only calling for 1 track so we can get the 'total' count
        one_result = requests.get("https://api.spotify.com/v1/me/tracks",
                                  headers=self.headers, params={"limit": 1})
        one_result = one_result.json()
        
        # setting the limit and offset to be called mutiple times in while loop
        limit = 50
        offset = 0
        items=[]
        
        # using this while loop to gather all my tracks
        # this works because if the offset is higher than the total
        # in the spotify api call, it will return an empty list
        while offset < one_result["total"]:
            # url to get 50 tracks
            result = requests.get("https://api.spotify.com/v1/me/tracks",
                                  headers=self.headers, params={"limit":limit,
                                                               "offset":offset})
            items += result.json().get("items",[])
            offset += limit

        tracks_df = self.etl.jsonToDf(file_name=TRACKS, proc_what='tracks',
                             result={"items":items})
        return tracks_df
    
    def get_artists(self, tracks_df: pd.DataFrame):
        # # empty string to append to for when I pull multiple artists
        # artist_ids = ""
        # for i in tracks_df.index:
        #     artist_ids += f'{tracks_df.loc[i, 'artist_id']},'
        # # seting string to exclude the last character(it ends with a comma)
        # artist_ids = artist_ids[:-1]
        
        # # request artists info with GET and turn results into JSON
        # artist_url = f"https://api.spotify.com/v1/artists?ids={artist_ids}"
        # result = requests.get(artist_url, headers=self.headers)
        
        # turning pandas column into a list
        ids = list(tracks_df['artist_id'])

        # chunks is going to batch 50 artists per an API call
        # and use yield to store that batch into memory to be written
        # into artists
        def chunks(lst:list, n:int):
            for i in range(0, len(lst), n):
                yield lst[i:i+n]
        
        # empty list to store all artists objects after each API call
        all_artists = []

        for batch in chunks(ids,50):
            #join the list elements via a comma in a string
            artist_ids = ','.join(batch)
            result = requests.get("https://api.spotify.com/v1/artists",
                                  headers=self.headers, params={
                                      "ids":artist_ids
                                  })
            # turn each result into json/dict, grab the artists key
            # then extend the result to list artists
            all_artists.extend(result.json().get("artists",[]))

        artists_df = self.etl.jsonToDf(file_name = ARTISTS, proc_what='artists',
                                result={"artists":all_artists})
        return artists_df
    
    def get_albums(self, tracks_df:pd.DataFrame):
        # # empty string to append to for when I pull multiple albums
        # album_ids_1 = ""
        # album_ids_2 = ""
        # album_ids_3 = ""
        # for i in tracks_df.index:
        #     if i > 0 and i <= 19:
        #         album_ids_1 += f"{tracks_df.loc[i, 'album_id']},"
        #     elif i >= 20 and i <= 39:
        #         album_ids_2 += f"{tracks_df.loc[i, 'album_id']},"
        #     else:
        #         album_ids_3 += f"{tracks_df.loc[i, 'album_id']},"
        # album_ids_1 = album_ids_1[:-1]
        # album_ids_2 = album_ids_2[:-1]
        # album_ids_3 = album_ids_3[:-1]
        # # request album endpoint and turn JSON to df
        # # we have to append the results and make multiple calls due to 20 LIMIT max 
        # album_url_1 = f"https://api.spotify.com/v1/albums?ids={album_ids_1}"
        # album_url_2 = f"https://api.spotify.com/v1/albums?ids={album_ids_2}"
        # album_url_3 = f"https://api.spotify.com/v1/albums?ids={album_ids_3}"
        # result_1 = requests.get(album_url_1,headers=self.headers)
        # result_2 = requests.get(album_url_2,headers=self.headers)
        # result_3 = requests.get(album_url_3,headers=self.headers)
        # album_df = pd.concat(
        #     [
        #         self.etl.jsonToDf(file_name=ALBUMS, proc_what='albums', result=result_1),
        #         self.etl.jsonToDf(file_name=ALBUMS, proc_what='albums', result=result_2),
        #         self.etl.jsonToDf(file_name=ALBUMS, proc_what='albums', result=result_3),
        #     ], ignore_index=True
        # )

        # turning pandas column into a list
        ids = list(tracks_df['album_id'])

        # chunks is going to yield 20 id's per loop
        def chunks(lst:list,n:int):
            for i in range(0,len(lst),n):
                yield lst[i:i+n]
        
        # this list will store all album objects per api call
        all_albums = []

        for batch in chunks(ids,20):
            album_ids = ','.join(batch)

            result = requests.get("https://api.spotify.com/v1/albums",
                                  headers=self.headers, params={"ids":album_ids})
            all_albums.extend(result.json().get("albums",[]))

        album_df = self.etl.jsonToDf(ALBUMS,'albums',result={"albums":all_albums})

        return album_df