# handler.py
import redis
from datetime import datetime
import json
import math
from service import car_service, game_service, play_service

myplayId = "1"
luck_num = 99
award_num =2
class Handler:

    #{"action":"add_energy","value":{"play_id":"","car_id":"1","rc_id":"1","num":3,"source":"1"}}
    #{"action":"nfc","value":{"play_id":"","car_id":"1","rc_id":"1", "nfc_id":"abc"}}
    #{"action":"game_end","value":{"play_id":"","car_id":"1","rc_id":"1","game_id":"1"}}
    #{"action":"end","value":{"play_id":"","car_id":"1"}}

    def __init__(self, mqtt_client,redis_client):
        self.mqtt_client = mqtt_client
        self.redis_client = redis_client
        self.car_id_list = []
        self.nfc_game = {
            "abc":"1"
        }


    def handle_message(self, topic, message):
        # 处理接收到的消息
        print(f"收到mqtt消息 topic: {topic},  message: {message}")

        message_data = json.loads(message)
        action = message_data['action']
        if action == "add_energy":
            self.add_energy(message_data['value'])
        elif action == "end":
            self.end_play(message_data['value'])
        elif action == "nfc" :
            self.handle_nfc(message_data['value'])
        elif action == "game_end":
            self.game_out(message_data['value']['play_id'],
                           message_data['value']['game_id'], message_data['value']['car_id'],
                           message_data['value']['rc_id'])


    def publishMsg(self, topic, message):
        self.mqtt_client.publish_message(topic, message)


    def add_all_car_to_redis(self):
        car_service.add_all_car_to_redis(self.redis_client)

    def add_car_to_redis(self, car_id, data):
        car_service.add_car_to_redis(car_id, data, self.redis_client)

    def modify_car_in_redis(self, car_id, data):
        self.add_car_to_redis(car_id, data)

    def del_play_in_redis(self, car_id):
        self.redis_client.delete(f'car_id:{car_id}')

    def get_all_car_in_redis(self):
        return car_service.get_all_car_in_redis(self.redis_client)

    def get_car_in_redis(self, car_id):
        return car_service.get_car_in_redis(car_id, self.redis_client)

    def clean_redis(self):
        car_service.clean_redis(self.redis_client)

    def redset_car_in_redis(self, car_id):
        car_service.redset_car_in_redis(car_id, self.redis_client)

    def get_car_energy_list(self, car_id):
        return car_service.get_car_energy_list(car_id, self.redis_client)

    def get_car_game_list(self, car_id):
        return car_service.get_car_game_list(car_id, self.redis_client)
    
    def add_energy(self, data):
        return car_service.add_energy(data, self.redis_client)


    def prepare_play(self, data):
        return play_service.prepare_play(data, self.mqtt_client, self.redis_client)
    def start_play(self, data):
        return play_service.start_play(data, self.mqtt_client, self.redis_client)

    def end_play(self, data):
        play_service.end_play(data, self.redis_client)
        # play_id = data['play_id']
        # car_id = data['car_id']
        #
        # car_in_redis = self.get_car_in_redis(car_id)
        # car_play = CarPlay(play_id=play_id,total_energy=car_in_redis["total_energy"],
        #                    used_energy=car_in_redis["used_energy"], status='10')
        # car_play_db.update_car_play2(car_play)
        #
        # self.redset_car_in_redis(car_id)

    def handle_nfc(self, data):
        nfc_id = data['nfc_id']
        car_id = data['car_id']
        rc_id = data['rc_id']
        play_id = data['play_id']
        game_id = self.nfc_game[nfc_id]

        self.game_in(play_id, game_id, car_id, rc_id)

    def game_in(self, play_id, game_id, car_id, rc_id):
        game_service.game_in(play_id,game_id, car_id, rc_id, self.mqtt_client, self.redis_client)

    def game_out(self, play_id, game_id, car_id, rc_id):
        game_service.game_out(play_id,game_id, car_id, rc_id, self.mqtt_client, self.redis_client)

    def digital_game_pause_num(self, car_id, rc_id, game_id, num, mqtt_client):
        if num == luck_num:
            message = {
                "action": "do_add_energy",
                "value": award_num
            }
            mqtt_client.publish_message(f"myplay/{myplayId}/game/{game_id}/receive", json.dumps(message))



















