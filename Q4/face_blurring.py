import cv2
import mediapipe as mp
import os
import datetime

# --- Setup directories ---
BASE_DIR = r"C:\Users\Abdul Muizz\Downloads\Delloyd-Internship-Assignment-main\Q4"
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# --- MediaPipe setup ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                  max_num_faces=5,
                                  refine_landmarks=True,
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

# --- Face blurring function ---
def blur_faces(frame, faces, blur_strength=15):
    blurred = frame.copy()
    for (x, y, w, h) in faces:
        y1, y2 = max(0, y), min(frame.shape[0], y + h)
        x1, x2 = max(0, x), min(frame.shape[1], x + w)
        if y2 > y1 and x2 > x1:
            k = max(11, min(151, blur_strength * 2 + 1))
            face_region = frame[y1:y2, x1:x2]
            blurred_face = cv2.GaussianBlur(face_region, (k, k), 0)
            blurred[y1:y2, x1:x2] = blurred_face
    return blurred

# --- Convert MediaPipe landmarks to bounding box ---
def get_face_boxes(frame):
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    boxes = []
    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            x_coords = [lm.x * w for lm in face.landmark]
            y_coords = [lm.y * h for lm in face.landmark]
            x1, y1 = int(min(x_coords)), int(min(y_coords))
            x2, y2 = int(max(x_coords)), int(max(y_coords))
            boxes.append([x1, y1, x2 - x1, y2 - y1])
    return boxes

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Cannot access webcam!")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    blur_strength = 15
    is_recording = False
    paused = False
    video_writer = None
    recording_start_time = None

    print("\n🎮 CONTROLS:")
    print("  s - Start/Stop Recording")
    print("  p - Pause/Resume Recording")
    print("  + / - - Increase/Decrease blur")
    print("  c - Screenshot")
    print("  q - Quit\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        faces = get_face_boxes(frame)
        blurred_frame = blur_faces(frame, faces, blur_strength)

        # --- Display info on screen ---
        cv2.putText(blurred_frame, f"Faces: {len(faces)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(blurred_frame, f"Status: {'Recording' if is_recording else 'Paused' if paused else 'Idle'}",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0) if is_recording else (0, 0, 255), 2)
        cv2.putText(blurred_frame, f"Blur Strength: {blur_strength}", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)

        cv2.imshow("MediaPipe Face Blurring", blurred_frame)

        # Write frame if recording and not paused
        if is_recording and not paused and video_writer:
            video_writer.write(blurred_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('s'):
            if not is_recording:
                filename = os.path.join(RECORDINGS_DIR, f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
                is_recording = True
                paused = False
                recording_start_time = datetime.datetime.now()
                print(f"▶️ Recording started: {filename}")
            else:
                is_recording = False
                paused = False
                if video_writer:
                    video_writer.release()
                    video_writer = None
                duration = (datetime.datetime.now() - recording_start_time).total_seconds()
                print(f"⏹️ Recording stopped. Duration: {duration:.2f}s")
        elif key == ord('p') and is_recording:
            paused = not paused
            print("⏸️ Paused" if paused else "▶️ Resumed")
        elif key in [ord('+'), ord('=')]:
            blur_strength = min(75, blur_strength + 5)
            print(f"🔺 Blur strength: {blur_strength}")
        elif key in [ord('-'), 45]:
            blur_strength = max(5, blur_strength - 5)
            print(f"🔻 Blur strength: {blur_strength}")
        elif key == ord('c'):
            filename = os.path.join(SCREENSHOTS_DIR, f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
            cv2.imwrite(filename, blurred_frame)
            print(f"📸 Screenshot saved: {filename}")

    cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()
    print("✅ Application closed successfully!")

if __name__ == "__main__":
    main()
