# Eye State Detection Application

## Overview
A simple desktop application that uses your webcam to detect whether your eyes are open or closed in real-time. Each eye is labeled individually showing its current state.

## What is Used

### Technologies
- **Python 3.x** - Programming language
- **OpenCV (cv2)** - Computer vision library for face and eye detection
- **Tkinter** - Built-in Python GUI framework for the application interface
- **PIL (Pillow)** - Image processing for displaying video frames in the GUI
- **Threading** - For smooth video processing without freezing the UI

### Detection Method
- **Haar Cascade Classifiers** - Pre-trained machine learning models for detecting:
  - Frontal faces (`haarcascade_frontalface_default.xml`)
  - Eyes (`haarcascade_eye.xml`)

## How It Works

### Detection Logic
1. **Face Detection**: The app first detects your face in the video frame using the face cascade classifier
2. **Eye Region**: It focuses on the upper half of the detected face where eyes are typically located
3. **Eye Detection**: Uses the eye cascade classifier to detect open eyes
4. **State Determination**:
   - **Eyes OPEN**: When the eye cascade detects eye patterns (2 rectangles = both eyes open)
   - **Eyes CLOSED**: When no eye patterns are detected (closed eyes don't match the open eye pattern)
5. **Labeling**: Each detected eye gets labeled as "OPEN" with a green rectangle and text

### Visual Feedback
- **Blue rectangle**: Around detected face
- **Green rectangles**: Around open eyes
- **Green text**: "Left Eye: OPEN" or "Right Eye: OPEN" labels
- **Status text**: Overall status above face ("Both Eyes: OPEN", "One Eye: OPEN", or "Both Eyes: CLOSED")

## Setup and Installation

### Step 1: Install Python
Make sure you have Python 3.7 or higher installed on your system.
- Download from: https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

### Step 2: Install Required Libraries
Open PowerShell or Command Prompt in the project folder and run:
```powershell
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install opencv-python Pillow
```

### Step 3: Verify Installation
Check if OpenCV is installed correctly:
```powershell
python -c "import cv2; print(cv2.__version__)"
```

## How to Run

### Method 1: Using Python Command
Navigate to the project folder and run:
```powershell
python eye_detection_app.py
```

### Method 2: Double-click (Windows)
If Python is properly associated with `.py` files, you can simply double-click `eye_detection_app.py`

## Usage Instructions

1. **Launch the Application**: Run the Python script as described above
2. **Click "Open Camera"**: Press the button to start your webcam
3. **Position Yourself**: Sit in front of the camera with good lighting
4. **Watch the Detection**: The app will:
   - Draw a blue box around your face
   - Draw green boxes around your open eyes
   - Label each eye as "OPEN" when detected
   - Show "CLOSED" when eyes are not detected (closed)
5. **Test It**: Try closing one or both eyes to see the labels change
6. **Close Camera**: Click the "Close Camera" button when done
7. **Exit**: Close the window to exit the application

## Tips for Best Results

- **Good Lighting**: Ensure your face is well-lit (face the light source)
- **Face the Camera**: Look directly at the camera for best detection
- **Remove Obstructions**: Avoid wearing sunglasses or having hair covering your eyes
- **Stable Position**: Keep your face within the camera frame
- **Distance**: Sit about 1-2 feet away from the camera

## Troubleshooting

### Camera doesn't open
- Check if another application is using the camera
- Ensure you have camera permissions enabled for Python
- Try restarting the application

### Eyes not detected properly
- Improve lighting conditions
- Remove glasses if wearing them
- Adjust your distance from the camera
- Ensure your face is clearly visible

### Application freezes
- Close and restart the application
- Check if your system meets the requirements
- Ensure no other heavy applications are running

## Technical Notes

- The application uses Haar Cascade classifiers which are fast but may have occasional false positives/negatives
- Eye detection works best with open eyes; closed eyes are inferred when no eye patterns are detected
- The video feed is mirrored (flipped horizontally) for a natural mirror-like experience
- Frame processing runs in a separate thread to keep the UI responsive

## System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.7 or higher
- **Webcam**: Built-in or external USB camera
- **RAM**: Minimum 2GB (4GB recommended)
- **Processor**: Any modern CPU with dual-core or better

## License
This is a simple educational project. Feel free to use and modify as needed.
