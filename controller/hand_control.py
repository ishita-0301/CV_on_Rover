"""Hand-gesture drive control (controller side).

Uses MediaPipe Hands to read the operator's hand pose and maps it to a single-
character drive command, which is streamed to the rover Pi over TCP. Run this on
the controller Pi with a camera pointed at your hand.

    open palm  (upright)  -> F (forward)     hand leaning right -> R (turn right)
    closed fist(upright)  -> B (backward)    hand leaning left  -> L (turn left)
    no hand -> S (stop)

The image is mirrored, so leaning your hand toward the screen's right turns
right and toward the left turns left.
"""

import math
import socket
import time

import cv2
import mediapipe as mp

import config

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# MediaPipe Hands landmark ids: finger tips and their PIP joints.
FINGER_TIPS = [8, 12, 16, 20]
FINGER_PIPS = [6, 10, 14, 18]
WRIST = 0
MIDDLE_MCP = 9   # base of the middle finger


def extended_finger_count(lm):
    """How many of the four fingers are extended (tip above its PIP joint)."""
    return sum(1 for tip, pip in zip(FINGER_TIPS, FINGER_PIPS)
               if lm[tip].y < lm[pip].y)


def recognize_command(hand_landmarks):
    """Map a hand pose to a drive command (F/B/L/R)."""
    lm = hand_landmarks.landmark

    # Pointing direction of the hand: wrist -> base of the middle finger.
    dx = lm[MIDDLE_MCP].x - lm[WRIST].x
    dy = lm[MIDDLE_MCP].y - lm[WRIST].y      # image y grows downward
    angle = math.degrees(math.atan2(-dy, dx))  # 90 = up, 0 = right, +/-180 = left

    # A clear sideways lean is a turn, regardless of open/closed.
    if abs(angle) <= config.TURN_ANGLE:
        return "R"                            # leaning right  -> turn right
    if abs(angle) >= 180 - config.TURN_ANGLE:
        return "L"                            # leaning left   -> turn left

    # Roughly upright: open palm drives forward, closed fist reverses.
    if extended_finger_count(lm) >= config.OPEN_FINGERS_MIN:
        return "F"
    return "B"


def connect_to_rover():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((config.ROVER_HOST, config.COMMAND_PORT))
    print(f"[hand] connected to rover at {config.ROVER_HOST}:{config.COMMAND_PORT}")
    return sock


def main():
    sock = connect_to_rover()
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    last_send = 0.0
    last_command = None

    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame = cv2.flip(frame, 1)  # mirror so it feels natural
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            command = "S"  # default: no hand -> stop
            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                command = recognize_command(hand)
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                labels = {"F": "FORWARD", "B": "BACKWARD",
                          "L": "TURN LEFT", "R": "TURN RIGHT", "S": "STOP"}
                cv2.putText(frame, f"{command} - {labels[command]}", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "no hand -> STOP", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Send at a fixed rate, and immediately whenever the command changes.
            now = time.time()
            if command != last_command or now - last_send >= config.SEND_INTERVAL:
                try:
                    sock.sendall((command + "\n").encode())
                except (BrokenPipeError, ConnectionResetError):
                    print("[hand] lost connection to rover")
                    break
                last_send = now
                last_command = command

            cv2.imshow("Hand Control (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    try:
        sock.sendall(b"S\n")   # make sure the rover halts on exit
    except OSError:
        pass
    sock.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
