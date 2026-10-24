# Records the gesture templates that dollarpy uses to recognize gestures.
# Run this once (and again whenever you change the camera position).
#   python record_gestures.py

import cv2
import config
import gestures


def main():
    cap = gestures.open_camera()
    hands = gestures.create_hands()
    segmenter = gestures.Segmenter()
    templates = {}
    finished_all = True

    for name in config.GESTURE_NAMES:
        samples = []
        flash_message = ""
        flash_count = 0
        while len(samples) < config.SAMPLES_PER_GESTURE:
            ok, frame = cap.read()
            if not ok:
                finished_all = False
                break
            frame = cv2.flip(frame, 1)
            point = gestures.find_hand_point(frame, hands)
            points = segmenter.update(point)
            if points is not None:
                samples.append([[x, y] for x, y in points])
                flash_message = "Saved sample " + str(len(samples))
                flash_count = 40
                print(name, "- saved sample", len(samples), "of", config.SAMPLES_PER_GESTURE)

            gestures.draw_text(frame, "Gesture: " + name.upper() + "  (sample "
                               + str(len(samples) + 1) + " of " + str(config.SAMPLES_PER_GESTURE) + ")", 30, (0, 255, 255))
            gestures.draw_text(frame, config.GESTURE_HELP[name], 60)
            if segmenter.recording:
                gestures.draw_trail(frame, segmenter.points)
                gestures.draw_text(frame, "Recording movement...", 90, (0, 255, 255))
            elif segmenter.in_cooldown():
                gestures.draw_text(frame, "Wait a moment...", 90)
            elif flash_count > 0:
                gestures.draw_text(frame, flash_message, 90, (0, 255, 0))
            else:
                gestures.draw_text(frame, "Make the gesture, then hold your hand still", 90)
            if flash_count > 0:
                flash_count -= 1
            gestures.draw_text(frame, "Press q to quit", frame.shape[0] - 15)

            cv2.imshow("AlphaBuild - record gestures", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                finished_all = False
                break
        if not finished_all:
            break
        templates[name] = samples

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

    if finished_all:
        gestures.save_templates(templates)
        print("Done. Templates saved to", gestures.TEMPLATES_PATH)
    else:
        print("Recording was stopped. Nothing was saved.")


main()
