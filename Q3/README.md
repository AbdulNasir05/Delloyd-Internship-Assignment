# ** Face Feature Detection using MediaPipe (Q3)**

This program uses MediaPipe Face Mesh to find the positions of the nose tip, left eye, and right eye from an image.
Unlike full face mesh visualization, this script highlights only key features with markers and labels.

# ** 🔎 How It Works **

Loads an input image using OpenCV.

Uses MediaPipe Face Mesh to detect facial landmarks.

Extracts only these points:

Nose tip (landmark 1)

Left eye center (average of landmarks 33 & 133)

Right eye center (average of landmarks 362 & 263)

Annotates the image with circles and text labels.

Displays the result in a pop-up window and saves the annotated image.

Prints a detection report with the coordinates of detected features.

# ** ⚙️ Configuration **

Update the image path inside the script as needed:

image_path = r"C:\...\Q3\goal_cristianoronaldo.jpg"


The output image will be saved as:

mediapipe_face_features_no_mesh.jpg

# ** ▶️ Usage ** 

Place your target image inside the Q3 folder.

Update the image_path variable in the script.

# ** Run the program: **

python mediapipe_face_features.py


# ** The program will: **

Detect the nose tip, left eye, and right eye.

Show the annotated image in a pop-up window.

Save the annotated image locally.

Print the detection report in the console.

# ** 📊 Example Output **

✅ MediaPipe Face Mesh initialized!  
💾 Results saved as: mediapipe_face_features_no_mesh.jpg  
👀 Press any key to close the window.  

📊 DETECTION REPORT:  
Total faces detected: 1  
Face 1:  
  Nose tip: (350, 220)  
  Left eye: (310, 200)  
  Right eye: (390, 200)  


Annotated Image:

🔴 Red dot → Nose tip

🔵 Blue dot → Left eye

🟡 Yellow dot → Right eye

# ** 📦 Requirements ** 

Python 3.7+

OpenCV → pip install opencv-python

MediaPipe → pip install mediapipe

NumPy → pip install numpy

# ** 👤 Author ** 

Abdul Nasir

Delloyd Internship 2025
