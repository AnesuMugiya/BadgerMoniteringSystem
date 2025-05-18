""" 
MQTT client that saves received images, processes them with detector(),
and saves results to Django models.
"""

import json
import base64
import paho.mqtt.client as mqtt
import os
import cv2
from datetime import datetime
from dotenv import load_dotenv
from django.core.files.base import ContentFile

from detector.detector import detector

load_dotenv()

# Load MQTT Credentials
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_RESPONSE_TOPIC = os.getenv("MQTT_RESPONSE_TOPIC")  # Default fallback

def send_detection_response(client, original_message, detection_result):
    """Send detection result back to the sender"""
    response = {
        'original_id': original_message.get('id'),
        'original_node': original_message.get('node'),
        'message': "True" if detection_result.detected else "False"
    }
    
    client.publish(
        topic=MQTT_RESPONSE_TOPIC,
        payload=json.dumps(response),
        qos=1,
        retain=False
    )
    print(f"Sent detection response to {MQTT_RESPONSE_TOPIC}")

def save_image_from_message(message):
    """Save image data from MQTT message to ImageFile model"""
    from detector.models import ImageFile, Detection
    from nodes.models import Node
    
    try:
        # Extract data from message
        node_id = message.get('id')
        node_name = message.get('node')
        image_data = message.get('image')
        
        # Decode base64 image data
        if image_data.startswith('data:image'):
            # Handle data URI format: "data:image/jpeg;base64,/9j/4AAQSkZ..."
            image_data = image_data.split(',')[1]
        img_bytes = base64.b64decode(image_data)
        
        # Create ImageFile instance
        timestamp = datetime.now()
        img_file = ContentFile(img_bytes, name=f"{node_name}_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg")
        
        image_record = ImageFile.objects.create(
            image=img_file,
            node=Node.objects.get(id=node_id),
            timestamp=timestamp
        )
        image_record.save()
        return image_record
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return None

def process_and_save_detection(image_record, original_message, client):
    from detector.models import ImageFile, Detection
    from nodes.models import Node
    """Process image and save detection results"""
    try:
        # Process image using your detector function
        output, score, detected = detector(image_record.image.path)
        
        # Encode result_img (OpenCV image) to JPEG bytes
        success, buffer = cv2.imencode('.jpg', output)
        if not success:
            raise Exception("Could not encode processed image.")
        
        # Create a ContentFile for Django ImageField
        output_file = ContentFile(buffer.tobytes(), name=f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        
        # Create Detection record
        detection = Detection.objects.create(
            detected=detected,
            confidence=max(score) if score else 0.0, 
            input=image_record,
            output=output_file # If your detector returns processed image
        )

        # Send response if something was detected
        if detection.detected:
            send_detection_response(client, original_message, detection)
        
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
        detection = process_and_save_detection(image_record, message, client)
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