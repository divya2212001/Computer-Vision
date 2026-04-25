from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model("image.png", save=True)

print("Done!")# Display the results
