# CV on Rover — Hand-Gesture-Controlled Rover with Live Camera Streaming

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-2%20units-C51A4A?logo=raspberrypi)](https://www.raspberrypi.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hands-orange?logo=google)](https://developers.google.com/mediapipe)

Drive a rover with your **hand**. A **controller Raspberry Pi** watches the
operator's hand through a camera, uses **MediaPipe** to recognise the gesture,
and sends a movement command over Wi-Fi to a second **Raspberry Pi on the
rover**. The rover Pi drives its wheels through an **L298N** motor driver and
**streams its own camera feed back** to the controller — so the operator sees
what the rover sees, in real time.

> **Two Raspberry Pis, talking over the network:**
> 1. **Controller Pi** — hand-gesture recognition → drive commands, plus a live viewer for the rover's camera (`controller/`)
> 2. **Rover Pi** — receives commands → GPIO motor control, and streams its camera back (`rover/`)

---

## Demo

▶ **[Watch the project demo](https://drive.google.com/file/d/15q0fyuLc9INrZ4JbzMzm7QIVIy_Q2SoV/view?usp=sharing)** (Google Drive)

---

## Gesture controls

The controller reads your hand pose (the image is mirrored, so lean toward the
screen's side you want to turn):

| Gesture | Command | Rover action |
|---|---|---|
| 🖐️ open palm, upright | `F` | forward |
| ✊ closed fist, upright | `B` | backward |
| 👉 hand leaning right | `R` | turn right |
| 👈 hand leaning left | `L` | turn left |
| ✋ no hand | `S` | stop |

---

## How it works

```
        Controller Pi                              Rover Pi
   ┌──────────────────────┐                  ┌──────────────────────┐
   │  camera → MediaPipe   │   command (TCP)  │  command server       │
   │  Hands → finger count │ ───────────────► │  → L298N via GPIO     │
   │  → F/B/L/R/S          │   "F\n" …        │  → drives the wheels  │
   │                       │                  │                       │
   │  video viewer         │ ◄─────────────── │  camera → JPEG        │
   │  (shows rover camera) │   JPEG frames    │  → video server       │
   └──────────────────────┘   (TCP stream)    └──────────────────────┘
```

- **Command channel** (`controller → rover`): newline-terminated single-char
  commands. The rover has a **watchdog** that stops the wheels if no command
  arrives for ~1 s, so it halts on disconnect.
- **Video channel** (`rover → controller`): each frame is a 4-byte length
  header followed by JPEG bytes.

---

## Repository structure

```
CV_on_Rover/
├── controller/                 # Controller Pi (operator's base station)
│   ├── hand_control.py         # MediaPipe hand gestures → drive commands (TCP)
│   ├── video_client.py         # receive + display the rover's live stream
│   ├── main.py                 # run both together
│   └── config.py               # rover IP, ports, gesture→command map
├── rover/                      # Rover Pi
│   ├── motor.py                # L298N differential drive via gpiozero
│   ├── command_server.py       # receive commands → drive the motors
│   ├── video_server.py         # camera (Picamera2 / OpenCV) → JPEG stream
│   ├── main.py                 # run both servers together
│   └── config.py               # GPIO pins, ports, camera settings
├── experiments/                # OpenCV/MediaPipe LEARNING code — NOT the rover
│   ├── face_detection.py       # Haar-cascade face detection
│   ├── face_tracking.py        # MediaPipe face-follow crosshair (on-screen only)
│   ├── classification/         # YOLOv5 image-classification experiments
│   └── README.md
├── yolov5/                     # Ultralytics YOLOv5 (submodule, experiments only)
├── scripts/setup.sh
├── requirements.txt
└── THIRD_PARTY_NOTICES.md
```

---

## Hardware

| Part | Notes |
|---|---|
| **2 × Raspberry Pi** | one on the rover, one as the controller (same Wi-Fi/LAN) |
| **Camera** | rover camera (Pi Camera Module or USB) + operator camera on the controller |
| **L298N motor driver** | dual H-bridge driving the rocker-bogie left/right wheel banks |
| **DC gear motors + battery** | motor supply into the L298N (share a common ground with the Pi) |

**L298N ↔ Rover Pi wiring** (BCM GPIO — see `rover/config.py`):

| L298N pin | Rover Pi (BCM) | Purpose |
|---|---|---|
| ENA | **GPIO 12** | enable left bank |
| IN1 / IN2 | **GPIO 17 / 27** | left-bank direction |
| ENB | **GPIO 13** | enable right bank |
| IN3 / IN4 | **GPIO 23 / 24** | right-bank direction |
| 12V / GND | battery | motor supply + **common ground** with the Pi |

> ⚠️ Never back-power the Pi from the motor battery. Keep motor power on the
> L298N, logic power on the Pi, and tie their grounds together.

---

## Setup

On **each** Pi, clone the repo and install the dependencies for that role.

```bash
git clone https://github.com/ishita-0301/CV_on_Rover.git
cd CV_on_Rover
```

**Rover Pi:**
```bash
pip install opencv-python numpy gpiozero
sudo apt install python3-picamera2      # Pi Camera stack (Raspberry Pi OS)
```

**Controller Pi:**
```bash
pip install opencv-python numpy mediapipe
```

Then point the controller at the rover — edit `controller/config.py`:
```python
ROVER_HOST = "192.168.1.50"   # the rover Pi's IP address on your LAN
```
(You can find it on the rover with `hostname -I`.)

---

## Run it

**1. On the rover Pi** — start the command + video servers:
```bash
python rover/main.py
```

**2. On the controller Pi** — start hand control + the live viewer:
```bash
python controller/main.py
```

Hold up fingers in front of the controller's camera to drive the rover; the
rover's camera feed opens in its own window. Press **q** to quit.

---

## Experiments (learning code)

The `experiments/` folder holds the OpenCV/MediaPipe **face detection**,
**face tracking**, and **YOLOv5 classification** scripts. These were written to
get familiar with the libraries and are **not part of the rover** — see
[`experiments/README.md`](experiments/README.md).

---

## Licenses & attribution

- The rover code (`controller/`, `rover/`) and the face scripts were written for
  this project.
- **Ultralytics YOLOv5** (`yolov5/` submodule + `experiments/classification/*.py`)
  is **AGPL-3.0**; see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
- **OpenCV Haar cascade** — BSD-3-Clause. **cvzone** — MIT.
