from ultralytics import YOLO
import cv2
import numpy as np
import os

# Load the model once when the module is imported
# Get the absolute path to the .pt file
MODEL_PATH = os.path.join(os.path.dirname(__file__), "badgerDetector.pt")
model = YOLO(MODEL_PATH)

def detector(image_path):
    """
    Run honey badger detection on an image.

    Args:
        image_path (str): Path to the input image.

    Returns:
        result_img (np.ndarray): Image with detection boxes drawn.
        confidence_scores (List[float]): List of confidence scores.
        detected (bool): True if any honey badger was detected.
    """
    results = model(image_path)
    result = results[0]

    # Get detections
    boxes = result.boxes
    confidence_scores = []
    detected = False

    # Read original image
    img = cv2.imread(image_path)

    if boxes is not None and boxes.shape[0] > 0:
        detected = True
        for box in boxes:
            conf = float(box.conf)
            confidence_scores.append(conf)

            # Coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f"HoneyBadger {conf:.2f}"

            # Draw box and label
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return img, confidence_scores, detected
