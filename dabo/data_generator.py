import json
import random
import math
import time

# --------------------------------------------------
# FUNCTION TYPES
# --------------------------------------------------

# --------------------------------------------------
# Generic
# --------------------------------------------------

def clamp(value, min_val, max_val):
    return min(max(value, min_val), max_val)


def random_float(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)


def random_int(min_val, max_val):
    return random.randint(min_val, max_val)


def simulated_timestamp():
    return int(time.time())


def normal_time(hour, minute, second):
    return f"{int(hour):02}:{int(minute):02}:{int(second):02}"


def daily_sine(hour, peak_hour=14, min_val=0, max_val=1):
    angle = math.pi * (hour - (peak_hour - 6)) / 12
    value = (math.sin(angle) + 1) / 2
    return min_val + value * (max_val - min_val)


# --------------------------------------------------
# Room sensors
# --------------------------------------------------

def sine_temp(hour, min_val, max_val):
    base = 20 + 5 * math.sin(math.pi * (hour - 6) / 12)
    temp = base + random.uniform(-0.5, 0.5)
    return round(clamp(temp, min_val, max_val), 2)


def sine_co2(hour, min_val, max_val):
    base = 650 + 200 * math.sin(math.pi * (hour - 6) / 12)
    co2 = base + random.uniform(-5, 5)
    return int(clamp(co2, min_val, max_val))


def sine_humidity(hour, min_val, max_val):
    base = 60 + 20 * math.sin(math.pi * (hour - 6) / 12)
    humidity = base + random.uniform(-2, 2)
    return round(clamp(humidity, min_val, max_val), 2)


# --------------------------------------------------
# Bench occupancy
# --------------------------------------------------

def bench_occupancy(hour, minute, sensor_id, capacity=4):
    if not hasattr(bench_occupancy, "_states"):
        bench_occupancy._states = {}

    if sensor_id not in bench_occupancy._states:
        bench_occupancy._states[sensor_id] = {
            "remaining": [],
            "last_min": None
        }

    state = bench_occupancy._states[sensor_id]
    current_min = (hour % 24) * 60 + (minute % 60)

    if state["last_min"] is None:
        state["last_min"] = current_min

    if current_min < state["last_min"]:
        current_min += 1440

    while state["last_min"] < current_min:
        state["remaining"] = [
            t - 1 for t in state["remaining"] if (t - 1) > 0
        ]

        if len(state["remaining"]) < capacity and random.random() < 0.05:
            state["remaining"].append(random.randint(5, 60))

        state["last_min"] += 1

    return len(state["remaining"])


# --------------------------------------------------
# Weather station
# --------------------------------------------------

def weather_temperature(hour, min_val=4, max_val=32):
    base = daily_sine(hour, peak_hour=15, min_val=min_val, max_val=max_val)
    noise = random.uniform(-0.8, 0.8)
    return round(clamp(base + noise, min_val, max_val), 2)


def weather_humidity(hour, min_val=30, max_val=98):
    temp_curve = daily_sine(hour, peak_hour=15, min_val=0, max_val=1)
    base = max_val - temp_curve * (max_val - min_val)
    noise = random.uniform(-3, 3)
    return round(clamp(base + noise, min_val, max_val), 2)


def weather_pressure(hour, min_val=980, max_val=1040):
    base = 1013 + 6 * math.sin(math.pi * hour / 12)
    noise = random.uniform(-1.5, 1.5)
    return round(clamp(base + noise, min_val, max_val), 2)


def weather_wind_speed(hour, min_val=0, max_val=18):
    base = daily_sine(hour, peak_hour=14, min_val=1, max_val=7)
    gust = random.uniform(0, 3) if random.random() < 0.15 else 0
    noise = random.uniform(-0.8, 0.8)
    return round(clamp(base + gust + noise, min_val, max_val), 2)


def weather_wind_direction(hour, min_val=0, max_val=359):
    base = 180 + 80 * math.sin(math.pi * hour / 12)
    noise = random.uniform(-25, 25)
    return int(clamp((base + noise) % 360, min_val, max_val))


def weather_rain_rate(hour, min_val=0, max_val=25):
    rain_probability = 0.03

    if 6 <= hour <= 10:
        rain_probability = 0.08
    elif 17 <= hour <= 22:
        rain_probability = 0.07

    if random.random() < rain_probability:
        return round(random.uniform(0.2, max_val), 2)

    return 0.0


