import pandas as pd #type:ignore
import json
from sqlalchemy import create_engine, text #type:ignore
import requests #type:ignore

class ETL():    
    def __init__(self):
        # right off bat, making ETL class connect to database
        # self.engine = create_engine("postgresql://dylan:wooli@localhost:5432/spotify  ")
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
    
    # creating this writeJson func because I am going to use it a few times
    ''' Never call to this directly in main()
       it is embedded into jsonToDF() '''
    def w_result_to_json(self, result: requests.models.Response, file_name:str) -> str:
        # turn the requests.models.Response to json so python reads as dict
        result = result.json()
        # write json'd result to file_name
        with open(file_name, 'w') as f:
            json.dump(result, f, indent=4)
        return file_name

    def jsonToDf(self, file_name:str, proc_what: str, result: requests.models.Response) -> pd.DataFrame:
        # first we are going to write the Response to json
        file_name = self.w_result_to_json(result=result, file_name=file_name)
        # code that will process the listening history end point
        if proc_what == 'history':
            with open(file_name, 'r') as f:
                history = json.load(f)
            # extract track_uri, track_id, played_at, context_type, context_uri
            self.history_dict = {
                idx: {
                    "id":item["track"].get("uri"),
                    "track_id":item["track"].get("id"),
                    "played_at":item.get("played_at"),
                    "context_type":item["context"].get("type"),
                    "context_uri":item["context"].get("uri")
                }
                for idx,item in enumerate(history.get("items",[]))
            }
            # turn history_dict into history_df
            self.history_df = pd.DataFrame(self.history_dict).T
            return self.history_df
        # code that will process the tracks endpoints 
        elif proc_what == 'tracks':
            # read the json file specified by file_name
            with open(file_name, 'r') as f:
                tracks = json.load(f)
            # extract only the track_id, track_name, artist_id, album_id, 
            # and duration_ms from json file and put it into self.tracks_dict
            self.tracks_dict = {
                idx: {
                    "track_id":item["track"].get("id"),
                    "track_name":item["track"].get("name"),
                    "artist_id":item["track"]["artists"][0].get("id"),
                    "album_id":item["track"]["album"].get("id"),
                    "duration_ms":item["track"].get("duration_ms"),
                    "added_at":item.get("added_at")
                }
                for idx, item in enumerate(tracks.get("items", []))
            }
            # turn self.tracks_dict into a dataframe
            # have to tranpose because the keys of each dict are originally the rows
            self.tracks_df = pd.DataFrame(self.tracks_dict).T
            return self.tracks_df
        # code that will process the artists endpoint
        elif proc_what == 'artists':
            # read the json file specified my file_name
            with open(file_name, 'r') as f:
                artists = json.load(f)
            # extract only the artist_id, artist_name, artist_genre,
            # artist_follwers, artist_popularity
            self.artists_dict = {
                idx: {
                    "artist_id":item.get("id"),
                    "artist_name":item.get("name"),
                    "artist_genre":(item.get('genres') or ['no genre specified'])[0],
                    "artist_followers":item["followers"].get("total"),
                    "artist_popularity":item.get("popularity")
                }
                for idx,item in enumerate(artists.get("artists", []))
            }
            print(f"\n\nFrom jsonToDf proc_what==artists: artists.get('artists', []) is {type(artists.get('artists', []))}\n\n")
            self.artists_df = pd.DataFrame(self.artists_dict).T
            return self.artists_df

    
# def main():
#     etl = ETL()
#     tracks_df = etl.tracks_jsonToDf()

#     # connect to local postgres DB
#     engine = create_engine("postgresql://dylan:wooli@localhost:5432/spotify")

#     # testing connection to database 'spotify'
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text('SELECT 1'))
#             print("Successful connection to 'spotify': ", result.scalar())
#     except Exception as e:
#         print("Failed Connection to 'spotify'", e)

#     # creating the table 'tracks'
#     create_tracks_table_sql = """
#     DROP TABLE IF EXISTS tracks;
#     CREATE TABLE IF NOT EXISTS tracks (
#     track_id VARCHAR PRIMARY KEY,
#     track_name VARCHAR,
#     artist_id VARCHAR, 
#     album_id VARCHAR, 
#     duration_ms INT 
#     );"""
#     with engine.connect() as conn:
#         conn.execute(text(create_tracks_table_sql))
#         conn.commit()
#     print("Table 'tracks' created")

#     # inserting tracks_df into table 'tracks'
#     # no need to commit because sqlalchemy to_sql() is in autocommit mode
#     # opens temp connection, executes the INSERT statements, auto commits, closes connection
#     tracks_df.to_sql("tracks", engine, if_exists='replace', index=False)

#     # testing to see if tracks loaded
#     with engine.connect() as conn:
#         # using engine.connect().execute()
#         # yields sqlalchemy CursorResult object
#         # that needs to printed with a "for row in result" as if you were trying
#         # view a "SELECT * FROM tracks"
#         result = conn.execute(text("SELECT COUNT(*) FROM tracks"))
#         for row in result:
#             print(row)
#         # using "pd.read_sql(query, connection)" reads the result into a 
#         # pandas DataFrame
#         test = pd.read_sql("SELECT COUNT(*) FROM tracks", engine)
#         print(test)


# if __name__ == "__main__":
#     main()



