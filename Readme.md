# Computer Vision Internship Pipeline (YOLO Detection)

This repository contains an end-to-end pipeline for **video → frames → dataset → training → prediction → final video** using **Ultralytics YOLO**.

It is structured to match the internship workflow described in the prompts:

- **Week 1:** extract frames with `ffmpeg` + reconstruct video
- **Week 2:** setup `venv`, install `ultralytics`, run pretrained YOLO detection
- **Week 3:** inspect metrics + semantic segmentation concepts
- **Week 4:** understand YOLO dataset meta files + labeling workflow (label-studio)
- **Week 5:** prepare labels, scale images, train, predict on test, and generate final output video
- **Road_pothole_Detection:** Detects the potholes on road using label studio

---

## End-to-end pipeline

This repo is organized to reflect the internship tasks:

### Week 1 — Video frames + reconstruction

- Download a short YouTube video.
- Extract frames using `ffmpeg`.
- Reconstruct a 1-minute video from frames (same FPS).
- Merge new audio into the reconstructed video.

### Week 2 — Environment + YOLO pretrained detection

- Create a Python virtual environment with `venv`.
- Install `ultralytics`.
- Run pretrained YOLO object detection to generate example outputs.

### Week 3 — Performance + segmentation (concept + code)

- Inspect metrics produced by YOLO runs.
- Explore semantic segmentation (pixelwise object coloring).

### Week 4 — YOLO dataset meta + labeling

- Understand dataset YAML + label format.
- Use **label-studio** to generate YOLO-format labels (`.txt`) and metadata (`data.yaml`, `train.txt`, `val.txt`).

### Week 5 — Scale images + train/test + final video

- Scale images to training resolution (preserve aspect ratio).
- Train YOLO on the labeled dataset.
- Predict on test images and stitch final videos.

> The exact dataset/scripts you executed for Week 5 in this repo are stored under the `week 5/` directory.

---

## What’s included in this repository

1. Frame extraction + dataset splitting scripts (Week 5 notes and examples).
2. YOLO training configuration (`data.yml` / dataset YAML, args).
3. Image scaling commands and notes.
4. Train / predict commands and example outputs.
5. Final video output artifacts.

---

## Folder structure (matches your Week 5 outputs)

```
Computer-Vision/
├──Road_pothole_Detection/
  ├── Data_Extraction/
  │   ├── road.mp4
  │   ├── road.yaml
  │   ├── extract_frames.py
  │   ├── split_dataset.py
  |   ├── train.txt / val.txt / test.txt
  |   ├── images/train|val|test/
  |   └── labels/train|val|test/       # YOLO label .txt files (class + normalized box)
  │   └── dataset/
  │       └── raw_images/
  │
  ├── Data_scaling/
  │   └── scaling_command.md                          # ffmpeg scaling commands
  │   └── images/*_scaled/              # scaled images output (example)
  │
  ├── Training/
  │   └── training_command.md
  │   └── train/
  │       └── weights/best.pt   # trained model output
  |   └── results*.png / results.csv / curves...
  │
  ├── Testing/
  │   └── predict-*/  
  │   └── testing_command.md
  │
  └── Final_video/
      ├── output_road.mp4  
      └── output_command.md
├── week 1/
├── week 2/
├── week 3/
├── week 4/
└── week 5/
    ├── Task1 - Data _Extraction/
    │   ├── traffic.mp4
    │   ├── extract_frames.py
    │   ├── split_dataset.py
    │   ├── car_bus_dataset.yaml           # dataset config used by YOLO
    │   ├── train.txt / val.txt / test.txt
    │   ├── images/train|val|test/
    │   └── labels/train|val|test/       # YOLO label .txt files (class + normalized box)
    │
    ├── Task2 - Scaling/
    │   └── scaling_command.md                          # ffmpeg scaling commands
    │   └── images/*_scaled/              # scaled images output (example)
    │
    ├── Task3 - Training/
    │   ├── args.yaml
    │   ├── training_command.md
    │   └── weights/                      # e.g., best.pt, last.pt
    │   └── results*.png / results.csv / curves...
    │
    ├── Task4 - Testing/
    │   ├── testing_command.md
    │   └── predict-*/                    # saved prediction frames
    │
    └── Task5 - Final_Output/
        ├── traffic.mp4                  # final annotated/rebuilt video
        └── output_command.md
├── gitignore 
├── Readme.md
├── requirements.txt
```

