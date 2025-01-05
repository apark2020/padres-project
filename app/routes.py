from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.models import PitchData
from datetime import datetime, timezone
from sqlalchemy.sql import func
import json;

@app.route('/')
def root():
    return send_from_directory('../client/dist','index.html')

# Path for the rest of the static files (JS/CSS)
@app.route('/<path:path>')
def assets(path):
    return send_from_directory('../client/dist', path)

#Use @dataclass for returning JSON https://www.reddit.com/r/flask/comments/vll4xu/af_how_to_turn_flask_sqlalchemy_query_results/

@app.route('/player_search/<string:last_name>', methods=["GET"])
def player_search(last_name):
    pitcher = db.session.query(func.avg(PitchData.rel_speed)).filter_by(pitcher_name_last=last_name).scalar()
    return str(pitcher);

if __name__ == "__main__":
    app.run(debug=True)

#pitch mix (maybe heatmap, contact/swing rate)
#pitch effectiveness after inning/balls pitched/some time measure
#pitcher vs batter matchup? limited dataset though
'''
How to get individual pitch video
- pull guid
- https://baseballsavant.mlb.com/sporty-videos?playId=<guid from play>
- scrape the video URL from the page
'''


# @app.route('/pitch-mix')
# def pitch_mix():
#     return render_template()

# @app.route('/heatmap')
# def heatmap():
#     return render_template()