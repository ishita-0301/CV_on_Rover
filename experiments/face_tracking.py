"""Face tracking (learning exercise, on-screen only).

Detects a face with cvzone's MediaPipe FaceDetector and draws a crosshair that
follows it around the frame. This was written to get familiar with MediaPipe and
OpenCV - it does not drive any hardware and is not part of the rover.
"""

import sys
from pathlib import Path

import cv2
from cvzone.FaceDetectionModule import FaceDetector

# Make the shared config importable regardless of the current working directory.
sys.path.append(str(Path(__file__).resolve().parent))
import config

cap = cv2.VideoCapture(config.CAMERA_INDEX)
ws, hs = config.FRAME_WIDTH, config.FRAME_HEIGHT
cap.set(3, ws)
cap.set(4, hs)

if not cap.isOpened():
    print("Camera couldn't be accessed!")
    exit()

detector = FaceDetector()

while True:
    success, img = cap.read()
    if not success:
        break

    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        fx, fy = bboxs[0]["center"]
        cv2.circle(img, (fx, fy), 80, (0, 0, 255), 2)
        cv2.circle(img, (fx, fy), 15, (0, 0, 255), cv2.FILLED)
        cv2.line(img, (0, fy), (ws, fy), (0, 0, 0), 2)   # horizontal crosshair
        cv2.line(img, (fx, 0), (fx, hs), (0, 0, 0), 2)   # vertical crosshair
        cv2.putText(img, "FACE LOCKED", (850, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    else:
        cv2.putText(img, "NO FACE", (880, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

    cv2.imshow("Face Tracking (press q to quit)", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