> Notes:
>
> - YOLO expects labels in `labels/<split>/` with the same base filename as the corresponding images in `images/<split>/`.
> - Your Week 5 dataset uses a **2-class** setup (see `car_bus_dataset.yaml`).

---

## Prerequisites

- **Python**: 3.11
- **ffmpeg**: Required for video encoding/decoding in the Colab notebook and local video processing.
  - _macOS_: `brew install ffmpeg`
  - _Ubuntu/Debian_: `sudo apt-get install ffmpeg`
  - _Windows_: [Download from ffmpeg.org](https://ffmpeg.org/download.html)
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

### 3. Label Studio setup (import images + export YOLO labels)

This repo follows the Week 4 labeling workflow: you manually annotate images in **label-studio**, then export YOLO-format bounding-box labels.

#### 3.1 Create a separate virtual environment for label-studio

> Do NOT install label-studio inside your YOLO/ultralytics environment.

```bash
python3 -m venv labelstudio-env
source labelstudio-env/bin/activate
pip install -U label-studio
```

Start the server:

```bash
label-studio
```

Open in browser:

- http://localhost:8080

#### 3.2 Create a project and choose labels

For this repo’s dataset (`car_bus_dataset.yaml`), use 2 classes:

- `bus`
- `car`

Create bounding-box annotations for these classes.

#### 3.3 Import images for annotation (train + val)

In the label-studio UI, add tasks/images from your folders:

- `week 5/Task1 - Data _Extraction/images/train/`
- `week 5/Task1 - Data _Extraction/images/val/`

#### 3.4 Annotate

- Use the rectangle/bounding-box tool.
- Annotate all objects in the images.

#### 3.5 Export YOLO labels

Export the labeled dataset in **YOLO detection** format (normalized `.txt` per image).

Place exported label files into:

- `week 5/Task1 - Data _Extraction/labels/train/`
- `week 5/Task1 - Data _Extraction/labels/val/`

> Ensure exported label filenames match the image base filenames (e.g., `frame_001.jpg` ↔ `frame_001.txt`).

---

### 4. Train / Detect

The dataset is configured via `People_Detection/data.yml`:

```yaml
path: /Users/divyanjaligopisetty/Computer-Vision/week 5/Task1 - Data _Extraction
train: images/train
val: images/val
test: images/test
names:
  0: bus
  1: car
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

| Key     | Value                              |
| ------- | ---------------------------------- |
| `path`  | Root directory of the dataset      |
| `train` | Relative path to training images   |
| `val`   | Relative path to validation images |
| `names` | Class index-to-name mapping        |

Make sure your label files (`.txt`) are placed under `People_Detection/dataset/labels/train/` and `labels/val/` with the same filenames as the images.

---


# Road Pothole Detection (YOLO)

This repo contains the end-to-end pipeline used in **Road_pothole_detection**: **video → frames → dataset → training → prediction → final video** using **Ultralytics YOLO**.

---

## Pipeline (as done in `Road_pothole_Detection/`)

### 1. Frame extraction

Extract frames from `road.mp4`.

```bash
python Road_pothole_Detection/Data_Extraction/extract_frames.py
```

- Writes frames into: `Road_pothole_Detection/Data_Extraction/dataset/raw_images/` (see script: `extract_frames.py`)

### 2. Create train/val/test splits + YOLO label structure

Split images and copy matching YOLO `.txt` labels into the expected folder structure.

```bash
python Road_pothole_Detection/Data_Extraction/split_dataset.py
```

- Uses YOLO label filenames with the same stem as images.
- Output folders are expected under `Road_pothole_Detection/Data_Extraction/images/*` and `Road_pothole_Detection/Data_Extraction/labels/*`.
### 3. Label Studio setup (import images + export YOLO labels)

This repo follows the Week 4 labeling workflow: you manually annotate images in **label-studio**, then export YOLO-format bounding-box labels.

#### 3.1 Create a separate virtual environment for label-studio

> Do NOT install label-studio inside your YOLO/ultralytics environment.

```bash
python3 -m venv labelstudio-env
source labelstudio-env/bin/activate
pip install -U label-studio
```

Start the server:

```bash
label-studio
```

Open in browser:

- http://localhost:8080

#### 3.2 Create a project and choose labels

For this repo’s dataset (`road.yaml`), use 1 class:

- `pothole`


Create bounding-box annotations for these classes.

Label Studio Interface:

  <View>
    <Image name="image" value="$image"/>

    <RectangleLabels name="label" toName="image">
      <Label value="road_damage" background="red"/>
    </RectangleLabels>
  </View>

#### 3.3 Import images for annotation (train + val)

In the label-studio UI, add tasks/images from your folders:

- `week 5/Task1 - Data _Extraction/images/train/`
- `week 5/Task1 - Data _Extraction/images/val/`

#### 3.4 Annotate

- Use the rectangle/bounding-box tool.
- Annotate all objects in the images.

#### 3.5 Export YOLO labels

Export the labeled dataset in **YOLO detection** format (normalized `.txt` per image).

Place exported label files into:

- `week 5/Task1 - Data _Extraction/labels/train/`
- `week 5/Task1 - Data _Extraction/labels/val/`

> Ensure exported label filenames match the image base filenames (e.g., `frame_001.jpg` ↔ `frame_001.txt`).

---

### 4. Train / Detect

The dataset is configured via `People_Detection/data.yml`:

```yaml
path: /Users/divyanjaligopisetty/Computer-Vision/Road_pothole_Detection/Data_Extraction

train: images/train
val: images/val
test: images/test

names:
  0: pothole
```

**Quick inference example** (from the `week/` directory):

```bash
cd week
python detect.py
```

### 4. Train (Ultralytics YOLO)

Training command:

```bash
yolo detect train \
  data=Road_pothole_Detection/Data_Extraction/road.yaml \
  model=yolo11n.pt \
  epochs=50 \
  imgsz=384 \
  batch=8
```

This matches `Road_pothole_Detection/Training/training_command.md`.

### 5. Predict on test images

```bash
yolo detect predict \
  model=Road_pothole_Detection/Training/train/weights/best.pt \
  source=Road_pothole_Detection/Data_Extraction/images/test \
  conf=0.10 \
  save=True
```

This matches `Road_pothole_Detection/Testing/testing_command.md`.

### 6. Predict on a whole video (final output)

```bash
yolo detect predict \
  model=Road_pothole_Detection/Training/train/weights/best.pt \
  source=Road_pothole_Detection/Data_Extraction/road.mp4 \
  conf=0.10 \
  show_labels=True \
  show_conf=True \
  save=True
```

This matches `Road_pothole_Detection/Final_video/output_command.md`.


> Notes:
> - YOLO detection labels are expected as normalized `.txt` files (class id + normalized box coords) and must match image stems.
> - The dataset YAML defines **one class**: `pothole` (`names: {0: pothole}`) in `road.yaml`.

---

## Prerequisites

- **Python**: 3.11
- **ffmpeg** (required for some video workflows)
  - macOS: `brew install ffmpeg`
- **GPU**: for faster training/inference(in colab based work)

---

## Install

```bash
pip install -r requirements.txt
```
