# People Detection with YOLOv8

A computer vision project for detecting people (and other objects) in videos using **YOLOv8**. The repository includes a complete pipeline for frame extraction, dataset preparation, auto-labeling, model training/inference, and video post-processing.

---


## Overview

This project demonstrates an end-to-end workflow for building a people detection system:

1. **Frame Extraction**: Convert input video into image frames.
2. **Dataset Splitting**: Organize frames into `train`, `val`, and `test` sets.
3. **Auto Labeling**: Use a pretrained YOLOv8 model to generate bounding-box annotations in Label Studio format.
4. **Training & Inference**: Fine-tune YOLOv8 on custom data or run inference directly.
5. **Video Processing**: A Colab notebook stitches processed frames back into videos with side-by-side comparisons (raw, detection, segmentation).

---

## Project Structure

```
Computer-Vision/
├── People_Detection/
│   ├── data.yml                     # YOLOv8 dataset configuration
│   ├── dataset/
│   │   ├── images/
│   │   │   ├── train/               # Training images
│   │   │   ├── val/                 # Validation images
│   │   │   └── test/                # Test images
│   │   ├── images_prev/             # Previous image sets (backup)
│   │   ├── labels/                  # YOLO format labels (.txt)
│   │   └── raw_frames/              # Frames extracted from video
│   └── scripts/
│       ├── extract_frames.py        # Extract frames from MP4
│       ├── split_dataset.py         # Split into train/val/test
│       ├── auto_label.py            # Generate pre-labels with YOLOv8
│       └── yolov8n.pt               # Pretrained nano model (auto-downloaded)
├── week/
│   └── detect.py                    # Quick YOLOv8 inference script
├── week3_task2.ipynb                # Colab notebook: full video pipeline
├── people-detection.mp4             # Sample input video
├── requirements.txt                 # Python dependencies
└── Readme.md                        # This file
```

---

## Prerequisites

- **Python**: 3.11
- **ffmpeg**: Required for video encoding/decoding in the Colab notebook and local video processing.
  - *macOS*: `brew install ffmpeg`
  - *Ubuntu/Debian*: `sudo apt-get install ffmpeg`
  - *Windows*: [Download from ffmpeg.org](https://ffmpeg.org/download.html)
- **GPU** (optional but recommended): CUDA-compatible GPU for faster YOLOv8 training/inference.

---

## Installation

1. **Clone the repository** (if applicable) and navigate to the project root:
   ```bash
   cd Computer-Vision
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Extract Frames from Video

Convert `people-detection.mp4` into individual frames saved under `People_Detection/dataset/raw_frames/`.

```bash
cd People_Detection/scripts
python extract_frames.py
```

- **Output**: `dataset/raw_frames/frame_0.jpg`, `frame_1.jpg`, ...
- **Settings**: Extracts one frame every `100 ms` (10 fps).

---

### 2. Split Dataset

Shuffle and split extracted frames into training, validation, and test sets (70/20/10).

```bash
cd People_Detection/scripts
python split_dataset.py
```

- **Output**:
  - `dataset/images/train/`
  - `dataset/images/val/`
  - `dataset/images/test/`

---

### 3. Auto Labeling with YOLOv8

Generate bounding-box pre-labels for training images using a pretrained YOLOv8 nano model. The results are exported in **Label Studio** JSON format.

```bash
cd People_Detection/scripts
python auto_label.py
```

- **Output**: `prelabels.json`
- **Classes mapped**: `person`, `car`, `truck`, `bus`, `bike` (motorcycle)
- **Confidence threshold**: `0.35`

> You can import `prelabels.json` into [Label Studio](https://labelstud.io/) to review and correct annotations before exporting final YOLO `.txt` labels.

---

### 4. Train / Detect

The dataset is configured via `People_Detection/data.yml`:

```yaml
path: dataset
train: images/train
val: images/val
names:
  0: person
```

**Quick inference example** (from the `week/` directory):

```bash
cd week
python detect.py
```

**Training example** (using the Ultralytics CLI):

```bash
yolo detect train data=People_Detection/data.yml model=yolov8n.pt epochs=100 imgsz=640
```

---

### 5. Colab Notebook (Video Pipeline)

Open `week3_task2.ipynb` in [Google Colab](https://colab.research.google.com/) for a complete video-processing pipeline:

1. Download a YouTube video using `yt-dlp`.
2. Extract frames with `ffmpeg`.
3. Run **object detection** (`yolov8s.pt`) and **instance segmentation** (`yolov8n-seg.pt`) on each frame.
4. Re-encode frames into individual videos.
5. Stack raw, detected, and segmented videos vertically.
6. Add custom audio to produce the final output.

> **Note**: The notebook is optimized for Colab and uses `torch.cuda` for GPU acceleration.

---

## Dataset Configuration

`People_Detection/data.yml` follows the [Ultralytics YOLO dataset format](https://docs.ultralytics.com/datasets/detect/).

| Key     | Value                                    |
|---------|------------------------------------------|
| `path`  | Root directory of the dataset            |
| `train` | Relative path to training images         |
| `val`   | Relative path to validation images       |
| `names` | Class index-to-name mapping              |

Make sure your label files (`.txt`) are placed under `People_Detection/dataset/labels/train/` and `labels/val/` with the same filenames as the images.

---


