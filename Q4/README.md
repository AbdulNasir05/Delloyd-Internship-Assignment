# 🎥 Advanced Face Blurring – Multiple Detection Models

# 📌 Overview

This Python program provides real-time face detection and blurring using multiple face detection models.
It is designed for privacy protection in video streams (like webcams or CCTV) by automatically detecting and blurring faces.

The system supports:

Haar Cascade (fast, lightweight)

DNN (Deep Neural Network) (accurate, requires model download)

YuNet (modern, highly accurate)

Users can dynamically switch detectors, adjust blur strength, change confidence thresholds, and even record or capture screenshots during execution.

# ⚙️ Features

✅ Real-time face detection and blurring

✅ Supports Haar Cascade, DNN, and YuNet models

✅ Adjustable blur strength (5–75)

✅ Adjustable detection confidence (0.3–0.95)

✅ Recording mode (start/stop with keypress)

✅ Screenshot capture with timestamp

✅ Debug mode to show bounding boxes

✅ Automatic DNN model download if missing

# 📂 File Structure

FaceBlurringSystem
 
 ├── face_blurring.py        # Main Python script
 
 ├── recordings/             # Folder for saved videos & screenshots
 
 ├── README.md               # Documentation


# ▶️ Usage

Run the program:

python face_blurring.py


Controls (while running):

s - Start/stop recording  

+ - Increase blur strength  

- - Decrease blur strength  

m - Switch detection model (Haar / DNN / YuNet)  

c - Increase detection confidence  

v - Decrease detection confidence  

d - Toggle debug mode (show face boxes)  

x - Capture screenshot  

q - Quit application  


# 📊 Example Output

🔹 Startup Console Output

Video properties: 640x480 at 30 FPS

✅ DNN model files downloaded successfully!

🎯 Advanced Face Blurring with Multiple Detection Models
============================================================
Controls:

s - Start/stop recording

+ - Increase blur strength

- - Decrease blur strength

m - Switch detection model

c - Increase detection confidence

v - Decrease detection confidence

d - Toggle debug mode

x - Capture screenshot

q - Quit application
============================================================
🔍 Current detector: Haar Cascade (Fast)

🎯 Detection confidence: 0.70


🔹 On-Screen Overlay Example

Faces: 2

Detector: Haar

Blur: 15

Confidence: 0.70


🔹 Recording Example

🎥 Started recording: recordings/face_blurred_20250929_193020.avi

⏹️ Stopped recording. Duration: 12.45 seconds


🔹 Screenshot Example

📸 Screenshot saved: recordings/screenshot_20250929_193150.jpg


🧪 Edge Cases

Missing DNN model files → Automatically downloaded from OpenCV repo

Detector errors → Falls back to next available method (YuNet → DNN → Haar)

Empty frame read → Handled safely

Face partially outside frame → Bounding box corrected before blurring

# ⚡ Performance

Haar Cascade → Fast (~200 FPS) but less accurate

DNN → Slower (~30 FPS) but robust to lighting/angles

YuNet → Balanced speed & accuracy (~60 FPS)

# 📦 Requirements

Python 3.7+

OpenCV (opencv-python, opencv-contrib-python)

NumPy

Install dependencies:

pip install opencv-python opencv-contrib-python numpy


# 👨‍💻 Author

Abdul Nasir

Delloyd Internship 2025

Delul Nasir
Delloyd Internship 2025
