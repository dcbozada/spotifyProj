import pandas as pd #type:ignore
import json
from sqlalchemy import create_engine, text #type:ignore

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

    # connect to local postgres DB
    engine = create_engine("postgresql://dylan:wooli@localhost:5432/spotify")

    # testing connection to database 'spotify'
    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT 1'))
            print("Successful connection to 'spotify': ", result.scalar())
    except Exception as e:
        print("Failed Connection to 'spotify'", e)

    # creating the table 'tracks'
    create_tracks_table_sql = """
    CREATE TABLE IF NOT EXISTS tracks (
    track_id VARCHAR PRIMARY KEY,
    track_name VARCHAR,
    artist_id VARCHAR, 
    album_id VARCHAR, 
    duration_ms INT 
    );"""
    with engine.connect() as conn:
        conn.execute(text(create_tracks_table_sql))
        conn.commit()
    print("Table 'tracks' created")

    # inserting tracks_df into table 'tracks'
    # no need to commit because sqlalchemy to_sql() is in autocommit mode
    # opens temp connection, executes the INSERT statements, auto commits, closes connection
    tracks_df.to_sql("tracks", engine, if_exists='replace', index=False)

    # testing to see if tracks loaded
    with engine.connect() as conn:
        # using engine.connect().execute()
        # yields sqlalchemy CursorResult object
        # that needs to printed with a "for row in result" as if you were trying
        # view a "SELECT * FROM tracks"
        result = conn.execute(text("SELECT COUNT(*) FROM tracks"))
        for row in result:
            print(row)
        # using "pd.read_sql(query, connection)" reads the result into a 
        # pandas DataFrame
        test = pd.read_sql("SELECT COUNT(*) FROM tracks", engine)
        print(test)






if __name__ == "__main__":
    main()



