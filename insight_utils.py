import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ["LASTFM_API_KEY"]

def get_top_tag(artist,track):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'track.gettoptags',
        'artist': artist,
        'track': track,
        'format':'json',
        'api_key': API_KEY
    }
    r = requests.get(url, params=params)
    data = r.json()
    try:
        tags = data['toptags']['tag']
        if tags:
            return tags[0]['name'].lower()
    except:
        return 'unknown'

def add_genre_column(df):
    df = df.copy()
    df['Genre'] = df.apply(lambda row: get_top_tag(row['Artist'], row['Track']), axis=1)
    return df

from insight_utils import add_genre_column
