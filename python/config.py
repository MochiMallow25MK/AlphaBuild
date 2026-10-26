# AlphaBuild - settings for the Python side.
# Change values here if something does not work on your computer.

# ----- Socket (Python is the server, Java connects to it) -----
SOCKET_HOST = "localhost"
SOCKET_PORT = 5000

# ----- TUIO (reacTIVision sends marker data to this port) -----
TUIO_PORT = 3333

# Number of identical readings in a row needed before a new word is sent.
# This stops the word from flickering when a marker is lost for one frame.
STABLE_FRAMES = 3

# Letters are read from the markers' x position, left to right.
# If your word appears backwards (TAC instead of CAT), change this to True.
FLIP_LETTER_ORDER = True

# ----- Gesture camera (the laptop webcam used by MediaPipe) -----
# Run check_cameras.py to find the right number.
CAMERA_INDEX = 0

# Which hand point is tracked. 9 = the middle of the palm (stable).
# 8 = the tip of the index finger.
TRACK_LANDMARK = 9

# ----- Gesture recognition -----
GESTURE_NAMES = ["submit", "next", "switch"]
GESTURE_HELP = {
    "submit": "Swipe your hand from left to right in a straight line",
    "next": "Draw a circle in the air with your hand",
    "switch": "Draw a big Z (a zigzag) in the air with your hand",
}
SAMPLES_PER_GESTURE = 5
TEMPLATES_FILE = "templates.json"

# A gesture is accepted only if its match score is at least this value (0 to 1).
# Lower it if good gestures are rejected. Raise it if wrong gestures are accepted.
MIN_SCORE = 0.35

# ----- Finding where a gesture starts and ends -----
# Hand speed is measured as the distance moved between two frames.
# The camera image is 1.0 wide, so 0.010 means 1 percent of the image width.
START_SPEED = 0.010     # moving faster than this starts a gesture
STOP_SPEED = 0.006      # moving slower than this counts as "hand is still"
STILL_FRAMES = 5        # this many still frames in a row end the gesture
LOST_FRAMES = 6         # this many frames without a hand also end the gesture
MIN_POINTS = 8          # gestures shorter than this are ignored
MIN_SIZE = 0.12         # gestures smaller than this (in image widths) are ignored
MAX_POINTS = 90         # a gesture is cut off after this many frames
COOLDOWN = 1.5          # seconds to ignore the hand after a gesture
