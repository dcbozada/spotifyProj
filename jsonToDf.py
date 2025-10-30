import pandas as pd
import json 
import os

PATH = 'C:\\Users\\dcboz\\Desktop\\dataEngineer\\spotifyProj\\results.json'

def load_json(file_path) -> dict:
    with open(file_path,'r') as file:
        data = json.load(file)
        # data = json.dumps(data, indent=4)
        return data

dict = load_json(PATH)
print(type(dict['albums']['items']))
print(f'{dict['albums']['items'][0]['artists'][0]['name']}\t{dict['albums']['items'][0]['artists'][1]['name']}')