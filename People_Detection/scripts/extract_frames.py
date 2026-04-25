import cv2
import os

video_path = "people-detection.mp4"

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build correct path
output_folder = os.path.join(BASE_DIR, "..", "dataset", "raw_frames")

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

count = 0
interval_ms = 100

while True:
    cap.set(cv2.CAP_PROP_POS_MSEC, count * interval_ms)

    success, frame = cap.read()

    if not success:
        break

    cv2.imwrite(os.path.join(output_folder, f"frame_{count}.jpg"), frame)

    count += 1

cap.release()
print("Frames extracted successfully!")