# mqtt_client.py  
import paho.mqtt.client as mqtt

class MqttClient:
    def __init__(self, broker, port, topic_subscribe):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic_subscribe = topic_subscribe
        self.on_message_callback = None

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic_subscribe)

    def on_message(self, client, userdata, msg):
        if self.on_message_callback:
            self.on_message_callback(msg.topic, msg.payload.decode())

    def connect(self):
        print("连接mqtt")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, 60)

    def start(self):
        self.connect()
        self.client.loop_start()

    def publish_message(self, topic, message):
        result = self.client.publish(topic, message)
        status = result[0]
        if status == 0:
            print(f"Message sent to {topic}")
        else:
            print(f"Failed to send message to {topic}")

    def set_message_callback(self, callback):
        self.on_message_callback = callback