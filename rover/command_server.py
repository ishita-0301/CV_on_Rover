"""Command channel (rover side).

Listens for one-character drive commands from the controller Pi and applies them
to the motors. Commands are newline-terminated ASCII:

    F  forward     B  backward
    L  turn left   R  turn right
    S  stop

A watchdog stops the rover if no command arrives for STOP_TIMEOUT seconds, so
the rover halts if the controller disconnects or the link drops.
"""

import socket

import config
from motor import Rover

STOP_TIMEOUT = 1.0   # seconds without a command -> stop


def dispatch(line, rover):
    if not line:
        return
    cmd = chr(line[0]).upper()
    actions = {
        "F": rover.forward,
        "B": rover.backward,
        "L": rover.turn_left,
        "R": rover.turn_right,
        "S": rover.stop,
    }
    action = actions.get(cmd)
    if action:
        action()


def handle(conn, rover):
    conn.settimeout(STOP_TIMEOUT)
    buffer = b""
    with conn:
        while True:
            try:
                chunk = conn.recv(64)
            except socket.timeout:
                rover.stop()           # watchdog: no fresh command -> halt
                continue
            if not chunk:
                break                  # controller closed the connection
            buffer += chunk
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                dispatch(line.strip(), rover)
    rover.stop()


def serve():
    rover = Rover()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((config.LISTEN_HOST, config.COMMAND_PORT))
    server.listen(1)
    print(f"[command] listening on {config.LISTEN_HOST}:{config.COMMAND_PORT}")
    try:
        while True:
            conn, addr = server.accept()
            print(f"[command] controller connected from {addr[0]}")
            try:
                handle(conn, rover)
            except OSError as exc:
                print(f"[command] connection error: {exc}")
            rover.stop()
            print("[command] controller disconnected; rover stopped")
    finally:
        rover.close()
        server.close()


if __name__ == "__main__":
    serve()