def weather_solar_radiation(hour, min_val=0, max_val=1000):
    if hour < 5 or hour > 21:
        return 0

    base = daily_sine(hour, peak_hour=13, min_val=0, max_val=max_val)
    cloud_factor = random.uniform(0.45, 1.0)
    noise = random.uniform(-30, 30)

    return round(clamp(base * cloud_factor + noise, min_val, max_val), 2)


def weather_uv(hour, min_val=0, max_val=9):
    if hour < 6 or hour > 20:
        return 0

    base = daily_sine(hour, peak_hour=13, min_val=0, max_val=max_val)
    cloud_factor = random.uniform(0.5, 1.0)

    return round(clamp(base * cloud_factor, min_val, max_val), 2)


def lux_sensor(hour, min_val=0, max_val=120000):
    if hour < 5 or hour > 21:
        return 0

    base = daily_sine(hour, peak_hour=13, min_val=0, max_val=max_val)
    cloud_factor = random.uniform(0.35, 1.0)
    noise = random.uniform(-1500, 1500)

    return round(clamp(base * cloud_factor + noise, min_val, max_val), 2)


def surface_temperature(hour, min_val=2, max_val=50):
    air_temp = weather_temperature(hour, min_val=4, max_val=32)

    if 10 <= hour <= 17:
        solar_gain = random.uniform(4, 13)
    elif 18 <= hour <= 20:
        solar_gain = random.uniform(1, 5)
    else:
        solar_gain = random.uniform(-3, 1)

    noise = random.uniform(-0.8, 0.8)

    return round(clamp(air_temp + solar_gain + noise, min_val, max_val), 2)


# --------------------------------------------------
# Water level
# --------------------------------------------------

