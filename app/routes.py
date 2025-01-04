from flask import render_template, flash, redirect, url_for, request
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.models import PitchData
from datetime import datetime, timezone

@app.route('/')
def index():
    pitcher = db.session.scalar(sa.select(PitchData).where(PitchData.pitcher_name_last == "Cease"))
    return render_template('index.html',pitcher=pitcher)

#pitch mix (maybe heatmap, contact/swing rate)
#pitch effectiveness after inning/balls pitched/some time measure
#pitcher vs batter matchup? limited dataset though
'''
How to get individual pitch video
- pull guid
- https://baseballsavant.mlb.com/sporty-videos?playId=<guid from play>
- scrape the video URL from the page
'''


@app.route('/pitch-mix')
def pitch_mix():
    return render_template()

@app.route('/heatmap')
def heatmap():
    return render_template()