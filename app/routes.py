from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.models import PitchData
from datetime import datetime, timezone, date
from sqlalchemy.sql import func
from sqlalchemy import select, and_
import json;
import sys;

@app.route('/')
def root():
    return send_from_directory('../client/dist','index.html')

# Path for the rest of the static files (JS/CSS)
@app.route('/<path:path>')
def assets(path):
    return send_from_directory('../client/dist', path)

#Use @dataclass for returning JSON https://www.reddit.com/r/flask/comments/vll4xu/af_how_to_turn_flask_sqlalchemy_query_results/

#get pitch data for every player
# @app.route('/api/player_record/<int:id>', methods=["GET"])
# def player_search(id):
#     pitcher_data = db.session.execute(select(PitchData.game_date, func.sum(PitchData.is_pitch).label('total_pitches')).where(PitchData.pitcher_bam_id==id).group_by(PitchData.game_bam_id,PitchData.game_date)).all()
#     data=[];
#     for appearance in pitcher_data:
#          data.append({
#             'date':appearance.game_date.split("-")[1]+"/"+appearance.game_date.split("-")[2],
#             'pitches':appearance.total_pitches
#          })
#     print(data,file=sys.stderr)
#     return jsonify(sorted(data,key=lambda x: datetime.strptime(x['date'], '%m/%d')));

@app.route('/api/player_record/<int:id>', methods=["GET"])
def player_search(id):
    # pitcher_data = db.session.execute(select(PitchData).where((PitchData.pitcher_bam_id == id) & (PitchData.is_pitch==True))).all()
    pitcher_data = db.session.query(PitchData).filter(and_(PitchData.pitcher_bam_id==id, PitchData.is_pitch==True))
    data=[];
    for pitch in pitcher_data:
        data.append({
            'date':pitch.game_date.split("-")[1]+"/"+pitch.game_date.split("-")[2],
            'plate_x':pitch.plate_x,
            'plate_z':pitch.plate_z,
            'swing':pitch.swing,
            'swinging_strike':pitch.swinging_strike,
            'chase':pitch.chase,
            'in_zone':pitch.in_zone,
            'pitch_type':pitch.pitch_type
         })
    # print(data,file=sys.stderr)
    return jsonify(sorted(data,key=lambda x: datetime.strptime(x['date'], '%m/%d')));
    
#gather list of Padres pitchers
@app.route('/api/pitchers', methods=["GET"])
def return_pitchers():
    pitcher_list = db.session.execute(select(PitchData.pitcher_bam_id,PitchData.pitcher_name_last,PitchData.pitcher_name_first).where(PitchData.pitcher_team == "San Diego Padres").distinct()).all()
    data = [];
    for pitcher in pitcher_list:
        data.append({
            'id':pitcher.pitcher_bam_id,
            'first_name':pitcher.pitcher_name_first,
            'last_name':pitcher.pitcher_name_last,
        })
    # print(data,file=sys.stderr)
    return jsonify(data);

if __name__ == "__main__":
    app.run(debug=True)

'''
Pitcher page
- Game logs (Game, pitches, innings pitched, SOs, BBs, other counting stats) 
- Pitch mix (heatmap/scatterplot, contact/whiff rate, average velo, movement) (GROUP BY pitch_type)
    - ball position: plate_x, plate_z
    - whiff rate = whiff/swings
    - chase rate = chased/balls outside zone (!in_zone)
    - spin_rate, induced_horiz_break, induced_vert_break
- PERHAPS a batted ball profile
'''
#pitch mix (maybe heatmap, contact/swing rate, average velo, movement (rise/drop, horizontal), batted ball profile)
#pitch effectiveness after inning/balls pitched/some time measure
#pitcher vs batter matchup? limited dataset though
'''
How to get individual pitch video
- pull guid
- https://baseballsavant.mlb.com/sporty-videos?playId=<guid from play>
- scrape the video URL from the page
Strike zone: https://umpscorecards.com/explainers/true_strike_zone; strikezone_top, strikezone_bottom
'''
#


# @app.route('/pitch-mix')
# def pitch_mix():
#     return render_template()

# @app.route('/heatmap')
# def heatmap():
#     return render_template()