"""Configuration for the controller-side Raspberry Pi (the operator's base).

The controller Pi watches the operator's hand with its own camera, turns hand
gestures into drive commands, sends them to the rover, and displays the live
video coming back from the rover's camera. Set ROVER_HOST to the rover Pi's IP.
"""

# --- Rover connection ------------------------------------------------------
ROVER_HOST   = "192.168.1.50"   # <-- rover Pi's IP address on your LAN
COMMAND_PORT = 5001             # must match rover/config.py
VIDEO_PORT   = 5002

# --- Operator camera (watches the hand) ------------------------------------
CAMERA_INDEX = 0
FRAME_WIDTH  = 640
FRAME_HEIGHT = 480

# --- Gesture recognition ---------------------------------------------------
# Hand pose -> single-character drive command:
#   open palm, upright   -> F (forward)
#   closed fist, upright -> B (backward)
#   hand leaning right   -> R (turn right)
#   hand leaning left    -> L (turn left)
#   no hand              -> S (stop)
TURN_ANGLE = 45        # a lean within this many degrees of horizontal = a turn
OPEN_FINGERS_MIN = 3   # >= this many extended fingers counts as an open palm
SEND_INTERVAL = 0.1    # seconds between command sends (10 Hz)
