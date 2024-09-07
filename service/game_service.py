from . import bind_service, car_service
import json

def game_in(play_id, game_id, car_id, rc_id, mqtt, redis):
    game_bind("1", play_id, game_id, car_id, rc_id, mqtt, redis)

def game_out(play_id, game_id, car_id, rc_id, mqtt, redis):
    game_bind("0", play_id, game_id, car_id, rc_id, mqtt, redis)



#type 0-unbind 1-bind
def game_bind(type, play_id, game_id, car_id, rc_id, mqtt, redis):
    bind_data = {
        "rc": rc_id,
        "game": game_id
    }
    bind_service.bind(type, bind_data, mqtt)
    car_info_redis = {
        "game_id": game_id,
        "game_name": f"game{game_id}"
    }
    car_status = "2"
    if type != "1":
        car_info_redis = {
            "game_id": "-",
            "game_name": "-"
        }
        car_status = "1"



    add_game(game_id, type, car_id, redis)
    car_service.modify_car_in_redis(car_id, car_info_redis,redis)
    car_service.change_car_status(car_id, car_status, mqtt, redis)

def add_game(game_id, type, car_id, redis):
    time_difference = car_service.get_played_second(car_id, redis)
    game_data = {
        "game_id": game_id,
        "time": time_difference,
        "type": type
    }
    redis.rpush(f'car_id:{car_id}:game_list', json.dumps(game_data))