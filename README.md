# AlphaBuild - Interactive Alphabet Word Builder

HCI midterm project (DPRG508). Children build words with plastic letters and fiducial
markers (reacTIVision + TUIO) and control the game with hand gestures
(MediaPipe + dollarpy). Python and Java talk to each other through a socket.

Full step-by-step instructions: AlphaBuild_Guide.docx

## Folders
- python/  marker listener, gesture recognition, socket server
- java/    the game window (Java Swing) and the pictures

## Quick start (after the one-time setup in the guide)
1. Start reacTIVision.
2. Terminal 1:  cd python   then   python main.py
3. Terminal 2:  cd java     then   java -cp out Main

No cameras? Use  python fake_tuio.py  instead of reacTIVision and
python main.py --no-camera  (see the guide, Step A).
