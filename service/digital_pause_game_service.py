import json
from config.config import SysConfig,DigitalPauseConfig

def pause_num(play_id,car_id, rc_id, game_id, num, mqtt):
    message = {
        "action": "unluck"
    }
    if num == DigitalPauseConfig.luck_num:
        message = {
            "action": "luck",
            "value": DigitalPauseConfig.award_energy
        }
    mqtt.publish_message(f"myplay/{SysConfig.myplayId}/game/{game_id}/receive", json.dumps(message))




