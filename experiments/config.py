"""Shared settings for the learning / familiarization scripts.

These scripts were written to get comfortable with OpenCV and MediaPipe and are
NOT part of the rover. See experiments/README.md.
"""

from pathlib import Path

EXPERIMENTS_DIR = Path(__file__).resolve().parent
HAAR_CASCADE = str(EXPERIMENTS_DIR / "models" / "haarcascade_frontalface_default.xml")

CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
