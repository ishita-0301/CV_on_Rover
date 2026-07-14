"""Run the controller Pi: hand-gesture control + live video viewer together.

The video viewer runs in a background thread while hand control owns the main
thread. Each opens its own OpenCV window.
"""

import threading

import hand_control
import video_client


def main():
    viewer = threading.Thread(target=video_client.main, name="video", daemon=True)
    viewer.start()
    hand_control.main()   # blocks until the operator presses 'q'


if __name__ == "__main__":
    main()
