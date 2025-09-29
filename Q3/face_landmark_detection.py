#!/usr/bin/python
"""
MediaPipe Face Detection with Nose Tip and Eyes (No Mesh Lines)
"""

import cv2
import mediapipe as mp
import os
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

class MediaPipeFaceDetector:
    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True,
                                               max_num_faces=5,
                                               refine_landmarks=True,
                                               min_detection_confidence=0.5)
        print("✅ MediaPipe Face Mesh initialized!")

    def detect_face_features(self, image_path):
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Could not load image: {image_path}")
            return None

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_img)

        if not results.multi_face_landmarks:
            print("❌ No faces detected.")
            return None

        annotated_img = img.copy()
        detection_results = []

        h, w, _ = img.shape

        for i, face_landmarks in enumerate(results.multi_face_landmarks):
            # Nose tip (landmark 1)
            nose_tip_lm = face_landmarks.landmark[1]
            nose_tip = (int(nose_tip_lm.x * w), int(nose_tip_lm.y * h))
            cv2.circle(annotated_img, nose_tip, 3, (0,0,255), -1)
            cv2.putText(annotated_img, "Nose", (nose_tip[0]-20, nose_tip[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)

            # Left eye center (average of 33 and 133)
            left_eye_x = int((face_landmarks.landmark[33].x + face_landmarks.landmark[133].x)/2 * w)
            left_eye_y = int((face_landmarks.landmark[33].y + face_landmarks.landmark[133].y)/2 * h)
            left_eye = (left_eye_x, left_eye_y)
            cv2.circle(annotated_img, left_eye, 3, (255,0,0), -1)
            cv2.putText(annotated_img, "Left Eye", (left_eye[0]-20, left_eye[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1)

            # Right eye center (average of 362 and 263)
            right_eye_x = int((face_landmarks.landmark[362].x + face_landmarks.landmark[263].x)/2 * w)
            right_eye_y = int((face_landmarks.landmark[362].y + face_landmarks.landmark[263].y)/2 * h)
            right_eye = (right_eye_x, right_eye_y)
            cv2.circle(annotated_img, right_eye, 3, (0,255,255), -1)
            cv2.putText(annotated_img, "Right Eye", (right_eye[0]-20, right_eye[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,255), 1)

            detection_results.append({
                "face_id": i+1,
                "nose_tip": nose_tip,
                "left_eye": left_eye,
                "right_eye": right_eye
            })

        return {
            "original": img,
            "annotated": annotated_img,
            "faces": detection_results,
            "total_faces": len(detection_results)
        }

def main():
    image_path = r"C:\Users\Home\Desktop\Nasir\Delloyd Internship\Q3\goal_cristianoronaldo-cropped_1td5dt3z4fahj1wbhl9647ciyw.jpg"
    if not os.path.exists(image_path):
        print("❌ Image file not found!")
        return

    detector = MediaPipeFaceDetector()
    result = detector.detect_face_features(image_path)

    if result:
        output_path = "mediapipe_face_features_no_mesh.jpg"
        cv2.imwrite(output_path, result['annotated'])
        print(f"💾 Results saved as: {output_path}")

        cv2.imshow("Face Features Detection", result['annotated'])
        print("👀 Press any key to close the window.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(f"\n📊 DETECTION REPORT:")
        print(f"Total faces detected: {result['total_faces']}")
        for face in result['faces']:
            print(f"Face {face['face_id']}:")
            print(f"  Nose tip: {face['nose_tip']}")
            print(f"  Left eye: {face['left_eye']}")
            print(f"  Right eye: {face['right_eye']}")

if __name__ == "__main__":
    main()
