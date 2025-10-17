#!/usr/bin/python
"""
MediaPipe Face Detection with Nose Tip and Eyes (No Mesh Lines) — Webcam Version
Includes: Auto-create 'recordings/' and 'screenshots/' folders, recording, screenshot, quit
Displays number of faces detected live on the webcam window.
"""

import cv2
import mediapipe as mp
import os
import time

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

BASE_DIR = r"C:\Users\Abdul Muizz\Downloads\Delloyd-Internship-Assignment-main\Q3"

# Folders for saving outputs inside BASE_DIR
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


class MediaPipeFaceDetector:
    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                               max_num_faces=5,
                                               refine_landmarks=True,
                                               min_detection_confidence=0.5,
                                               min_tracking_confidence=0.5)
        print("✅ MediaPipe Face Mesh initialized!")

    def detect_face_features(self, frame):
        """
        Detect face landmarks (nose + eyes) and draw them.
        Returns annotated frame and number of faces detected.
        """
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        annotated = frame.copy()
        face_count = 0

        if results.multi_face_landmarks:
            face_count = len(results.multi_face_landmarks)
            for face_landmarks in results.multi_face_landmarks:
                # Nose tip (landmark 1)
                nose_tip_lm = face_landmarks.landmark[1]
                nose_tip = (int(nose_tip_lm.x * w), int(nose_tip_lm.y * h))
                cv2.circle(annotated, nose_tip, 3, (0, 0, 255), -1)
                cv2.putText(annotated, "Nose", (nose_tip[0]-20, nose_tip[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

                # Left eye center (average of 33 and 133)
                left_eye_x = int((face_landmarks.landmark[33].x + face_landmarks.landmark[133].x)/2 * w)
                left_eye_y = int((face_landmarks.landmark[33].y + face_landmarks.landmark[133].y)/2 * h)
                left_eye = (left_eye_x, left_eye_y)
                cv2.circle(annotated, left_eye, 3, (255, 0, 0), -1)
                cv2.putText(annotated, "Left Eye", (left_eye[0]-20, left_eye[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

                # Right eye center (average of 362 and 263)
                right_eye_x = int((face_landmarks.landmark[362].x + face_landmarks.landmark[263].x)/2 * w)
                right_eye_y = int((face_landmarks.landmark[362].y + face_landmarks.landmark[263].y)/2 * h)
                right_eye = (right_eye_x, right_eye_y)
                cv2.circle(annotated, right_eye, 3, (0, 255, 255), -1)
                cv2.putText(annotated, "Right Eye", (right_eye[0]-20, right_eye[1]-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

        return annotated, face_count


def main():
    detector = MediaPipeFaceDetector()
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Cannot access webcam!")
        return

    recording = False
    paused = False
    out = None
    video_filename = None

    print("\n🎮 CONTROLS:")
    print("  s - Start Recording")
    print("  p - Pause/Resume Recording")
    print("  x - Stop Recording & Save")
    print("  c - Take Screenshot")
    print("  q - Quit\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        annotated_frame, face_count = detector.detect_face_features(frame)

        # Overlay status and number of faces
        status_text = "Recording" if recording else "Paused" if paused else "Idle"
        cv2.putText(annotated_frame, f"Status: {status_text}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if recording else (0, 0, 255), 2)
        cv2.putText(annotated_frame, f"Faces: {face_count}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        cv2.imshow("Webcam Face Detection", annotated_frame)

        key = cv2.waitKey(1) & 0xFF

        # --- Key Bindings ---
        if key == ord('s'):
            if not recording:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_filename = os.path.join(RECORDINGS_DIR, f"recording_{time.strftime('%Y%m%d_%H%M%S')}.mp4")
                out = cv2.VideoWriter(video_filename, fourcc, 20.0,
                                      (annotated_frame.shape[1], annotated_frame.shape[0]))
                recording = True
                paused = False
                print(f"▶️ Recording started: {video_filename}")

        elif key == ord('p'):
            if recording:
                paused = not paused
                print("⏸️ Paused" if paused else "▶️ Resumed")

        elif key == ord('x'):
            if recording:
                recording = False
                paused = False
                if out:
                    out.release()
                print(f"💾 Recording saved as: {video_filename}")
                video_filename = None

        elif key == ord('c'):
            screenshot_name = os.path.join(SCREENSHOTS_DIR, f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(screenshot_name, annotated_frame)
            print(f"📸 Screenshot saved as: {screenshot_name}, Faces detected: {face_count}")

        elif key == ord('q'):
            print("👋 Quitting...")
            break

        # Save frame if recording and not paused
        if recording and not paused and out is not None:
            out.write(annotated_frame)

    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
