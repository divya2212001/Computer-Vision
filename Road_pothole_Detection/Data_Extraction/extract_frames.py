import cv2
import os

video_path = "road.mp4"
output_folder = "dataset/raw_images"

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

count = 0
frame_interval = 10

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if count % frame_interval == 0:
        frame_name = f"frame_{count}.jpg"
        cv2.imwrite(os.path.join(output_folder, frame_name), frame)

    count += 1

cap.release()

print("Frames extracted successfully!")