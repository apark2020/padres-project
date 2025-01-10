from flask import render_template, flash, redirect, url_for, request, send_from_directory, jsonify
from urllib.parse import urlsplit
import sqlalchemy as sa
from app import app, db
from app.models import PitchData
from datetime import datetime, timezone, date
from sqlalchemy.sql import func
from sqlalchemy import select, and_, case, distinct, tuple_, or_, within_group
import json;
import sys;

@app.route('/')
def root():
    return send_from_directory('../client/dist','index.html')

# Path for the rest of the static files (JS/CSS)
@app.route('/<path:path>')
def assets(path):
    return send_from_directory('../client/dist', path)

@app.route('/api/player_record/<int:id>', methods=["GET"])
def player_search(id):
    pitcher_data = db.session.query(PitchData).filter(and_(PitchData.pitcher_bam_id==id, PitchData.is_pitch==True))
    data=[];
    for pitch in pitcher_data:
        data.append({
            'pitcher_id':id,
            'date':pitch.game_date.split("-")[1]+"/"+pitch.game_date.split("-")[2],
            'plate_x':pitch.plate_x,
            'plate_z':pitch.plate_z,
            'swing':pitch.swing,
            'swinging_strike':pitch.swinging_strike,
            'called_strike':pitch.called_strike,
            'chase':pitch.chase,
            'in_zone':pitch.in_zone,
            'pitch_type':pitch.pitch_type,
            'induced_vert_break':pitch.induced_vert_break,
            'horz_break':pitch.horz_break,
            'batter_side':pitch.batter_side,
            'rel_speed':round(pitch.rel_speed,1),
            'guid':pitch.guid,
            'ball_call':"ball" if pitch.ball else ("swinging_strike" if pitch.swinging_strike else "called_strike"),
            'batter_name':pitch.batter_name_first + " " + pitch.batter_name_last,
            'pitch_result':pitch.pitch_result,
            'description':pitch.description,
            'count':str(pitch.pre_balls) + "-" + str(pitch.pre_strikes),
            'exit_velocity': round(pitch.hit_exit_speed,1) if pitch.hit_exit_speed else None
         })
    return jsonify(sorted(data,key=lambda x: datetime.strptime(x['date'], '%m/%d')));
    
@app.route('/api/pitchers', methods=["GET"])
def return_pitchers():
    pitcher_list = db.session.execute(select(PitchData.pitcher_bam_id,PitchData.pitcher_name_last,PitchData.pitcher_name_first,PitchData.pitcher_team).distinct()).all()
    data = [];
    for pitcher in pitcher_list:
        data.append({
            'id':pitcher.pitcher_bam_id,
            'first_name':pitcher.pitcher_name_first,
            'last_name':pitcher.pitcher_name_last,
            'team':pitcher.pitcher_team
        })
    return jsonify(data);

@app.route('/api/player_pitch_data/<int:id>', methods=["GET"])
def player_pitch_type_data(id):
    pitcher_data = db.session.execute(select(
                                        PitchData.pitch_type, 
                                        func.avg(PitchData.rel_speed).label('MPH'),
                                        func.avg(PitchData.hit_exit_speed).label('EV'),
                                        func.sum(case((PitchData.event_type == "strikeout", 1), else_=0)).label('SO'),
                                        func.avg(PitchData.spin_rate).label('Spin'),
                                        func.sum(case((or_(PitchData.event_type == "single",PitchData.event_type == "double",PitchData.event_type == "triple",PitchData.event_type == "home_run"), 1), else_=0)).label('Hits'),
                                        func.sum(PitchData.swing).label('swings'),
                                        func.sum(PitchData.swinging_strike).label('whiffs')
                                        ).where((PitchData.pitcher_bam_id==id)&(PitchData.is_pitch)).group_by(PitchData.pitch_type)).all()
    data=[];
    for category in pitcher_data:
         data.append({
            'Whiff':'N/A' if (category.swings is None or category.swings == 0) else (0 if (category.whiffs is None or category.whiffs == 0) else round(100*category.whiffs/category.swings,1)),
            'Spin':int(category.Spin),
            'Hits':category.Hits,
            'SO':category.SO,
            'EV': 'N/A' if (category.EV is None or category.EV == 0) else round(category.EV,1),
            'MPH':round(category.MPH,1),
            'pitch_type':category.pitch_type,
         })
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