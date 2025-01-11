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

@app.route('/api/pitcher_record/<int:id>', methods=["GET"])
def pitcher_search(id):
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
            'ball_call':"foul" if pitch.foul else ("in_play" if pitch.in_play else("ball" if pitch.ball else ("swinging_strike" if pitch.swinging_strike else "called_strike"))),
            'batter_name':pitch.batter_name_first + " " + pitch.batter_name_last,
            'pitch_result':pitch.pitch_result,
            'description':pitch.description,
            'count':str(pitch.pre_balls) + "-" + str(pitch.pre_strikes),
            'exit_velocity': round(pitch.hit_exit_speed,1) if pitch.hit_exit_speed else None
         })
    return jsonify(sorted(data,key=lambda x: datetime.strptime(x['date'], '%m/%d')));

@app.route('/api/batter_record/<int:id>', methods=["GET"])
def batter_search(id):
    batter_data = db.session.query(PitchData).filter(and_(PitchData.batter_bam_id==id, PitchData.in_play==True))
    data=[];
    for contact in batter_data:
        data.append({
            'launch_angle':contact.hit_vertical_angle,
            'hit_distance':contact.hit_distance,
            'exit_velocity':contact.hit_exit_speed,
            'event_type':contact.event_type,
            'hit_trajectory':contact.hit_trajectory
         })
    return jsonify(data);
    
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

@app.route('/api/batters', methods=["GET"])
def return_batters():
    batter_list = db.session.execute(select(PitchData.batter_bam_id,PitchData.batter_name_last,PitchData.batter_name_first,PitchData.batter_team).distinct()).all()
    data = [];
    for pitcher in batter_list:
        data.append({
            'id':pitcher.batter_bam_id,
            'first_name':pitcher.batter_name_first,
            'last_name':pitcher.batter_name_last,
            'team':pitcher.batter_team
        })
    return jsonify(data);

@app.route('/api/batter_discipline/<int:id>', methods=["GET"])
def batter_discipline(id):
    discipline_data = db.session.query(PitchData).filter((PitchData.batter_bam_id==id))
    data=[];
    for instance in discipline_data:
        data.append({
            'plate_x':instance.plate_x,
            'plate_z':instance.plate_z,
            'swinging_strike':instance.swinging_strike,
            'swing': instance.swing,
            'contact': instance.contact
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
                                        func.sum(PitchData.swinging_strike).label('whiffs'),
                                        func.sum(PitchData.chase).label('chases'),
                                        func.sum(case((PitchData.in_zone,0), else_=1)).label('out_zone')
                                        ).where((PitchData.pitcher_bam_id==id)&(PitchData.is_pitch)).group_by(PitchData.pitch_type)).all()
    data=[];
    for category in pitcher_data:
         data.append({
            'Chase %': 'N/A' if (category.out_zone is None or category.out_zone == 0) else (0 if (category.chases is None or category.chases == 0) else round(100*category.chases/category.out_zone,1)),
            'Whiff %':'N/A' if (category.swings is None or category.swings == 0) else (0 if (category.whiffs is None or category.whiffs == 0) else round(100*category.whiffs/category.swings,1)),
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
