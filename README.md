# CV on Rover — Real-Time Face Tracking Turret & YOLOv5 Object Detection on a Rocker-Bogie Rover

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)](https://opencv.org/)
[![Arduino](https://img.shields.io/badge/Arduino-Compatible-teal?logo=arduino)](https://www.arduino.cc/)
[![YOLOv5](https://img.shields.io/badge/YOLOv5-Classification-orange)](https://github.com/ultralytics/yolov5)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

A Python + Arduino project that mounts a **self-aiming face-tracking camera** on a **rocker-bogie Mars rover**. The camera pan-tilts in real time to lock onto detected faces using OpenCV and dual servo motors, while YOLOv5 handles on-board object classification.

```
Webcam Feed
     │
     ▼
┌──────────────────────┐
│  Face Detection       │  ← cvzone FaceDetectionModule (Haar + MediaPipe)
│  (Real-Time, ~30fps) │
└──────────┬───────────┘
           │  face center (x, y)
           ▼
┌──────────────────────┐
│  Coordinate Mapping  │  ← np.interp → servo angle [0°–180°]
└──────────┬───────────┘
           │  PWM signal
           ▼
┌──────────────────────┐
│  Arduino (pyfirmata) │  ← USB serial to Arduino Uno
│  Pin 9 → Servo X     │
│  Pin 10 → Servo Y    │
└──────────────────────┘
           │
           ▼
      [ TARGET LOCKED ]
      Pan-tilt head physically
      moves to track the face
```

## Features

| Feature | Details |
|---|---|
| **Face Tracking** | Real-time pan-tilt via 2 servo motors on an Arduino |
| **Face Detection** | Haar Cascade (`facedetection.py`) + cvzone MediaPipe model (`facetracking.py`) |
| **Object Classification** | YOLOv5 inference on webcam/video/image streams (`predict.py`) |
| **Hardware** | Arduino Uno, 2× SG90 servos, rocker-bogie rover chassis |
| **Training Pipeline** | `train.py` + `val.py` for custom YOLOv5 classification models |

## Demo

```
[No Target]                  [TARGET LOCKED]
  ·  · ─── · ·                 ·  · ─── · ·
  ·  (      )  ·                ·  ( ◎  )  ·
  ·  ·     ·  ·     →           ·  · ─── · ·
  │                              │  Servo X: 112°
  │                              │  Servo Y: 98°
```

The crosshair physically follows the detected face at ~30fps.

## Hardware Setup

- Arduino Uno (connected via USB)
- 2× SG90 servo motors
  - Servo X (horizontal pan) → Arduino **pin 9**
  - Servo Y (vertical tilt) → Arduino **pin 10**
- Any USB webcam

See [`wiring schematic.jpg`](wiring%20schematic.jpg) for the full wiring diagram.

## Installation

```bash
git clone https://github.com/ishita-0301/CV_on_Rover.git
cd CV_on_Rover
pip install cvzone pyfirmata torch torchvision ultralytics
```

## Usage

### Face Detection (no hardware needed)
```bash
python facedetection.py
```
Opens your webcam and draws bounding boxes around detected faces.

### Face Tracking with Arduino Servos
```bash
# Edit facetracking.py line 12: port = "COM7"  ← change to your Arduino port
python facetracking.py
```

### YOLOv5 Object Classification
```bash
# Webcam
python predict.py --weights yolov5s-cls.pt --source 0

# Image
python predict.py --weights yolov5s-cls.pt --source img.jpg
```

### Train a Custom Classifier
```bash
python train.py --data your_dataset.yaml --epochs 50
python val.py   --weights runs/train/exp/weights/best.pt
```

## Project Structure

```
CV_on_Rover/
├── facedetection.py          # Haar Cascade face detection (OpenCV only)
├── facetracking.py           # Real-time face tracking → Arduino servo control
├── predict.py                # YOLOv5 classification inference
├── train.py                  # YOLOv5 model training
├── val.py                    # YOLOv5 model validation
├── tutorial.ipynb            # Step-by-step tutorial notebook
├── haarcascade_frontalface_default.xml
└── wiring schematic.jpg      # Arduino + servo wiring diagram
```

## Requirements

```
cvzone>=1.4.1       # includes opencv-python and mediapipe
pyfirmata           # Arduino serial communication
torch
torchvision
ultralytics         # YOLOv5
```

## How It Works

1. Each video frame is passed to the face detector.
2. The face center pixel coordinates `(fx, fy)` are mapped to servo angles using `numpy.interp`.
3. The angles are sent over USB serial to the Arduino via `pyfirmata`.
4. The Arduino drives the two SG90 servos to physically aim the camera at the face.
