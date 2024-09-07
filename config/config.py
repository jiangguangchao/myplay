# MQTT 配置块
class MQTTConfig:
    BROKER = "localhost"
    PORT = 1883
    TOPIC_SUBSCRIBE = "myplay/1/#"
    TOPIC_PUBLISH = "test/response/mqtt"

# MySQL 配置块
class MySQLConfig:
    HOST = "localhost"
    PORT = 3306
    USER = "root"
    PASSWORD = "password"
    DB = "mydatabase"

class RedisConfig:
    HOST = "localhost"
    PORT = 6379
    DB=1

class SysConfig:
    myplayId = "1"

class DigitalPauseConfig:
    luck_num = 99
    award_energy = 2