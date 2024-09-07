import os
from flask import Flask
from flask_cors import CORS
from mqtt_client import MqttClient
from route import main_route  # 导入 routes 模块
from config.config import MQTTConfig, MySQLConfig,RedisConfig
from handler import Handler
from schedule import task_schedule
import redis
import json


# 创建 Flask 实例
app = Flask(__name__)
CORS(app)  # 这将允许所有域名的跨域请求

mqtt_client = MqttClient(MQTTConfig.BROKER, MQTTConfig.PORT, MQTTConfig.TOPIC_SUBSCRIBE)
redis_client = redis.Redis(host=RedisConfig.HOST, port=RedisConfig.PORT, db=RedisConfig.DB)
handler = Handler(mqtt_client,redis_client)
mqtt_client.set_message_callback(handler.handle_message)

# 初始化路由
main_route.init_routes(app, handler)
handler.clean_redis()
handler.add_all_car_to_redis()

task_schedule.init_scheduler(app)
task_schedule.history_statistics();#每次启动都对历史数据做一个统计

if __name__ == '__main__':
    print('启动服务器。。。。。。。。。。。。。。。。')

    # 启动 MQTT 客户端
    mqtt_client.start()

    # 启动 Flask 应用
    app.run(host='localhost', port=5000, debug=True, use_reloader=False)