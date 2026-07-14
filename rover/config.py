"""Configuration for the rover-side Raspberry Pi.

The rover Pi drives the wheels through an L298N motor driver and streams its
camera back to the controller Pi. It hosts two TCP servers; the controller Pi
connects to them. Adjust the GPIO pins and ports to match your wiring and LAN.
"""

# --- Network ---------------------------------------------------------------
# 0.0.0.0 means "listen on every interface" so the controller Pi can reach the
# rover over Wi-Fi/Ethernet.
LISTEN_HOST  = "0.0.0.0"
COMMAND_PORT = 5001       # controller -> rover : drive commands (F/B/L/R/S)
VIDEO_PORT   = 5002       # rover -> controller : live camera stream (JPEG)

# --- Motor driver (L298N), Broadcom (BCM) GPIO numbering -------------------
# Left wheel bank
LEFT_FORWARD   = 17       # IN1
LEFT_BACKWARD  = 27       # IN2
LEFT_ENABLE    = 12       # ENA (enables the left H-bridge)
# Right wheel bank
RIGHT_FORWARD  = 23       # IN3
RIGHT_BACKWARD = 24       # IN4
RIGHT_ENABLE   = 13       # ENB (enables the right H-bridge)

DRIVE_SPEED = 0.8         # 0.0 - 1.0 duty cycle applied while moving

# --- Camera ----------------------------------------------------------------
FRAME_WIDTH  = 640
FRAME_HEIGHT = 480
JPEG_QUALITY = 70         # lower = smaller frames = smoother stream over Wi-Fi
TARGET_FPS   = 20
