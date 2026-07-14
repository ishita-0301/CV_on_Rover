"""Live video viewer (controller side).

Connects to the rover Pi's video server and displays the incoming stream. Each
frame arrives as a 4-byte big-endian length header followed by JPEG bytes.
"""

import socket
import struct

import cv2
import numpy as np

import config


def recv_exactly(sock, n):
    """Read exactly n bytes from the socket, or return None on disconnect."""
    buffer = bytearray()
    while len(buffer) < n:
        chunk = sock.recv(n - len(buffer))
        if not chunk:
            return None
        buffer.extend(chunk)
    return bytes(buffer)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((config.ROVER_HOST, config.VIDEO_PORT))
    print(f"[video] connected to rover at {config.ROVER_HOST}:{config.VIDEO_PORT}")

    try:
        while True:
            header = recv_exactly(sock, 4)
            if header is None:
                break
            (length,) = struct.unpack(">I", header)
            payload = recv_exactly(sock, length)
            if payload is None:
                break
            frame = cv2.imdecode(np.frombuffer(payload, np.uint8), cv2.IMREAD_COLOR)
            if frame is None:
                continue
            cv2.imshow("Rover Camera (press q to quit)", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        sock.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
