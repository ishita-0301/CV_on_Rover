"""Video channel (rover side).

Captures the rover's camera and streams JPEG frames to the controller Pi. Each
frame is sent as a 4-byte big-endian length header followed by the JPEG bytes.

Prefers Picamera2 (the Raspberry Pi camera stack); falls back to any OpenCV
capture device (e.g. a USB webcam) if Picamera2 is unavailable.
"""

import socket
import struct
import time

import cv2

import config


def open_camera():
    """Return (read, close): read() -> BGR frame, preferring the Pi camera."""
    try:
        from picamera2 import Picamera2

        picam = Picamera2()
        picam.configure(
            picam.create_video_configuration(
                main={"size": (config.FRAME_WIDTH, config.FRAME_HEIGHT),
                      "format": "RGB888"}
            )
        )
        picam.start()
        time.sleep(0.5)  # let auto-exposure settle

        def read():
            frame = picam.capture_array()
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        return read, picam.close

    except Exception:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

        def read():
            ok, frame = cap.read()
            return frame if ok else None

        return read, cap.release


def stream_to(conn, read):
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), config.JPEG_QUALITY]
    frame_interval = 1.0 / config.TARGET_FPS
    with conn:
        while True:
            start = time.time()
            frame = read()
            if frame is None:
                continue
            ok, jpeg = cv2.imencode(".jpg", frame, encode_params)
            if not ok:
                continue
            payload = jpeg.tobytes()
            try:
                conn.sendall(struct.pack(">I", len(payload)) + payload)
            except (BrokenPipeError, ConnectionResetError):
                break  # controller went away
            elapsed = time.time() - start
            if elapsed < frame_interval:
                time.sleep(frame_interval - elapsed)


def serve():
    read, close_camera = open_camera()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((config.LISTEN_HOST, config.VIDEO_PORT))
    server.listen(1)
    print(f"[video] listening on {config.LISTEN_HOST}:{config.VIDEO_PORT}")
    try:
        while True:
            conn, addr = server.accept()
            print(f"[video] controller connected from {addr[0]}")
            stream_to(conn, read)
            print("[video] controller disconnected")
    finally:
        close_camera()
        server.close()


if __name__ == "__main__":
    serve()
