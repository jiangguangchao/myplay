import json
from config.config import SysConfig
# data 形如 {"car":"1", "rc":"1"}
#type 0-unbind 1-bind
def bind(type, data, mqtt):
    bind = "bind"
    if type != "1":
        bind = "unbind"
    publishMsg = {
        "action":bind,
        "value": data
    }
    for key, value in data.items():
        mqtt.publish_message(f"myplay/{SysConfig.myplayId}/{key}/{value}/receive", json.dumps(publishMsg))