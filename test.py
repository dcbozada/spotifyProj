import pandas as pd
import json

with open('artists.json', 'r') as f:
    artists = json.load(f)
genre = (artists['artists'][5].get('genres') or ['No Genre specified'])[0]
print(genre)
print(type(artists))
print(type(artists['artists']))
print(type(artists['artists'][6]))