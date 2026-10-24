# Socket server: sends letters and gestures from Python to the Java game.
# Same idea as python-server.ipynb from the lab, but it sends plain text
# (one message per line) because Java cannot read Python pickle data.

import socket
import threading


class SocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket()
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.conn = None                 # the connection to the Java game
        self.lock = threading.Lock()     # two threads send, so we use a lock
        self.last_letters = ""           # remembered for a Java game that connects late

    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        thread = threading.Thread(target=self.accept_loop, daemon=True)
        thread.start()
        print("Socket server waiting for the Java game on port", self.port)

    def accept_loop(self):
        while True:
            try:
                conn, addr = self.server.accept()
            except OSError:
                return                   # server was closed
            print("Java game connected")
            with self.lock:
                self.conn = conn
            # Tell the new game which letters are on the table right now.
            self.send_text("LETTERS " + self.last_letters)

    def send_text(self, text):
        with self.lock:
            if self.conn is None:
                return
            try:
                self.conn.sendall((text + "\n").encode("utf-8"))
            except OSError:
                print("Java game disconnected")
                self.conn = None

    def send_letters(self, letters):
        self.last_letters = letters
        print("Letters on the table:", letters if letters else "(none)")
        self.send_text("LETTERS " + letters)

    def send_gesture(self, name):
        print("Gesture:", name)
        self.send_text("GESTURE " + name)

    def close(self):
        with self.lock:
            if self.conn is not None:
                self.conn.close()
        self.server.close()
