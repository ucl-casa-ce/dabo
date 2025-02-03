# :incoming_envelope: DaBo :incoming_envelope:

## Data in a Box <br> A Simple, Customizable MQTT Publisher for Dummy Multi-Room Environmental Data

## Description
DaBo, from the Latin "I will give", is a simple MQTT publisher based on [Eclipse Paho-MQTT](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html) to provide dummy data for temperature, CO2, and light on/off over 24 hours. The data is randomized and follows a simple sine wave, so it does not reflect any real-case scenario or real data (for now...). Over the 24 hours, the temperature and CO2 reach their highest values at noon and their lowest at midnight, then repeat. Light is also randomized every 10 cycles. It should be used solely to demonstrate data visualization when real data is unavailable.
All of this is nicely dockerized and controlled by [Docker Compose](https://docs.docker.com/compose/).

## Usage

> [!NOTE]
> Ensure Docker is installed on your system before running DaBo. You can download Docker from [here](https://www.docker.com/get-started).

Create a '.env' in the same folder of the `dockerfile` to configure the parameters of DaBo:

```.env
BROKER_ADDRESS=mqtt.your.broker # The address of the broker
BROKER_PORT=1111 # The port of the broker used to publish  
MQTT_USERNAME=userid # User ID
MQTT_PASSWORD="password" # Password (use quotes if it contains special characters)
MQTT_TOPIC=root/of/the/topic # The root topic where the message is published
NUM_ROOMS=10 # Number of rooms created
FREQUENCY=1 # Frequency in seconds at which sensors send data (default is 1 second)
REALTIME_MULTIPLIER=50 # Value to speed up the simulation (50 means 1 second = 1 minute)
```

Build the image using 

```console
docker-compose build
```

Run the container using

```console
docker-compose up
```

The message sent will have the following syntax (in the case of 3 rooms):

```json
{
  "room1": {
    "co2": 395,
    "temperature": 20.39,
    "light_on": true,
    "time": "06:43"
  },
  "room2": {
    "co2": 404,
    "temperature": 19.48,
    "light_on": false,
    "time": "06:43"
  },
  "room3": {
    "co2": 392,
    "temperature": 20.07,
    "light_on": true,
    "time": "06:43"
  }
}
```