def ultrasonic_water_level(hour, minute, sensor_id, min_val=20, max_val=120):
    if not hasattr(ultrasonic_water_level, "_states"):
        ultrasonic_water_level._states = {}

    if sensor_id not in ultrasonic_water_level._states:
        ultrasonic_water_level._states[sensor_id] = {
            "level": random.uniform(45, 75),
            "last_min": None
        }

    state = ultrasonic_water_level._states[sensor_id]
    current_min = (hour % 24) * 60 + (minute % 60)

    if state["last_min"] is None:
        state["last_min"] = current_min

    if current_min < state["last_min"]:
        current_min += 1440

    while state["last_min"] < current_min:
        current_hour = (state["last_min"] // 60) % 24

        state["level"] -= random.uniform(0.005, 0.025)

        rain_probability = 0.002
        if 6 <= current_hour <= 10 or 17 <= current_hour <= 22:
            rain_probability = 0.006

        if random.random() < rain_probability:
            state["level"] += random.uniform(1.5, 6.0)

        state["level"] = clamp(state["level"], min_val, max_val)
        state["last_min"] += 1

    noise = random.uniform(-0.8, 0.8)
    return round(clamp(state["level"] + noise, min_val, max_val), 2)


# --------------------------------------------------
# Soil sensors
# --------------------------------------------------

def soil_moisture(hour, minute, sensor_id, min_val=10, max_val=90):
    if not hasattr(soil_moisture, "_states"):
        soil_moisture._states = {}

    if sensor_id not in soil_moisture._states:
        soil_moisture._states[sensor_id] = {
            "moisture": random.uniform(35, 65),
            "last_min": None
        }

    state = soil_moisture._states[sensor_id]
    current_min = (hour % 24) * 60 + (minute % 60)

    if state["last_min"] is None:
        state["last_min"] = current_min

    if current_min < state["last_min"]:
        current_min += 1440

    while state["last_min"] < current_min:
        current_hour = (state["last_min"] // 60) % 24

        dry_rate = random.uniform(0.003, 0.012)

        if 11 <= current_hour <= 17:
            dry_rate *= 2.0

        state["moisture"] -= dry_rate

        water_probability = 0.0015
        if 6 <= current_hour <= 9 or 18 <= current_hour <= 21:
            water_probability = 0.004

        if random.random() < water_probability:
            state["moisture"] += random.uniform(3, 12)

        state["moisture"] = clamp(state["moisture"], min_val, max_val)
        state["last_min"] += 1

    noise = random.uniform(-1.2, 1.2)
    return round(clamp(state["moisture"] + noise, min_val, max_val), 2)


def soil_temperature(hour, min_val=6, max_val=26):
    base = daily_sine(hour, peak_hour=16, min_val=min_val, max_val=max_val)
    noise = random.uniform(-0.4, 0.4)
    return round(clamp(base + noise, min_val, max_val), 2)


# --------------------------------------------------
# BirdNET-style sensor
# --------------------------------------------------

BIRD_SPECIES = [
    "Turdus merula",
    "Parus major",
    "Cyanistes caeruleus",
    "Erithacus rubecula",
    "Columba palumbus",
    "Pica pica",
    "Corvus corone",
    "Passer domesticus"
]


def birdnet_audio_level(hour, min_val=25, max_val=85):
    base = daily_sine(hour, peak_hour=13, min_val=35, max_val=65)

    if 7 <= hour <= 9 or 17 <= hour <= 19:
        base += random.uniform(3, 10)

    noise = random.uniform(-4, 4)
    return round(clamp(base + noise, min_val, max_val), 2)


def birdnet_event(hour, min_val=0, max_val=1):
    probability = 0.03

    if 5 <= hour <= 9:
        probability = 0.35
    elif 16 <= hour <= 20:
        probability = 0.22
    elif 10 <= hour <= 15:
        probability = 0.10
    elif hour >= 22 or hour <= 4:
        probability = 0.01

    detected = 1 if random.random() < probability else 0
    audio_level = birdnet_audio_level(hour, 25, 85)

    if detected == 0:
        return {
            "bird_detected": 0,
            "species": None,
            "confidence": 0.0,
            "audio_level_db": audio_level
        }

    if 5 <= hour <= 9:
        species_pool = [
            "Turdus merula",
            "Erithacus rubecula",
            "Parus major",
            "Cyanistes caeruleus",
            "Columba palumbus"
        ]
    elif 16 <= hour <= 20:
        species_pool = [
            "Turdus merula",
            "Columba palumbus",
            "Pica pica",
            "Corvus corone"
        ]
    else:
        species_pool = BIRD_SPECIES

    return {
        "bird_detected": 1,
        "species": random.choice(species_pool),
        "confidence": round(random.uniform(0.5, 0.99), 2),
        "audio_level_db": audio_level
    }


def get_birdnet_event(device_id, hour, minute, second):
    """
    Keeps birdnet_detected, species and confidence consistent
    when using separate JSON fields.
    """
    if not hasattr(get_birdnet_event, "_events"):
        get_birdnet_event._events = {}

    key = (device_id, hour, minute, second)

    if key not in get_birdnet_event._events:
        get_birdnet_event._events[key] = birdnet_event(hour)

    return get_birdnet_event._events[key]


# --------------------------------------------------
# Noise sensor
# --------------------------------------------------

def noise_level(hour, min_val=50, max_val=90):
    base = 38

    if 7 <= hour <= 9:
        base = 58
    elif 10 <= hour <= 16:
        base = 52
    elif 17 <= hour <= 19:
        base = 60
    elif 20 <= hour <= 22:
        base = 48
    elif hour >= 23 or hour <= 5:
        base = 34

    occasional_event = random.uniform(5, 18) if random.random() < 0.08 else 0
    noise = random.uniform(-4, 4)

    return round(clamp(base + occasional_event + noise, min_val, max_val), 2)


# --------------------------------------------------
# Air quality sensor
# --------------------------------------------------

def air_quality_pm25(hour, min_val=2, max_val=80):
    base = 8

    if 7 <= hour <= 10:
        base = 18
    elif 16 <= hour <= 19:
        base = 20
    elif hour >= 23 or hour <= 5:
        base = 10

    pollution_event = random.uniform(5, 25) if random.random() < 0.06 else 0
    noise = random.uniform(-2, 2)

    return round(clamp(base + pollution_event + noise, min_val, max_val), 2)


def air_quality_pm10(hour, min_val=5, max_val=120):
    pm25 = air_quality_pm25(hour, min_val=2, max_val=80)
    multiplier = random.uniform(1.4, 2.3)

    return round(clamp(pm25 * multiplier, min_val, max_val), 2)


def air_quality_no2(hour, min_val=5, max_val=100):
    base = 12

    if 7 <= hour <= 10:
        base = 38
    elif 16 <= hour <= 19:
        base = 42
    elif hour >= 23 or hour <= 5:
        base = 10

    noise = random.uniform(-4, 4)
    spike = random.uniform(8, 25) if random.random() < 0.05 else 0

    return round(clamp(base + noise + spike, min_val, max_val), 2)


def air_quality_o3(hour, min_val=2, max_val=90):
    base = daily_sine(hour, peak_hour=15, min_val=8, max_val=55)
    noise = random.uniform(-5, 5)

    return round(clamp(base + noise, min_val, max_val), 2)


def air_quality_voc(hour, min_val=50, max_val=800):
    base = 120

    if 8 <= hour <= 18:
        base = 220
    elif 19 <= hour <= 22:
        base = 170

    event = random.uniform(80, 350) if random.random() < 0.04 else 0
    noise = random.uniform(-30, 30)

    return round(clamp(base + event + noise, min_val, max_val), 2)


# --------------------------------------------------
# Sensor registry
# --------------------------------------------------

sensor_functions = {
    "random_float": random_float,
    "random_int": random_int,
    "sine_temp": sine_temp,
    "sine_co2": sine_co2,
    "sine_humidity": sine_humidity,
    "timestamp": simulated_timestamp,
    "normal_time": normal_time,

    "bench_occupancy": bench_occupancy,

    "weather_temperature": weather_temperature,
    "weather_humidity": weather_humidity,
    "weather_pressure": weather_pressure,
    "weather_wind_speed": weather_wind_speed,
    "weather_wind_direction": weather_wind_direction,
    "weather_rain_rate": weather_rain_rate,
    "weather_solar_radiation": weather_solar_radiation,
    "weather_uv": weather_uv,
    "lux_sensor": lux_sensor,
    "surface_temperature": surface_temperature,

    "ultrasonic_water_level": ultrasonic_water_level,

    "soil_moisture": soil_moisture,
    "soil_temperature": soil_temperature,

    "birdnet_audio_level": birdnet_audio_level,
    "birdnet_event": birdnet_event,

    "noise_level": noise_level,

    "air_quality_pm25": air_quality_pm25,
    "air_quality_pm10": air_quality_pm10,
    "air_quality_no2": air_quality_no2,
    "air_quality_o3": air_quality_o3,
    "air_quality_voc": air_quality_voc
}


# --------------------------------------------------
# Load device template
# --------------------------------------------------

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


# --------------------------------------------------
# Generate data
# --------------------------------------------------

def generate_data(device_id, device_profile, hour, minute, second):
    data = {}

    for sensor_name, sensor_info in device_profile.items():
        sensor_type = sensor_info["type"]
        func = sensor_functions.get(sensor_type)

        min_val = sensor_info.get("min", 0)
        max_val = sensor_info.get("max", 100)

        if sensor_type in [
            "sine_temp",
            "sine_co2",
            "sine_humidity",

            "weather_temperature",
            "weather_humidity",
            "weather_pressure",
            "weather_wind_speed",
            "weather_wind_direction",
            "weather_rain_rate",
            "weather_solar_radiation",
            "weather_uv",
            "lux_sensor",
            "surface_temperature",

            "soil_temperature",

            "birdnet_audio_level",

            "noise_level",

            "air_quality_pm25",
            "air_quality_pm10",
            "air_quality_no2",
            "air_quality_o3",
            "air_quality_voc"
        ]:
            value = func(hour, min_val, max_val)

        elif sensor_type in [
            "random_float",
            "random_int"
        ]:
            value = func(min_val, max_val)

        elif sensor_type == "timestamp":
            value = simulated_timestamp()

        elif sensor_type == "normal_time":
            value = normal_time(hour, minute, second)

        elif sensor_type == "bench_occupancy":
            capacity = sensor_info.get("capacity", 4)
            value = bench_occupancy(hour, minute, device_id, capacity)

        elif sensor_type in [
            "ultrasonic_water_level",
            "soil_moisture"
        ]:
            value = func(hour, minute, device_id, min_val, max_val)

        elif sensor_type == "birdnet_detection":
            event = get_birdnet_event(device_id, hour, minute, second)
            value = event["bird_detected"]

        elif sensor_type == "birdnet_species":
            event = get_birdnet_event(device_id, hour, minute, second)
            value = event["species"]

        elif sensor_type == "birdnet_confidence":
            event = get_birdnet_event(device_id, hour, minute, second)
            value = event["confidence"]

        elif sensor_type == "birdnet_event":
            value = birdnet_event(hour)

        elif func:
            value = func()

        else:
            value = None

        data[sensor_name] = value

    return data