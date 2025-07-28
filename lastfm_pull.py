import requests
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

import os
API_KEY = os.environ["LASTFM_API_KEY"]
USERNAME = os.environ["LASTFM_USERNAME"]

def get_recent_tracks(limit=100):
    url = 'http://ws.audioscrobbler.com/2.0/'
    params = {
        'method': 'user.getrecenttracks',
        'user': USERNAME,
        'api_key': API_KEY,
        'format':'json',
        'limit': limit
    }
    r = requests.get(url, params=params)
    data = r.json()
    print(data)
    return data

def format_tracks(tracks):
    rows = []
    for t in tracks:
        track = t['name']
        artist = t['artist']['#text']
        album = t['album']['#text']
        date = t.get('date',{}).get('#text', 'Now Playing')
        rows.append([track, artist, album, date])
    df = pd.DataFrame(rows, columns=['Track', 'Artist', 'Album', 'Date'])
    return df

raw_data = get_recent_tracks()
print(raw_data)

if 'recenttracks' in raw_data:
    tracks = raw_data['recenttracks']['track']
    df = format_tracks(tracks)
    print(df.head())
else:
    print("API not working")