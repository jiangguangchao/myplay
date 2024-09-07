# main_route.py

from flask import jsonify, request
from db import car_db,play_record_db
import json
from datetime import datetime

myplayId = "1"

def init_routes(app, handler):

    @app.route('/carInfo/list')
    def car_info_list():
        car_info = handler.get_all_car_in_redis()
        return jsonify(car_info)
    
    @app.route('/carInfo/energyList')
    def car_energy_list():
        car_id = request.args.get('car_id')
        energy_list = handler.get_car_energy_list(car_id)
        return jsonify(energy_list)

    @app.route('/carInfo/gameList')
    def car_game_list():
        car_id = request.args.get('car_id')
        game_list = handler.get_car_game_list(car_id)
        return jsonify(game_list)

    @app.route('/car/prepare', methods=['POST'])
    def car_prepare():
        # 从请求体中获取 JSON 数据
        data = request.get_json()
        return jsonify(handler.prepare_play(data))

    @app.route('/car/start', methods=['POST'])
    def startPlay():
        data = request.get_json()
        return jsonify(handler.start_play(data))

    @app.route('/car/add', methods=['POST'])
    def add_car():
        data = request.get_json()
        car_db.insert_car(data.get("id"), data.get("name"), data.get("mcu"))
        return "1"

    @app.route('/car/update', methods=['POST'])
    def update_car():
        data = request.get_json()
        car_db.update_car(data.get("id"), data.get("name"), data.get("mcu"))
        return "1"

    @app.route('/car/listAll')
    def listAll_car():
        list = car_db.select_all_cars()
        print(list)
        return jsonify(list)

    @app.route('/car/delete')
    def delete_car():
        id = request.args.get("id")
        car_db.delete_car(id)
        return "1"
