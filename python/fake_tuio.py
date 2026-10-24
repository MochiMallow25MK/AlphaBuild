# Pretends to be reacTIVision, so you can test without cameras or printed markers.
# Type letters (for example CAT) to put those letters "on the table".
# Press Enter on an empty line to remove them. Type q to quit.
#   python fake_tuio.py

import threading
import time

from pythonosc.osc_bundle_builder import OscBundleBuilder, IMMEDIATELY
from pythonosc.osc_message_builder import OscMessageBuilder
from pythonosc.udp_client import UDPClient

import config

word = ""
running = True


def make_message(*args):
    builder = OscMessageBuilder(address="/tuio/2Dobj")
    for arg in args:
        builder.add_arg(arg)
    return builder.build()


def send_loop():
    client = UDPClient("127.0.0.1", config.TUIO_PORT)
    frame = 0
    while running:
        letters = list(word)
        bundle = OscBundleBuilder(IMMEDIATELY)
        bundle.add_content(make_message("source", "fake@localhost"))
        bundle.add_content(make_message("alive", *range(len(letters))))
        for i, letter in enumerate(letters):
            marker_id = ord(letter) - ord("A")
            x = (i + 1) / (len(letters) + 1)       # spread letters from left to right
            bundle.add_content(make_message("set", i, marker_id, x, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
        frame += 1
        bundle.add_content(make_message("fseq", frame))
        client.send(bundle.build())
        time.sleep(1 / 30)                         # about 30 frames per second


thread = threading.Thread(target=send_loop, daemon=True)
thread.start()
print("Fake reacTIVision started. Type letters like CAT and press Enter. Type q to quit.")
while True:
    text = input("Letters on the table: ").strip().upper()
    if text == "Q":
        break
    word = "".join(c for c in text if "A" <= c <= "Z")
running = False
