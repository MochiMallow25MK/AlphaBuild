# AlphaBuild: Interactive Alphabet Word Builder

**AlphaBuild** is an interactive educational game designed to help children develop letter recognition, spelling, and vocabulary skills through physical interaction. By combining computer vision, hand gesture recognition, and tangible objects, AlphaBuild transforms traditional alphabet learning into an engaging, hands-on experience.

Children use physical plastic alphabet letters placed in front of a camera to complete word-building challenges. Hand gestures allow them to submit answers and navigate the game, while printed reacTIVision fiducial markers provide additional tangible interactions and context-dependent content.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Gameplay](#gameplay)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Overview

AlphaBuild aims to make early literacy education more interactive by connecting physical alphabet letters with a camera-based game environment.

Instead of relying solely on a keyboard, touchscreen, or mouse, children interact with real objects and natural hand movements. The system combines computer vision and tangible user interfaces to create a playful learning environment.

### Project Goals

- Improve alphabet and letter recognition.
- Encourage children to build and spell words.
- Expand vocabulary through interactive challenges.
- Enable natural interaction using hand gestures.
- Integrate physical objects into a digital learning experience.
- Provide context-dependent content through fiducial marker tracking.

## Features

- **Physical Alphabet Interaction:** Use plastic alphabet letters, with one letter for each character from A to Z.
- **Word-Building Challenges:** Complete word challenges by arranging or presenting the required letters in front of a camera.
- **Hand Gesture Recognition:** Use gestures to submit answers and navigate between game screens.
- **Computer Vision:** Use MediaPipe to support real-time hand tracking and gesture-based interaction.
- **Gesture Recognition:** Use dollarpy to recognize supported gestures through a gesture-recognition algorithm.
- **Fiducial Marker Tracking:** Use printed reacTIVision markers to identify tangible objects and trigger context-dependent interactions.
- **TUIO Communication:** Transmit tangible interaction and tracking data between compatible components.
- **Cross-Language Integration:** Combine Python and Java components using socket-based communication where required.
- **Educational Gameplay:** Support an engaging, hands-on approach to learning spelling and vocabulary.

## How It Works

AlphaBuild combines camera input, gesture recognition, tangible object tracking, and game logic.

1. **Camera Input:** A camera captures the play area containing the physical alphabet letters and the child's hands.
2. **Letter Interaction:** The system processes the camera input to support interaction with the physical letters.
3. **Gesture Detection:** MediaPipe tracks hand landmarks, while dollarpy can recognize defined gestures.
4. **Marker Tracking:** reacTIVision detects printed fiducial markers and communicates tracking information through TUIO.
5. **Communication:** Python and Java components exchange relevant events and data through socket programming where needed.
6. **Word Validation:** The game compares the selected letters with the target word.
7. **Feedback:** The game provides appropriate feedback for correct answers, incorrect answers, and navigation actions.

*Note: The precise letter-detection method, communication protocol, and division of responsibilities between Python and Java depend on the implemented system architecture.*

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic and computer vision integration |
| MediaPipe | Hand landmark detection and tracking |
| dollarpy | Gesture recognition using the $1 recognizer approach |
| reacTIVision | Fiducial marker detection and tangible interaction |
| TUIO | Communication of tangible object tracking data |
| Java | Supporting application components and system integration |
| Socket Programming | Communication between application components |
| Camera | Capturing physical letters, markers, and hand movements |

## System Architecture

The application is organized around several cooperating components:

```text
                 Physical Interaction
              +------------------------+
              | Alphabet Letters (A-Z) |
              | Printed Fiducial       |
              | Markers                |
              +-----------+------------+
                          |
                          v
                   +-------------+
                   |   Camera    |
                   +------+------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
      +---------------+       +----------------+
      | Letter Input  |       | MediaPipe      |
      | Processing    |       | Hand Tracking  |
      +-------+-------+       +--------+-------+
              |                        |
              |                        v
              |               +----------------+
              |               | dollarpy       |
              |               | Gesture        |
              |               | Recognition    |
              |               +--------+-------+
              |                        |
              +------------+-----------+
                           |
                           v
                  +------------------+
                  |   Game Logic     |
                  | Word Challenges  |
                  | Answer Validation|
                  +--------+---------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
      +-------------+             +-------------+
      | reacTIVision|             | Python/Java |
      | and TUIO    |             | Socket      |
      | Tracking    |             | Communication|
      +------+------+             +------+------+
             |                           |
             +-------------+-------------+
                           |
                           v
                  +------------------+
                  | Game Feedback    |
                  | and Navigation   |
                  +------------------+
```

This diagram illustrates the conceptual architecture. Actual component connections may vary according to the final implementation.

## Getting Started

### Prerequisites

Before running AlphaBuild, prepare the following:

- Python installed on your computer.
- Java Development Kit (JDK), if Java components are included.
- A compatible camera or webcam.
- MediaPipe and dollarpy dependencies.
- reacTIVision installed and configured for marker tracking.
- Printed, compatible reacTIVision fiducial markers.
- Physical plastic alphabet letters from A to Z.
- A suitable environment for TUIO communication and socket-based integration.

### Installation

**1. Clone the repository**

```bash
git clone <repository-url>
cd AlphaBuild
```

Replace `<repository-url>` with the actual repository URL.

**2. Create a Python virtual environment**

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

**3. Install Python dependencies**

If a `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the Python dependencies according to the versions supported by the project:

```bash
pip install mediapipe dollarpy
```

Additional packages may be required for camera access, image processing, or TUIO communication, depending on the implementation.

**4. Configure Java**

Install a compatible JDK and configure the Java environment if your version of AlphaBuild includes Java-based components.

**5. Configure reacTIVision and TUIO**

- Install and launch reacTIVision.
- Configure the camera and tracking area.
- Print and prepare the compatible fiducial markers.
- Configure the TUIO destination and ensure the receiving component listens on the corresponding endpoint.

**6. Run the application**

The exact startup command depends on the repository structure. For example, if the main Python entry point is `main.py`, run:

```bash
python main.py
```

If Java components are required, compile and launch them using the project's build configuration or documented commands.

## Gameplay

A typical AlphaBuild session follows this sequence:

1. Start the application and position the camera so that it can see the interaction area.
2. Place the physical alphabet letters in front of the camera.
3. Begin a word-building challenge.
4. Identify and select the letters needed to form the target word.
5. Use the supported hand gesture to submit the answer.
6. Receive feedback based on the result.
7. Use the supported navigation gestures to continue to another challenge.
8. Interact with printed fiducial markers to access additional context-dependent content, where implemented.

The exact gestures, challenge rules, and marker-triggered actions should be documented as they are finalized.

## Project Structure

The following is a suggested directory structure. Adapt it to match the actual files in the repository.

```text
AlphaBuild/
├── README.md
├── requirements.txt
├── main.py
├── src/
│   ├── letter_detection.py
│   ├── hand_tracking.py
│   ├── gesture_recognition.py
│   ├── word_builder.py
│   ├── game_logic.py
│   └── communication.py
├── java/
│   └── src/
├── config/
│   └── settings.example
├── assets/
│   ├── images/
│   ├── words/
│   └── markers/
├── tests/
└── docs/
```

*These filenames and directories are illustrative and do not imply that all these files already exist.*

## Future Improvements

Potential enhancements include:

- **Difficulty Levels:** Introduce beginner, intermediate, and advanced word challenges.
- **Vocabulary Categories:** Organize words into themes such as animals, colors, food, and everyday objects.
- **Visual and Audio Feedback:** Add animations, spoken words, and encouraging sounds.
- **Progress Tracking:** Track completed challenges and learning milestones.
- **Adaptive Learning:** Adjust word difficulty according to the child's performance.
- **Expanded Gesture Controls:** Introduce additional gestures for pausing, restarting, and selecting categories.
- **Improved Recognition:** Enhance letter detection under different lighting conditions and camera angles.
- **Testing and Reliability:** Add automated tests for word validation, gesture recognition, and communication between components.
- **Accessibility:** Support multiple languages, adjustable difficulty, and alternative interaction methods.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Commit your work with a descriptive message.
5. Submit a pull request describing the changes.

Please ensure that new features preserve the project's focus on safe, accessible, and child-friendly learning.

## License

No license has been specified yet. Add an appropriate open-source license, such as the MIT License, if you intend to distribute the project under those terms. Until a license is included, reuse and redistribution permissions should not be assumed.

---

**AlphaBuild — Making alphabet learning tangible, interactive, and fun.**
