
""" This initializes an MQTT client, connects to the broker, subscribes to a topic, 
and prints received messages. Moreover, client.loop_start() runs the MQTT client in 
a separate thread, ensuring it continues to listen for messages."""

import json
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
from django.core.cache import cache

load_dotenv()

# Load MQTT Credentials
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")


# Define MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        message = json.loads(msg.payload.decode("utf-8"))
        print(f"Received message: {message}")

        # Store message in Django cache
        cache.set("mqtt_data", message, timeout=20) # Store for 10 seconds
        print("Message stored in cache")
        
    except json.JSONDecodeError:
        print("Error decoding MQTT message")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT Broker")


# Create and configure MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_start()