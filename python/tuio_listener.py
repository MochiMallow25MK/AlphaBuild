# Listens to reacTIVision (TUIO messages over UDP) and works out which
# letters are on the table and in which order.
#
# reacTIVision sends these TUIO messages for every camera frame:
#   alive  -> the session ids of all markers that are visible now
#   set    -> session id, marker id, x, y, angle, ... for one marker
#   fseq   -> end of the frame

import threading
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import config


def marker_to_letter(marker_id):
    # Marker 0 = A, marker 1 = B, ... marker 25 = Z. Other markers are ignored.
    if 0 <= marker_id <= 25:
        return chr(ord("A") + marker_id)
    return None


class TuioListener:
    def __init__(self, on_letters):
        self.on_letters = on_letters     # function that receives the new word
        self.objects = {}                # session id -> (marker id, x position)
        self.last_word = ""              # last word that was sent
        self.candidate = ""              # word seen in the latest frames
        self.candidate_count = 0

    def handle(self, address, *args):
        if len(args) == 0:
            return
        command = args[0]
        if command == "alive":
            alive_ids = set(args[1:])
            for session_id in list(self.objects.keys()):
                if session_id not in alive_ids:
                    del self.objects[session_id]
        elif command == "set":
            session_id = args[1]
            marker_id = args[2]
            x = args[3]
            self.objects[session_id] = (marker_id, x)
        elif command == "fseq":
            self.end_of_frame()

    def end_of_frame(self):
        found = []
        for marker_id, x in self.objects.values():
            letter = marker_to_letter(marker_id)
            if letter is not None:
                found.append((x, letter))
        found.sort()                     # left to right
        if config.FLIP_LETTER_ORDER:
            found.reverse()
        word = "".join(letter for x, letter in found)

        # Only accept a word after it was the same for a few frames in a row.
        if word == self.candidate:
            self.candidate_count += 1
        else:
            self.candidate = word
            self.candidate_count = 1
        if self.candidate_count >= config.STABLE_FRAMES and word != self.last_word:
            self.last_word = word
            self.on_letters(word)

    def start(self):
        dispatcher = Dispatcher()
        dispatcher.map("/tuio/2Dobj", self.handle)
        server = BlockingOSCUDPServer(("127.0.0.1", config.TUIO_PORT), dispatcher)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print("Listening for reacTIVision (TUIO) on port", config.TUIO_PORT)
