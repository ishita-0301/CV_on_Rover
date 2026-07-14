"""Hand-gesture drive control (controller side).

Uses MediaPipe Hands to count how many fingers the operator is holding up and
maps that to a single-character drive command, which is streamed to the rover
Pi over TCP. Run this on the controller Pi with a camera pointed at your hand.

    1 finger  -> F (forward)     3 fingers -> L (left)
    2 fingers -> B (backward)    4 fingers -> R (right)
    fist / open palm / no hand -> S (stop)
"""

import socket
import time

import cv2
import mediapipe as mp

import config

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Landmark ids of the four finger tips and the thumb tip (MediaPipe Hands).
FINGER_TIPS = [8, 12, 16, 20]
THUMB_TIP = 4


def count_fingers(hand_landmarks, handedness_label):
    lm = hand_landmarks.landmark
    fingers = 0

    # Four fingers: a finger is "up" when its tip is above (smaller y) the PIP
    # joint two landmarks below it.
    for tip in FINGER_TIPS:
        if lm[tip].y < lm[tip - 2].y:
            fingers += 1

    # Thumb: compare x against the IP joint; direction depends on which hand.
    if handedness_label == "Right":
        if lm[THUMB_TIP].x < lm[THUMB_TIP - 1].x:
            fingers += 1
    else:
        if lm[THUMB_TIP].x > lm[THUMB_TIP - 1].x:
            fingers += 1

    return fingers


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
                label = result.multi_handedness[0].classification[0].label
                fingers = count_fingers(hand, label)
                command = config.GESTURE_COMMANDS.get(fingers, "S")
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f"{fingers} fingers -> {command}", (10, 40),
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
