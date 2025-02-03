import paho.mqtt.client as mqtt
import json
import time
import random
import math
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def generate_dummy_data(room_id, light_status, hour, minute):
    # Simulate temperature as a sine wave over 24 hours with some randomness
    base_temperature = 20 + 5 * math.sin(math.pi * (hour - 6) / 12)  # 20°C average, 5°C amplitude
    temperature = round(base_temperature + random.uniform(-0.5, 0.5), 2)  # Add random variation and round to 2 decimals

    # Simulate CO2 levels as a sine wave over 24 hours with some randomness
    base_co2 = 650 + 200 * math.sin(math.pi * (hour - 6) / 12)  # 650 ppm average, 200 ppm amplitude
    co2 = int(base_co2 + random.uniform(-5, 5))  # Add random variation and convert to integer

    time_str = f"{int(hour):02}:{int(minute):02}"  # Format time as hh:mm

    return {
        "co2": co2,
        "temperature": temperature,
        "light_on": light_status,
        "time": time_str
    }

def main():
    broker = os.getenv('BROKER_ADDRESS')
    port = int(os.getenv('BROKER_PORT'))
    username = os.getenv('MQTT_USERNAME')
    password = os.getenv('MQTT_PASSWORD')
    root_topic = os.getenv('MQTT_TOPIC')
    num_rooms = int(os.getenv('NUM_ROOMS'))
    frequency = int(os.getenv('FREQUENCY'))
    realtime_multiplier = float(os.getenv('REALTIME_MULTIPLIER'))

    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.connect(broker, port)

    light_status = {room_id: random.choice([True, False]) for room_id in range(1, num_rooms + 1)}
    light_change_counter = {room_id: 0 for room_id in range(1, num_rooms + 1)}
    hour = 6  # Start at 6 AM for lowest values
    minute = 0

    while True:
        all_data = {}
        for room_id in range(1, num_rooms + 1):
            if light_change_counter[room_id] >= 10:  # Change light status every 10 cycles
                light_status[room_id] = not light_status[room_id]
                light_change_counter[room_id] = 0
            else:
                light_change_counter[room_id] += 1

            data = generate_dummy_data(room_id, light_status[room_id], hour, minute)
            all_data[f"room{room_id}"] = data

        client.publish(root_topic, json.dumps(all_data))

        time.sleep(frequency)  # Publish every 'frequency' seconds
        minute += (frequency * realtime_multiplier) / 60
        if minute >= 60:
            hour = (hour + 1) % 24
            minute = minute % 60

if __name__ == "__main__":
    main()