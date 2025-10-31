import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv

load_dotenv()

class MQTTPublisher:
    def __init__(self):
        self.broker = os.getenv('BROKER_ADDRESS')
        self.port = int(os.getenv('BROKER_PORT'))
        self.username = os.getenv('MQTT_USERNAME')
        self.password = os.getenv('MQTT_PASSWORD')
        self.root_topic = os.getenv('MQTT_TOPIC')
        self.client = mqtt.Client()
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker, self.port)

    def publish(self, device_id, data):
        topic = f"{self.root_topic}/{device_id}"
        self.client.publish(topic, json.dumps(data))