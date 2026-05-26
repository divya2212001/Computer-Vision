import os
import random
import shutil

image_source = "images"
label_source = "labels"

folders = [
    "images/train",
    "images/val",
    "images/test",
    "labels/train",
    "labels/val",
    "labels/test"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

images = [
    f for f in os.listdir(image_source)
    if f.endswith((".jpg", ".jpeg", ".png"))
]

random.shuffle(images)

train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

total = len(images)

train_end = int(total * train_ratio)
val_end = train_end + int(total * val_ratio)

train_images = images[:train_end]
val_images = images[train_end:val_end]
test_images = images[val_end:]

def move_files(image_list, split_name):
    for img in image_list:

        # Image paths
        src_img = os.path.join(image_source, img)
        dst_img = os.path.join(f"images/{split_name}", img)

        shutil.copy(src_img, dst_img)

        # Label file
        label_name = os.path.splitext(img)[0] + ".txt"

        src_label = os.path.join(label_source, label_name)
        dst_label = os.path.join(f"labels/{split_name}", label_name)

        if os.path.exists(src_label):
            shutil.copy(src_label, dst_label)

# Move files
move_files(train_images, "train")
move_files(val_images, "val")
move_files(test_images, "test")

print("Dataset split completed successfully!")
print(f"Train: {len(train_images)}")
print(f"Val: {len(val_images)}")
print(f"Test: {len(test_images)}")