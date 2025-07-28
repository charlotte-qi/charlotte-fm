from flask import Flask, render_template
import pandas as pd
from lastfm_pull import get_recent_tracks, format_tracks
from insight_utils import add_genre_column

app = Flask (__name__)

@app.route('/')
def index():
    raw = get_recent_tracks()
    if 'recenttracks' in raw:
        tracks = raw['recenttracks']['track']
        df = format_tracks(tracks)
        print(df.head())
        if not df.empty:
            top_artists = df['Artist'].value_counts().head(5).reset_index()
            top_artists.columns = ['Artist', 'Plays']
            table_html = top_artists.to_html(classes='data', index=False)
        else:
            table_html = "<p>No data available.</p>"
    else:
        table_html = "<p>Error fetching data.</p>"

    return render_template('index.html', table=table_html)

@app.route('/insights')
def insights():
    raw = get_recent_tracks()
    if 'recenttracks' in raw:
        tracks = raw['recenttracks']['track']
        df = format_tracks(tracks)
        df_with_genre = add_genre_column(df)
        top_genres = df_with_genre['Genre'].value_counts().head(5).reset_index()
        top_genres.columns = ['Genre', 'Plays']
        table_html = top_genres.to_html(classes = 'data', index=False)
    else:
        table_html = "<p>Error fetching genre data.</p>"
    
    return render_template('insights.html', genre_table=table_html)

if __name__ == '__main__':
    app.run(debug=True)        