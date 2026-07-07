"""Shared configuration for the CV-on-Rover vision scripts.

Central place for camera, Arduino serial and model-path settings so the
face-detection / face-tracking scripts don't hard-code them individually.
Edit the values below to match your own hardware.
"""

from pathlib import Path

# --- Paths -----------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = REPO_ROOT / "models"
HAAR_CASCADE = str(MODELS_DIR / "haarcascade_frontalface_default.xml")

# --- Camera ----------------------------------------------------------------
CAMERA_INDEX = 0        # default webcam
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# --- Arduino (pyfirmata / StandardFirmata) ---------------------------------
ARDUINO_PORT = "COM7"   # change to match your board, e.g. "/dev/ttyUSB0"
SERVO_PIN_X = 9         # horizontal pan servo  -> Arduino D9
SERVO_PIN_Y = 10        # vertical tilt servo   -> Arduino D10
SERVO_MIN_ANGLE = 0
SERVO_MAX_ANGLE = 180
