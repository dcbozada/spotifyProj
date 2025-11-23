import pandas as pd #type:ignore
import json
from sqlalchemy import create_engine #type:ignore

class ETL():
    def __init__(self):
        self.file_name = "my_tracks.json"
        self.tracks_dict = {}
        self.tracks_df = None

    def jsonToDf(self) -> pd.DataFrame:
        # read the tracks json file
        with open(self.file_name, 'r') as f:
            tracks = json.load(f)
        
        # extract only the track_id, track_name, artist_id, album_id, 
        # and duration_ms from json file and put it into self.tracks_dict
        for i in range(len(tracks['items'])):
            self.tracks_dict.update({
                i:{
                    'track_id':tracks['items'][i]['track']['id'],
                    'track_name':tracks['items'][i]['track']['name'],
                    'artist_id':tracks['items'][i]['track']['artists'][0]['name'],
                    'album_id':tracks['items'][i]['track']['album']['id'],
                    'duration_ms':tracks['items'][i]['track']['duration_ms']
                }
            })
        
        # turn self.tracks_dict into a dataframe
        # have to tranpose because the keys of each dict are originally the rows
        self.tracks_df = pd.DataFrame(self.tracks_dict).T

        return self.tracks_df
    
def main():
    etl = ETL()
    tracks_df = etl.jsonToDf()
    print(tracks_df)

    # connect to local postgres DB
    engine = create_engine("postgresql://dylan:wooli@localhost:5432/spotify")

    tracks_df.to_sql("tracks", engine, if_exists="replace", index=False)



if __name__ == "__main__":
    main()



