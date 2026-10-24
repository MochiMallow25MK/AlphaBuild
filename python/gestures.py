# Hand gestures: MediaPipe finds the hand, dollarpy recognizes the movement.
# Based on the lab files Realtime-pose.ipynb (live camera loop with MediaPipe)
# and dollarpy.ipynb (Template, Recognizer, Point).

import json
import math
import os
import time

import cv2
import mediapipe as mp
from dollarpy import Recognizer, Template, Point

import config

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# The templates file is stored next to this script.
TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), config.TEMPLATES_FILE)


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def size_of(points):
    """Width or height of the area covered by the movement (the bigger one)."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return max(max(xs) - min(xs), max(ys) - min(ys))


class Segmenter:
    """Cuts the stream of hand positions into separate gestures.
    A gesture starts when the hand moves fast and ends when the hand is still
    (or disappears) for a short time."""

    def __init__(self):
        self.recording = False
        self.points = []
        self.previous = None
        self.still_count = 0
        self.lost_count = 0
        self.ignore_until = 0.0

    def in_cooldown(self, now=None):
        if now is None:
            now = time.time()
        return now < self.ignore_until

    def update(self, point, now=None):
        """point is (x, y) or None when no hand is visible.
        Returns a list of points when a gesture has just finished, otherwise None."""
        if now is None:
            now = time.time()

        if self.in_cooldown(now):
            self.previous = point
            return None

        if point is None:
            self.previous = None
            if self.recording:
                self.lost_count += 1
                if self.lost_count >= config.LOST_FRAMES:
                    return self.finish(now)
            return None

        self.lost_count = 0
        previous = self.previous
        self.previous = point
        speed = 0.0
        if previous is not None:
            speed = distance(previous, point)

        if not self.recording:
            if previous is not None and speed > config.START_SPEED:
                self.recording = True
                self.points = [previous, point]
                self.still_count = 0
            return None

        self.points.append(point)
        if speed < config.STOP_SPEED:
            self.still_count += 1
        else:
            self.still_count = 0
        if self.still_count >= config.STILL_FRAMES or len(self.points) >= config.MAX_POINTS:
            return self.finish(now)
        return None

    def finish(self, now):
        points = self.points
        if 0 < self.still_count < len(points):
            points = points[:-self.still_count]      # remove the still part at the end
        self.recording = False
        self.points = []
        self.still_count = 0
        self.lost_count = 0
        if len(points) < config.MIN_POINTS or size_of(points) < config.MIN_SIZE:
            return None                              # too small, probably not a gesture
        self.ignore_until = now + config.COOLDOWN
        return points


def load_templates():
    """Returns a dictionary: gesture name -> list of recorded samples."""
    if not os.path.exists(TEMPLATES_PATH):
        return {}
    with open(TEMPLATES_PATH) as f:
        return json.load(f)


def save_templates(templates):
    with open(TEMPLATES_PATH, "w") as f:
        json.dump(templates, f)


def classify(points, templates):
    """Compares the movement with all recorded templates using dollarpy.
    Returns (gesture name, score) or (None, score) if nothing matches well."""
    # New Template objects are built every time because dollarpy changes the
    # lists it is given while it works.
    template_list = []
    for name, samples in templates.items():
        for sample in samples:
            template_list.append(Template(name, [Point(x, y, 1) for x, y in sample]))
    movement = [Point(x, y, 1) for x, y in points]
    try:
        name, score = Recognizer(template_list).recognize(movement)
    except Exception:
        return None, 0.0
    if name is None or score < config.MIN_SCORE:
        return None, score
    return name, score


def open_camera():
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Cannot open camera number " + str(config.CAMERA_INDEX)
                           + ". Run check_cameras.py and fix CAMERA_INDEX in config.py")
    return cap


def create_hands():
    return mp_hands.Hands(static_image_mode=False,     # video mode (faster than image mode)
                          max_num_hands=1,
                          model_complexity=0,         # lightest model
                          min_detection_confidence=0.6,
                          min_tracking_confidence=0.5)


def find_hand_point(frame, hands):
    """Finds the hand in a frame. Returns (x, y) between 0 and 1, or None.
    Also draws the hand on the frame."""
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
        landmark = hand.landmark[config.TRACK_LANDMARK]
        return (landmark.x, landmark.y)
    return None


def draw_text(frame, text, y, color=(255, 255, 255)):
    cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
    cv2.putText(frame, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


def draw_trail(frame, points):
    height, width = frame.shape[:2]
    for i in range(1, len(points)):
        a = (int(points[i - 1][0] * width), int(points[i - 1][1] * height))
        b = (int(points[i][0] * width), int(points[i][1] * height))
        cv2.line(frame, a, b, (0, 255, 255), 3)


def run_gesture_loop(on_gesture):
    """Main camera loop. Calls on_gesture(name) every time a gesture is recognized.
    Returns False if it could not start."""
    templates = load_templates()
    if not templates:
        print("No gesture templates found. Run record_gestures.py first.")
        return False
    try:
        cap = open_camera()
    except RuntimeError as error:
        print(error)
        return False

    hands = create_hands()
    segmenter = Segmenter()
    message = "Make a gesture"
    message_until = 0.0
    print("Gesture camera started. Press q in the camera window to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Could not read from the camera.")
            break
        frame = cv2.flip(frame, 1)               # mirror image, like a mirror
        point = find_hand_point(frame, hands)
        finished = segmenter.update(point)

        if finished is not None:
            name, score = classify(finished, templates)
            if name is not None:
                on_gesture(name)
                message = "Recognized: " + name + " (" + str(round(score, 2)) + ")"
            else:
                message = "Gesture not recognized, try again"
            message_until = time.time() + 2.0

        if segmenter.recording:
            draw_trail(frame, segmenter.points)
            draw_text(frame, "Recording movement...", 30, (0, 255, 255))
        elif time.time() < message_until:
            draw_text(frame, message, 30, (0, 255, 0))
        elif segmenter.in_cooldown():
            draw_text(frame, "Wait...", 30)
        else:
            draw_text(frame, "Make a gesture, then hold still", 30)
        draw_text(frame, "Press q to quit", frame.shape[0] - 15)

        cv2.imshow("AlphaBuild - gesture camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    return True
