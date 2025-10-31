from mqtt_publisher import MQTTPublisher
from data_generator import load_device_definitions_from_template, generate_data
import time
import os
from dotenv import load_dotenv
import json

load_dotenv()

publisher = MQTTPublisher()
frequency = int(os.getenv('FREQUENCY'))
realtime_multiplier = float(os.getenv('REALTIME_MULTIPLIER'))

# Load device definitions with root_topic included
def load_device_definitions_with_topic(template_path):
    with open(template_path, "r") as f:
        template = json.load(f)

    devices = {}
    for device in template:
        device_type = device["device_type"]
        count = device["count"]
        sensors = device["sensors"]
        root_topic = device.get("root_topic", "default")
        for i in range(1, count + 1):
            device_id = f"{device_type}_{i:02}"
            devices[device_id] = {
                "sensors": sensors,
                "root_topic": root_topic
            }
    return devices

devices = load_device_definitions_with_topic("device_template.json")

hour = 0
minute = 0
second = 0

# Loop to simulate the data and publish on the MQTT broker
while True:
    for device_id, info in devices.items():
        profile = info["sensors"]
        root_topic = info["root_topic"]
        data = generate_data(profile, hour,minute,second)
        topic = f"{root_topic}/{device_id}"
        publisher.publish(device_id=topic, data=data)

    time.sleep(frequency)
    second += (frequency * realtime_multiplier)
    # minute += (frequency * realtime_multiplier) / 60
    if second >= 60:
        minute = (minute + 1) % 60
        second = second %60
    if minute >= 60:
        hour = (hour + 1) % 24
        minute = minute % 60