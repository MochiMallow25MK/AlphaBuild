# Shows which camera number is which, so you can set CAMERA_INDEX in config.py.
# Press any key in the window to go to the next camera. Press q to quit.
#   python check_cameras.py

import cv2

for index in range(5):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("Camera", index, ": not available")
        cap.release()
        continue
    print("Camera", index, ": opened. Look at the window, press any key for the next camera.")
    key = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Camera", index, ": could not read a picture")
            break
        cv2.putText(frame, "Camera number " + str(index), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Camera check", frame)
        key = cv2.waitKey(30) & 0xFF
        if key != 255:
            break
    cap.release()
    if key == ord("q"):
        break
cv2.destroyAllWindows()
