import json
import random
import math
import time

# Functions used to simulate the sensor values.
def random_float(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)

def random_int(min_val, max_val):
    return random.randint(min_val, max_val)

def sine_temp(hour, min_val, max_val):
    base = 20 + 5 * math.sin(math.pi * (hour - 6) / 12)
    temp = base + random.uniform(-0.5, 0.5)
    return round(min(max(temp, min_val), max_val), 2)

def sine_co2(hour, min_val, max_val):
    base = 650 + 200 * math.sin(math.pi * (hour - 6) / 12)
    co2 = base + random.uniform(-5, 5)
    return int(min(max(co2, min_val), max_val))

def simulated_timestamp():
    return int(time.time())

def normal_time(hour, minute,second):
    return f"{int(hour):02}:{int(minute):02}:{int(second):02}"

sensor_functions = {
    "random_float": random_float,
    "random_int": random_int,
    "sine_temp": sine_temp,
    "sine_co2": sine_co2,
    "timestamp": simulated_timestamp,
    "normal_time": normal_time
}

# Import the sensors from the device_template.json
def load_device_definitions_from_template(template_path):
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

# The data is simulated using the top functions and the variabled provided by the sensor
def generate_data(device_profile, hour, minute, second):
    data = {}
    for sensor_name, sensor_info in device_profile.items():
        sensor_type = sensor_info["type"]
        func = sensor_functions.get(sensor_type)
        if func:
            if sensor_type in ["sine_temp", "sine_co2"]:
                min_val = sensor_info.get("min", 0)
                max_val = sensor_info.get("max", 100)
                value = func(hour, min_val, max_val)
            elif sensor_type in ["random_float", "random_int"]:
                min_val = sensor_info.get("min", 0)
                max_val = sensor_info.get("max", 100)
                value = func(min_val, max_val)
            elif sensor_type == "timestamp":
                value = func()
            elif sensor_type == "normal_time":
                value = func(hour, minute,second)
            else:
                value = func()
            data[sensor_name] = value
    return data