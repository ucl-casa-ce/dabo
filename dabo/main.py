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
sim_seconds = hour*3600 + minute*60 + second

while True:
    for device_id, info in devices.items():
        profile    = info["sensors"]
        root_topic = info["root_topic"]
        topic      = f"{root_topic}/{device_id}"

        # derive H:M:S for downstream generators
        H, rem  = divmod(sim_seconds % 86400, 3600)
        M, S    = divmod(rem, 60)

        data = generate_data(device_id, profile, H, M, S)
        publisher.publish(device_id=topic, data=data)

    time.sleep(frequency)

    # advance simulation
    sim_seconds = (sim_seconds + int(frequency * realtime_multiplier)) % 86400

    # pretty print
    H, rem = divmod(sim_seconds, 3600)
    M, S   = divmod(rem, 60)
    print(f"{H:02}:{M:02}:{S:02}")