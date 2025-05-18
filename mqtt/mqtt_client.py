""" 
MQTT client that saves received images, processes them with detector(),
and saves results to Django models.
"""

import json
import base64
import paho.mqtt.client as mqtt
import os
from datetime import datetime
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from detector.models import ImageFiles, Detections
from detector import detector  # Your image processing module

load_dotenv()

# Load MQTT Credentials
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")

def save_image_from_message(message):
    """Save image data from MQTT message to ImageFiles model"""
    try:
        # Extract data from message
        node_name = message.get('node')
        location = message.get('location')
        image_data = message.get('image')
        
        # Get or create Node instance (adjust based on your Node model)
        node, _ = Node.objects.get_or_create(name=node_name, defaults={'location': location})
        
        # Decode base64 image data
        if image_data.startswith('data:image'):
            # Handle data URI format: "data:image/jpeg;base64,/9j/4AAQSkZ..."
            image_data = image_data.split(',')[1]
        img_bytes = base64.b64decode(image_data)
        
        # Create ImageFiles instance
        timestamp = datetime.now()
        img_file = ContentFile(img_bytes, name=f"{node_name}_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg")
        
        image_record = ImageFiles.objects.create(
            image=img_file,
            node=node,
            timestamp=timestamp
        )
        
        return image_record
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None

def process_and_save_detection(image_record):
    """Process image and save detection results"""
    try:
        # Process image using your detector function
        detection_result = detector(image_record.image.path)
        
        # Create Detections record
        detection = Detections.objects.create(
            detected=detection_result['detected'],
            confidence=detection_result['confidence'],
            input=image_record,
            output=detection_result.get('output_image')  # If your detector returns processed image
        )
        
        return detection
    except Exception as e:
        print(f"Error processing detection: {str(e)}")
        return None

def on_message(client, userdata, msg):
    try:
        message = json.loads(msg.payload.decode("utf-8"))
        print(f"Received message from {message.get('node')}")
        
        # Save the image to database
        image_record = save_image_from_message(message)
        if not image_record:
            return
            
        # Process the image and save results
        detection = process_and_save_detection(image_record)
        if detection:
            print(f"Detection saved: {detection}")
        
    except json.JSONDecodeError:
        print("Error decoding MQTT message")
    except Exception as e:
        print(f"Error processing message: {str(e)}")

# (Rest of your MQTT setup remains the same)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Connection failed with code {rc}")

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