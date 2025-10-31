# :incoming_envelope: DaBo :incoming_envelope:

## Data in a Box <br> A Customizable MQTT Publisher for Synthetic Data

## Description

DaBo is a customizable MQTT publisher written in Python, designed to broadcast synthetic sensor data for testing, prototyping, and demonstration purposes. It uses the [Eclipse Paho-MQTT](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html) library to publish data to an MQTT broker and is fully containerised for easy deployment. DaBo simulates sensor readings using randomised and time-aware functions, making it ideal for visualising data flows when real-world data is unavailable or impractical to use:

- Prototyping data pipelines
- Testing MQTT-based dashboards
- Demonstrating real-time data visualisation
- Teaching and experimentation

## Features

- **Synthetic Sensor Simulation**: Generates data using randomized functions and sine wave patterns to simulate realistic temporal rhythms.
- **Customizable Devices**: Define multiple device types and sensor profiles via a JSON template.
- **MQTT Publishing**: Publishes data to a broker with configurable frequency and time acceleration.
- **Containerised**: Easily deployable with [Docker Compose](https://docs.docker.com/compose/) or [Podman Compose](https://podman-desktop.io/docs/compose).

## How It Works
1. Device Definitions

The `device_template.json` file defines the virtual devices and their sensors. This is the core configuration that DaBo uses to simulate and publish synthetic data.
Each entry in the JSON array must include:

- `device_type`: A string representing the type of device (e.g. `raspberry_pi`). This forms the base of the device ID and MQTT subtopic.
- `count`: An integer specifying how many instances of this device type to simulate.
- `root_topic`: The parent MQTT topic under which all devices of this type will publish.
- `sensors`: A dictionary of sensor names and their simulation configuration.

Each `sensor` must include:
- `type`: The function used to simulate the sensor value. This must match one of the available functions in `data_generator.py`:

- `random_float`: Generates a floating-point number between a specified minimum and maximum.
- `random_int`: Produces a random integer within a defined range.
- `sine_temp`: Simulates temperature following a daily sine wave pattern, peaking at noon and dipping at midnight.
- `sine_co2`: Simulates CO₂ levels using a sine wave to reflect daily fluctuations similar to human activity cycles.
- `timestamp`: Returns the current Unix timestamp to represent a heartbeat or data capture moment.
- `normal_time`: Formats the simulated time as a human-readable string (HH:MM:SS).

- `min and max`: The minimum and maximum values the sensor can produce (required for all types except `timestamp` and `normal_time`).

The MQTT topic for each device is constructed as:

Number of instances (count)
MQTT topic root (root_topic)
Sensor definitions with types and value ranges

```bash
<root_topic>/<device_type>_<device_number>
```

For example, with:

```json
{
  "device_type": "room_sensor",
  "count": 2,
  "root_topic": "room"
}
```

The devices will publish to:

- `room/room_sensor_01`
- `room/room_sensor_02`

Each sensor within the device will be published as a JSON payload under that topic.

```json
[
  {
    "device_type": "raspberry_pi",
    "count": 10,
    "root_topic": "pi_cluster",
    "sensors": {
      "cpu_percent": { "type": "random_float", "min": 0, "max": 100 },
      "ping_ms": { "type": "random_int", "min": 10, "max": 100 },
      "temp": { "type": "sine_temp", "min": 30, "max": 45 },
      "heartbeat": { "type": "timestamp" },
      "time": { "type": "normal_time" }
    }
  },
  {
    "device_type": "room_sensor",
    "count": 18,
    "root_topic": "room",
    "sensors": {
      "co2": { "type": "sine_co2", "min": 400, "max": 1000 },
      "temperature": { "type": "sine_temp", "min": 18, "max": 26 },
      "light_on": { "type": "random_int", "min": 0, "max": 1 },
      "time": { "type": "normal_time" }
    }
  }
]
```

## Configuration

Create a new `.env` file and set the following environment variables:

```env
BROKER_ADDRESS = broker.mqtt.to.use # The address of the broker [string]
BROKER_PORT = port # The port of the broker used to publish [int] 
MQTT_USERNAME = user # User ID [string]
MQTT_PASSWORD = password # Password (use quotes if it contains special characters)
MQTT_TOPIC = something/something/dabo  # The root topic where the message is published
FREQUENCY = 1 # Frequency in seconds at which sensors send data (default is every 1 second)
REALTIME_MULTIPLIER = 60 # See table below

# 1    => Real time                        => 1 second = 1 second 
# 60   => 1 second = 1 simulated minute    => 1 second = 1 minute
# 3600 => 1 second = 1 simulated hour      => 1 second = 1 hour
# 1800 => 1 second = 30 simulated minutes  => 1 second = 30 minutes
# 0.5  => 1 second = 0.5 simulated seconds => 1 second = half a second
```

The system simulates time progression using a REALTIME_MULTIPLIER to speed up or slow down the 24-hour cycle.


## Getting Started

### Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/ucl-casa-ce/dabo.git
cd dabo
```

### [Option A] Running DaBo from the Console (Python)

- Install dependencies:

```bash
pip install paho-mqtt python-dotenv
```
- Set up your environment:
  - Create a `.env` file with your MQTT broker settings.
  - Ensure `device_template.json` is present and correctly configured.

### Run the publisher:

```bash
python main.py
```

This will start publishing synthetic sensor data to your MQTT broker at the configured frequency.

###  [Option B] Running DaBo with Docker/Podman
- Ensure Docker/Podman and Docker/Podman Compose are installed.
- Set up your environment:
  - Create a `.env` file with your MQTT broker settings.
  - Ensure `device_template.json` is present and correctly configured.
- Build and run the container:

```bash
docker-compose up --build
```



This will launch DaBo inside a container and begin publishing data based on your `.env` and `device_template.json` configuration.

## Disclaimer
This system generates synthetic data and does not reflect real-world measurements. It should be used solely for demonstration and testing purposes.