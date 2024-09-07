from flask import jsonify, request
from db import car_db,play_record_db, play_statistics_db
import json
from datetime import datetime

def init_routes(app, handler):


    @app.route('/play/list')
    def play_list():
        play_id = request.args.get('play_id')
        car_id = request.args.get('car_id')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        list = play_record_db.query_play(play_id, car_id, start_time, end_time)
        return jsonify(list)


    @app.route('/playStatc/list')
    def play_statc_list():
        statc_type = request.args.get('statc_type')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        list = play_statistics_db.query_statistics(statc_type, start_time, end_time)
        return jsonify(list)