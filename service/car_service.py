from db import car_db
import json
import math
from datetime import datetime
from config.config import SysConfig

car_id_list = []
def add_car_to_redis(car_id, data, redis):
    pipe = redis.pipeline()
    for key, value in data.items():
        pipe.hset(f'car_id:{car_id}:car_info', key, value)
    pipe.execute()

def modify_car_in_redis(car_id, data, redis):
    add_car_to_redis(car_id, data, redis)

def del_play_in_redis(car_id, redis):
    redis.delete(f'car_id:{car_id}')

def add_all_car_to_redis(redis):
    cars = car_db.select_all_cars()
    for c in cars:
        data = {
            "car_id": c["id"],
            "car_name": c["name"],
            "play_id": "-",
            "rc_id": c['id'],
            "rc_name": f"rc{c['id']}",
            "play_time": "-",
            "start_time": "-",
            "energy": 0,#当前能量值
            "total_energy":0,#获得的总能量
            "used_energy":0, #使用的总能量
            "car_status": "-1", # -1：未开始 0：准备中  1：进行中  2：暂停
            "game_id":"-",
            "game_name":"-",
            "mcu": c["mcu"],
        }
        add_car_to_redis(c["id"], data, redis)
        car_id_list.append(c["id"])

def get_car_in_redis(car_id, redis):
    car_info = redis.hgetall(f'car_id:{car_id}:car_info')
    # Redis的hgetall返回的是字节串，可能需要转换为字符串
    car_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in car_info.items()}
    return car_info

def get_all_car_in_redis(redis):
    car_info_list = []
    for car_id in car_id_list:
        car_info = redis.hgetall(f'car_id:{car_id}:car_info')
        # Redis的hgetall返回的是字节串，可能需要转换为字符串
        car_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in car_info.items()}
        car_info_list.append(car_info)
    return car_info_list


def clean_redis(redis):
    for i in range(100):
        redis.delete(f"car_id:{i}:car_info")
        redis.delete(f"car_id:{i}:energy_list")
        redis.delete(f"car_id:{i}:game_list")

def redset_car_in_redis(car_id, redis):
    data = {
        "play_id": "-",
        "play_time": "-",
        "start_time": "-",
        "energy": 0,#当前能量值
        "total_energy":0,#获得的总能量
        "used_energy":0, #使用的总能量
        "car_status": "-1", # -1：未开始 0：准备中  1：进行中  2：暂停
        "game_id":"-",
        "game_name":"-",
    }
    modify_car_in_redis(car_id, data, redis)
    redis.delete(f"car_id:{car_id}:energy_list")
    redis.delete(f"car_id:{car_id}:game_list")


def get_car_energy_list(car_id, redis):
    list = redis.lrange(f'car_id:{car_id}:energy_list', 0, -1)
    energy_list = [json.loads(item.decode('utf-8')) for item in list]
    return energy_list

def get_car_game_list(car_id, redis):
    list = redis.lrange(f'car_id:{car_id}:game_list', 0, -1)
    game_list = [json.loads(item.decode('utf-8')) for item in list]
    return game_list

def get_played_second(car_id, redis):
    start_time = redis.hget(f'car_id:{car_id}:car_info', "start_time").decode('utf-8')
    # 将日期字符串转换为datetime对象
    date_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    # 获取当前时间
    now = datetime.now()
    # 计算时间差并转换为秒数
    time_difference = int((now - date_obj).total_seconds())
    return time_difference



def change_car_status(car_id, car_status, mqtt, redis):
    data = {
        "car_status": car_status
    }
    modify_car_in_redis(car_id, data, redis)

    publish_msg = {
        "action":"change_status",
        "value": car_status
    }
    mqtt.publish_message(f"myplay/{SysConfig.myplayId}/car/{car_id}/receive", json.dumps(publish_msg))


def add_energy(message, redis):

    play_id = message['play_id']
    car_id = message['car_id']
    rc_id = message['rc_id']
    num = message['num']
    source = message['source']

    car_status = redis.hget(f'car_id:{car_id}:car_info', "car_status").decode('utf-8')

    print(f"小车[{car_id}]状态为{car_status}")
    if car_status != "1" and car_status != "2": #如果不是进行中或者暂停中，就无法增加能量
        print(f"小车[{car_id}]状态不是进行中或者暂停中，无法增加能量")
        return

    
    time_difference = get_played_second(car_id, redis)
    energy_data = {
        "num":num,
        "time": time_difference,
        "source": source
    }
    redis.rpush(f'car_id:{car_id}:energy_list', json.dumps(energy_data))

    redis.hincrby(f'car_id:{car_id}:car_info', 'energy', num)
    if (num > 0):
        redis.hincrby(f'car_id:{car_id}:car_info', 'total_energy', num)
    else:
        redis.hincrby(f'car_id:{car_id}:car_info', 'used_energy', num)