from flask import Flask, render_template
import pandas as pd
from lastfm_pull import get_recent_tracks, format_tracks

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


if __name__ == '__main__':
    app.run(debug=True)        