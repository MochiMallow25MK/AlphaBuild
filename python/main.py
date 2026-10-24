# AlphaBuild - Python side.
#   python main.py              runs everything (markers + gesture camera + socket)
#   python main.py --no-camera  runs markers + socket only (no gesture camera)
#
# Start this BEFORE the Java game.

import sys
import time

import config
from socket_server import SocketServer
from tuio_listener import TuioListener


def main():
    use_camera = "--no-camera" not in sys.argv

    server = SocketServer(config.SOCKET_HOST, config.SOCKET_PORT)
    server.start()

    tuio = TuioListener(server.send_letters)
    tuio.start()

    try:
        if use_camera:
            from gestures import run_gesture_loop     # loaded only when needed (it is slow)
            run_gesture_loop(server.send_gesture)
            print("Gesture camera is not running. Markers still work. Press Ctrl+C to stop.")
        else:
            print("Running without the gesture camera. Press Ctrl+C to stop.")
        while True:                  # keep the program alive so marker data keeps flowing
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    server.close()
    print("Stopped.")


main()
