# Experiments — OpenCV / MediaPipe familiarization

These scripts are **not part of the rover**. They were written early on to get
comfortable with OpenCV and MediaPipe (and, separately, to try out YOLOv5
image classification) *before* building the actual hand-gesture-controlled
rover. They are kept here for reference and history.

## Face detection — `face_detection.py`
Classic OpenCV Haar-cascade face detection on a webcam feed; draws a box around
each detected face and prints the count.

```bash
python experiments/face_detection.py
```

## Face tracking — `face_tracking.py`
Uses cvzone's MediaPipe `FaceDetector` to draw a crosshair that follows a face
around the frame. On-screen only — no servos, no hardware.

```bash
python experiments/face_tracking.py
```

▶ Early face-tracking clip: [`CVDemo.mp4`](CVDemo.mp4)

## YOLOv5 image classification — `classification/`
A small exploration of image classification with Ultralytics YOLOv5 (inference,
training and validation wrappers). Requires the `yolov5/` git submodule:

```bash
git submodule update --init --recursive
pip install -r ../yolov5/requirements.txt

python experiments/classification/predict.py --weights yolov5s-cls.pt --source 0
```

See [`classification/tutorial.ipynb`](classification/tutorial.ipynb) for a walkthrough.
