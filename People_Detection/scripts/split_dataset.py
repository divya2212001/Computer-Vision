import os
import shutil
import random

# Get current script directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Correct paths
source = os.path.join(BASE_DIR, "..", "dataset", "raw_frames")

train = os.path.join(BASE_DIR, "..", "dataset", "images", "train")
val = os.path.join(BASE_DIR, "..", "dataset", "images", "val")
test = os.path.join(BASE_DIR, "..", "dataset", "images", "test")

# Create folders
for folder in [train, val, test]:
    os.makedirs(folder, exist_ok=True)

# Read images only
images = [img for img in os.listdir(source) if img.lower().endswith((".jpg", ".jpeg", ".png"))]

# Shuffle images
random.seed(42)
random.shuffle(images)

# Split ratio: 70% train, 20% val, 10% test
total = len(images)

train_count = int(total * 0.7)
val_count = int(total * 0.2)

train_imgs = images[:train_count]
val_imgs = images[train_count:train_count + val_count]
test_imgs = images[train_count + val_count:]

# Copy files
for img in train_imgs:
    shutil.copy(os.path.join(source, img), train)

for img in val_imgs:
    shutil.copy(os.path.join(source, img), val)

for img in test_imgs:
    shutil.copy(os.path.join(source, img), test)

print("Dataset Split Completed!")
print(f"Train: {len(train_imgs)} images")
print(f"Val: {len(val_imgs)} images")
print(f"Test: {len(test_imgs)} images")