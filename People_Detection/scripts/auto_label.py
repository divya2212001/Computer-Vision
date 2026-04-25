from ultralytics import YOLO
import os
import json
from PIL import Image


IMAGE_FOLDER = "../dataset/images/train"
OUTPUT_JSON = "prelabels.json"

# Load YOLO model
model = YOLO("yolov8n.pt")

# Allowed classes
allowed = {
    "car": "car",
    "truck": "truck",
    "bus": "bus",
    "person": "person",
    "motorcycle": "bike"
}

tasks = []

for file in os.listdir(IMAGE_FOLDER):
    if file.lower().endswith((".jpg", ".jpeg", ".png")):

        image_path = os.path.join(IMAGE_FOLDER, file)

        # Get image size
        img = Image.open(image_path)
        img_w, img_h = img.size

        # Run prediction
        results = model(image_path)[0]

        predictions = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])

            if conf < 0.35:
                continue

            class_name = model.names[cls_id]

            if class_name in allowed:

                label_name = allowed[class_name]

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                # Convert to Label Studio %
                x = (x1 / img_w) * 100
                y = (y1 / img_h) * 100
                width = ((x2 - x1) / img_w) * 100
                height = ((y2 - y1) / img_h) * 100

                predictions.append({
                    "from_name": "label",
                    "to_name": "image",
                    "type": "rectanglelabels",
                    "value": {
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height,
                        "rotation": 0,
                        "rectanglelabels": [label_name]
                    }
                })

        task = {
            "data": {
                "image": image_path
            },
            "predictions": [
                {
                    "model_version": "YOLOv8 Auto Label",
                    "result": predictions
                }
            ]
        }

        tasks.append(task)

with open(OUTPUT_JSON, "w") as f:
    json.dump(tasks, f, indent=2)

print(f"Created: {OUTPUT_JSON}")
print(f"Tasks: {len(tasks)}")