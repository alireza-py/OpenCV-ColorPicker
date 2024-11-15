# TheBall - Color-Based Object Detection for RoboCup Soccer

## Overview
TheBall is a Python project originally developed for **RoboCup Soccer** competitions. It detects and tracks soccer balls or other objects based on their color using OpenCV and the HSV color space. This project is optimized for real-time image processing in robotic soccer scenarios.

## Features
- Real-time detection and tracking of objects using color thresholds.
- Interactive color picker to dynamically adjust HSV values.
- Designed specifically for robotics and competitive environments.

## Quick Start
1. Install dependencies:
   ```bash
   pip install opencv-python numpy
Run the script:
bash
Copy code
python main.py
Use these keys for interaction:
q: Quit the program.
c: Pick a color from the video.
h: Open HSV adjustment trackbars.
Requirements
Python 3.7+
Libraries: OpenCV, NumPy
Applications
This code was developed for use in RoboCup Soccer competitions, where robots need to:

Detect and follow the ball.
React dynamically to changes in lighting and environment.
License
This is a personal project initially created for RoboCup. Feel free to use or modify it for educational and non-commercial purposes.

yaml
Copy code
