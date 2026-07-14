"""Run the rover Pi: drive-command server + live-video server together."""

import threading

import command_server
import video_server


def main():
    threads = [
        threading.Thread(target=command_server.serve, name="command", daemon=True),
        threading.Thread(target=video_server.serve, name="video", daemon=True),
    ]
    for t in threads:
        t.start()
    print("[rover] command + video servers running. Ctrl-C to stop.")
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("\n[rover] shutting down")


if __name__ == "__main__":
    main()
