from service import car_service
from model.CarPlay import CarPlay
from db import play_record_db
from config.config import SysConfig
import json
from datetime import datetime

def prepare_play(data,mqtt, redis):

    # 解析数据
    rc_id = data.get('rc_id')
    car_id = data.get('car_id')
    play_time = data.get('play_time')
    total_energy = 0

    play_id = datetime.now().strftime('%Y%m%d%H%M%S')
    car_status = '0'
    car_play = CarPlay(play_id, SysConfig.myplayId, car_id, rc_id, None, None, play_time, total_energy, 0, car_status)
    play_record_db.insert_play(car_play)

    data_in_redis = {
        "play_id": play_id,
        "rc_id": rc_id,
        "play_time": play_time,
        "energy": 0,#当前能量值
        "total_energy":total_energy,#获得的总能量
        "used_energy":0, #使用的总能量
        "car_status": car_status #-1：未开始 0：准备中  1：进行中  2：暂停
    }
    publishMsg = {
        "action":"bind",
        "value": data_in_redis
    }
    mqtt.publish_message(f"myplay/{SysConfig.myplayId}/car/{car_id}/receive", json.dumps(publishMsg))
    mqtt.publish_message(f"myplay/{SysConfig.myplayId}/rc/{rc_id}/receive", json.dumps(publishMsg))

    car_service.modify_car_in_redis(car_id, data_in_redis, redis)

    # 返回响应
    return data_in_redis

def start_play(data, mqtt, redis):
    rc_id = data.get('rc_id')
    car_id = data.get('car_id')
    play_id = data.get('play_id')
    play_time = data.get('play_time')
    car_status = "1"
    publishMsg = {
        "action":"start",
        "value": {
            "car_status": car_status,#-1：未开始 0：准备中  1：进行中  2：暂停
            "play_time": play_time
        }
    }
    mqtt.publish_message(f"myplay/{SysConfig.myplayId}/car/{car_id}/receive", json.dumps(publishMsg))
    mqtt.publish_message(f"myplay/{SysConfig.myplayId}/rc/{rc_id}/receive", json.dumps(publishMsg))

    start_time = datetime.now()
    start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    car_play = CarPlay(play_id=play_id,start_time=start_time, play_time= play_time,status=car_status)
    play_record_db.update_play(car_play)

    returnData = {
        "car_status": car_status,
        "play_time": play_time,
        "start_time": start_time_str
    }
    car_service.modify_car_in_redis(car_id, returnData, redis)
    return returnData


def end_play(data, redis):
    play_id = data['play_id']
    car_id = data['car_id']

    car_in_redis = car_service.get_car_in_redis(car_id,redis)
    car_play = CarPlay(play_id=play_id,total_energy=car_in_redis["total_energy"],
                       used_energy=car_in_redis["used_energy"], status='10')
    play_record_db.update_play(car_play)
    car_service.redset_car_in_redis(car_id, redis)