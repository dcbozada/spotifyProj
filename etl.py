import pandas as pd #type:ignore
import json
from sqlalchemy import create_engine, text #type:ignore
import requests #type:ignore

class ETL():    
    def __init__(self):
        # for listening history processing
        self.history_dict = {}
        self.history_df = None
        # for tracks processing
        # self.tracks_file_name = "tracks.json"
        self.tracks_dict = {}
        self.tracks_df = None
        # for artists process
        self.artists_dict = {}
        self.artists_df = None
        # for albumbs process
        self.albums_dict = {}
        self.albums_df = None
    
    # creating this writeJson func because I am going to use it a few times
    ''' Never call to this directly in main()
       it is embedded into jsonToDF() '''
    def w_result_to_json(self, result: requests.models.Response | dict, file_name:str) -> str:
        # turn the requests.models.Response to json so python reads as dict
        if type(result) == requests.models.Response:
            result = result.json()
        # write json'd result to file_name
        with open(file_name, 'w') as f:
            json.dump(result, f, indent=4)     
        return result

    def jsonToDf(self, file_name: str, proc_what: str, result: requests.models.Response | dict) -> pd.DataFrame:
        # first we are going to write the Response to json
        result = self.w_result_to_json(result=result, file_name=file_name)
        # code that will process the listening history end point
        if proc_what == 'history':
            # extract track_uri, track_id, played_at, context_type, context_uri
            self.history_dict = {
                idx: {
                    "played_at": item.get("played_at", "n/a"),
                    "track_id": (item.get("track") or {}).get("id", "n/a"),
                    "context_type": (item.get("context") or {}).get("type", "n/a"),
                    "context_uri": (item.get("context") or {}).get("uri", "n/a")
                }
                for idx,item in enumerate(result.get("items") or [])
            }
            # turn history_dict into history_df
            self.history_df = pd.DataFrame(self.history_dict).T
            return self.history_df
        # code that will process the tracks endpoints 
        elif proc_what == 'tracks':
            # extract only the track_id, track_name, artist_id, album_id, 
            # and duration_ms from json file and put it into self.tracks_dict
            self.tracks_dict = {
                idx: {
                    "track_id": (item.get("track") or {}).get("id", "n/a"),
                    "track_name": (item.get("track") or {}).get("name", "n/a"),
                    "artist_id": ((item.get("track") or {}).get("artists") or [{}])[0].get("id", "n/a"),
                    "album_id": ((item.get("track") or {}).get("album") or {}).get("id", "n/a"),
                    "duration_ms": (item.get("track") or {}).get("duration_ms", "n/a"),
                    "added_at": item.get("added_at", "n/a")
                }
                for idx, item in enumerate(result.get("items") or [])
            }
            # turn self.tracks_dict into a dataframe
            # have to tranpose because the keys of each dict are originally the rows
            self.tracks_df = pd.DataFrame(self.tracks_dict).T
            return self.tracks_df
        # code that will process the artists endpoint
        elif proc_what == 'artists':
            # extract only the artist_id, artist_name, artist_genre,
            # artist_follwers, artist_popularity
            self.artists_dict = {
                idx: {
                    "artist_id": item.get("id", "n/a"),
                    "artist_name": item.get("name", "n/a"),
                    "artist_genre": (item.get("genres") or ["n/a"])[0],
                    "artist_followers": (item.get("followers") or {}).get("total", "n/a"),
                    "artist_popularity": item.get("popularity", "n/a")
                }
                for idx,item in enumerate(result.get("artists") or [])
            }
            self.artists_df = pd.DataFrame(self.artists_dict).T
            return self.artists_df
        # code to process albums
        elif proc_what == 'albums':
            # extract only the album_id, name,
            # release_date, album_type, total_tracks, 
            # image_url
            self.albums_dict = {
                idx: {
                    "album_id":item.get("id","n/a"),
                    "name":item.get("name","n/a"),
                    "release_date":item.get("release_date","n/a"),
                    "album_type":item.get("album_type","n/a"),
                    "total_tracks":item.get("total_tracks","n/a"),
                    "image_url":(item.get("images") or ["n/a"])[0].get("url","n/a")
                }
                for idx, item in enumerate(result.get("albums") or [])
            }
            self.albums_df = pd.DataFrame(self.albums_dict).T
            return self.albums_df