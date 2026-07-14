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

# --- Gesture -> command mapping --------------------------------------------
# Number of raised fingers -> single-character drive command.
GESTURE_COMMANDS = {
    1: "F",   # 1 finger  -> forward
    2: "B",   # 2 fingers -> backward
    3: "L",   # 3 fingers -> turn left
    4: "R",   # 4 fingers -> turn right
    0: "S",   # fist      -> stop
    5: "S",   # open palm -> stop
}
SEND_INTERVAL = 0.1   # seconds between command sends (10 Hz)
