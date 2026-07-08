# Computer Vision on Rover — Real-Time Face-Tracking Turret & YOLOv5 Classification on a Rocker-Bogie Rover

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)](https://opencv.org/)
[![Arduino](https://img.shields.io/badge/Arduino-Uno-teal?logo=arduino)](https://www.arduino.cc/)
[![YOLOv5](https://img.shields.io/badge/YOLOv5-Classification-orange)](https://github.com/ultralytics/yolov5)
[![License](https://img.shields.io/badge/License-AGPL--3.0-lightgrey)](THIRD_PARTY_NOTICES.md)

A **Python + Arduino** project that mounts a **self-aiming, face-tracking camera** on a **rocker-bogie rover**. A webcam detects faces in real time; the head physically pan-tilts on two servos to keep the face centered, while a separate motor-driver channel drives the six-wheel rocker-bogie chassis. An optional **YOLOv5** pipeline adds on-board image classification, training and validation.

> **Two independent subsystems, one rover:**
> 1. **Vision + turret** — OpenCV / cvzone face detection → servo pan-tilt (`vision/`, `hardware/pan_tilt_servo/`)
> 2. **Locomotion** — serial-driven L298N rocker-bogie drive (`hardware/rover_drive/`)
> 3. **Classification (optional)** — YOLOv5 predict / train / val (`classification/`, `yolov5/` submodule)

---

## Demo

▶ **[Watch the face-tracking demo](docs/CVDemo.mp4)** 

<video src="https://github.com/ishita-0301/CV_on_Rover/raw/main/docs/CVDemo.mp4" controls muted width="720"></video>

<!--
  The link above always works. For a guaranteed inline auto-playing player,
  drag-and-drop docs/CVDemo.mp4 into the GitHub web README editor (or a new
  Issue); GitHub returns a https://github.com/user-attachments/assets/… URL —
  paste it on its own line here to render an embedded player.
-->

```
[No Target]                  [TARGET LOCKED]
  ·  · ─── · ·                 ·  · ─── · ·
  ·  (      )  ·                ·  ( ◎  )  ·
  ·  ·     ·  ·     →           ·  · ─── · ·
  │                              │  Servo X: 112°
  │                              │  Servo Y:  98°
```

The crosshair physically follows the detected face at ~30 fps.

---

## How It Works

```
        Webcam Feed
             │
             ▼
   ┌────────────────────────┐
   │  Face Detection        │  ← cvzone FaceDetectionModule (MediaPipe)
   │  (real-time, ~30 fps)  │     or OpenCV Haar cascade
   └───────────┬────────────┘
               │  face center (fx, fy)
               ▼
   ┌────────────────────────┐
   │  Coordinate Mapping    │  ← np.interp → servo angle [0°–180°]
   └───────────┬────────────┘
               │  angles (X, Y)
               ▼
   ┌────────────────────────┐
   │  Arduino Uno           │  ← USB serial (pyfirmata / native sketch)
   │  D9  → Servo X (pan)   │
   │  D10 → Servo Y (tilt)  │
   └───────────┬────────────┘
               │
               ▼
        [ TARGET LOCKED ] — pan-tilt head aims the camera at the face
```

1. Each webcam frame is passed to the face detector.
2. The face-center pixel coordinates `(fx, fy)` are mapped to servo angles with `numpy.interp`.
3. The angles are streamed over USB serial to the Arduino.
4. The Arduino drives the two servos to physically aim the camera; the rover chassis is driven independently over the same serial link.

---

## Features

| Feature | Details | Code |
|---|---|---|
| **Face Detection** | OpenCV Haar cascade, no extra hardware needed | `vision/facedetection.py` |
| **Face Tracking** | Real-time pan-tilt via 2 servos, cvzone/MediaPipe detector | `vision/facetracking.py` |
| **Pan-Tilt Firmware** | Native serial servo sketch (Firmata alternative) | `hardware/pan_tilt_servo/` |
| **Rover Locomotion** | L298N differential drive for a 6-wheel rocker-bogie | `hardware/rover_drive/` |
| **Object Classification** | YOLOv5 inference on webcam / image / video / stream | `classification/predict.py` |
| **Training Pipeline** | Train & validate custom YOLOv5 classifiers | `classification/train.py`, `val.py` |
| **Shared Config** | One place for camera index, serial port & servo pins | `vision/config.py` |

---

## Repository Structure

```
CV_on_Rover/
├── vision/
│   ├── facedetection.py          # Haar-cascade face detection (OpenCV only)
│   ├── facetracking.py           # Real-time tracking → Arduino servos (pyfirmata)
│   └── config.py                 # Camera / serial-port / servo-pin settings
├── classification/
│   ├── predict.py                # YOLOv5 classification inference
│   ├── train.py                  # YOLOv5 classifier training
│   └── val.py                    # YOLOv5 classifier validation
├── yolov5/                       # Ultralytics YOLOv5 (git submodule)
├── hardware/
│   ├── pan_tilt_servo/           # Native serial servo sketch (.ino)
│   ├── rover_drive/              # L298N rocker-bogie drive sketch (.ino)
│   └── firmata/                  # StandardFirmata upload notes
├── models/
│   └── haarcascade_frontalface_default.xml
├── notebooks/
│   └── tutorial.ipynb            # YOLOv5 classification walkthrough
├── docs/
│   └── wiring_schematic.jpg      # Arduino + servo + motor wiring diagram
├── scripts/
│   ├── setup.sh                  # Init submodule + install dependencies
│   └── run_classify.sh           # Convenience wrapper for inference
├── requirements.txt
└── THIRD_PARTY_NOTICES.md        # YOLOv5 (AGPL-3.0), OpenCV, cvzone licenses
```

---

## Hardware Setup

| Component | Connection |
|---|---|
| Arduino Uno | USB to host PC |
| USB webcam | any UVC webcam |
| Servo X (pan) | signal → **D9** |
| Servo Y (tilt) | signal → **D10** |
| Servos power | external **5 V** supply + common ground (don't power two servos from the Arduino 5 V pin) |

**Rocker-bogie drive (L298N)** — the six wheels are ganged into a left and a right bank and driven differentially:

| L298N pin | Arduino | Purpose |
|---|---|---|
| ENA | **D5** (PWM) | left-bank speed |
| IN1 / IN2 | **D7 / D8** | left-bank direction |
| ENB | **D6** (PWM) | right-bank speed |
| IN3 / IN4 | **D9 / D10** | right-bank direction |
| 12V / GND | battery | motor supply + common ground |

> ℹ️ The pan-tilt servos and the rover drive both reference D9/D10 in their default sketches — run them on **separate Arduinos**, or remap the pins in the sketch, if you use both at once.

See [`docs/wiring_schematic.jpg`](docs/wiring_schematic.jpg) for the full diagram.

---

## Installation

Clone **with submodules** (YOLOv5 lives in the `yolov5/` submodule):

```bash
git clone --recurse-submodules https://github.com/ishita-0301/CV_on_Rover.git
cd CV_on_Rover
```

Already cloned without `--recurse-submodules`? Pull it in:

```bash
git submodule update --init --recursive
```

Install dependencies (one step):

```bash
bash scripts/setup.sh          # inits submodule + installs both requirement sets
```

…or manually:

```bash
pip install -r requirements.txt
pip install -r yolov5/requirements.txt   # only needed for the classification pipeline
```

---

## Usage

Before running the hardware scripts, set your board in [`vision/config.py`](vision/config.py):

```python
ARDUINO_PORT = "COM7"     # Windows, or "/dev/ttyUSB0" on Linux/Mac
CAMERA_INDEX = 0
SERVO_PIN_X  = 9
SERVO_PIN_Y  = 10
```

### 1. Face Detection (no hardware needed)
```bash
python vision/facedetection.py
```
Opens the webcam and draws boxes around detected faces. Press **q** to quit.

### 2. Face Tracking with servos
Upload **StandardFirmata** to the Arduino (see [`hardware/firmata/StandardFirmata_note.md`](hardware/firmata/StandardFirmata_note.md)), then:
```bash
python vision/facetracking.py
```
Prefer a custom firmware? Flash [`hardware/pan_tilt_servo/pan_tilt_servo.ino`](hardware/pan_tilt_servo/pan_tilt_servo.ino) and send `"<x>,<y>\n"` serial commands instead.

### 3. Rover locomotion
Flash [`hardware/rover_drive/rover_drive.ino`](hardware/rover_drive/rover_drive.ino), then drive it with single-character serial commands at 9600 baud:

| Command | Action |
|---|---|
| `F` / `B` | forward / backward |
| `L` / `R` | pivot left / right |
| `S` | stop |
| `V<0-255>` | set speed, e.g. `V180` |

### 4. YOLOv5 Object Classification
```bash
# via the wrapper
scripts/run_classify.sh --weights yolov5s-cls.pt --source 0        # webcam
scripts/run_classify.sh --weights yolov5s-cls.pt --source img.jpg  # image

# or directly
python classification/predict.py --weights yolov5s-cls.pt --source 0
```

### 5. Train / validate a custom classifier
```bash
python classification/train.py --model yolov5s-cls.pt --data imagenette160 --epochs 50 --img 224
python classification/val.py   --weights runs/train-cls/exp/weights/best.pt --data imagenette160
```

A step-by-step walkthrough is in [`notebooks/tutorial.ipynb`](notebooks/tutorial.ipynb).

---

## Requirements

```
opencv-python>=4.5     # image capture & Haar detection
numpy                  # coordinate mapping
cvzone>=1.4.1          # MediaPipe FaceDetectionModule
mediapipe
pyfirmata              # Arduino serial (StandardFirmata)
# classification only:
torch, torchvision, and the rest of yolov5/requirements.txt
```

---

## Licenses & Attribution

This repo bundles third-party components — see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).

- **Ultralytics YOLOv5** (`yolov5/` submodule + `classification/*.py`) — **AGPL-3.0**. Because AGPL is copyleft, any distribution or network use that includes these files must comply with AGPL-3.0.
- **OpenCV Haar cascade** (`models/`) — BSD-3-Clause.
- **cvzone** `FaceDetectionModule` — MIT.

The original vision and hardware code in this repository was written for this project.

## Acknowledgements

- [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5) — classification pipeline
- [cvzone](https://github.com/cvzone/cvzone) — MediaPipe face-detection wrapper
- [OpenCV](https://opencv.org/) — Haar cascades and video I/O
