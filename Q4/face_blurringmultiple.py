import cv2
import numpy as np
import datetime
import os

def detect_faces(frame):
    """Detect faces using Haar Cascade"""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Face detection parameters
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    return faces

def blur_faces(frame, faces, blur_strength=30):
    """Blur detected faces with adjustable strength - FIXED VERSION"""
    blurred_frame = frame.copy()
    
    for (x, y, w, h) in faces:
        # Ensure we don't go out of frame bounds
        y1, y2 = max(0, y), min(frame.shape[0], y + h)
        x1, x2 = max(0, x), min(frame.shape[1], x + w)
        
        if y2 > y1 and x2 > x1:
            # Extract the face region
            face_region = frame[y1:y2, x1:x2]
            
            # FIXED: Kernel size changes with blur strength (must be odd numbers)
            kernel_size = blur_strength * 2 + 1  # Convert strength to odd number
            
            # Ensure kernel size is reasonable (not too small or too large)
            kernel_size = max(11, min(151, kernel_size))  # Between 11x11 and 151x151
            
            # Apply Gaussian blur with dynamic kernel size
            blurred_face = cv2.GaussianBlur(face_region, (kernel_size, kernel_size), 0)
            
            # Replace the face region with the blurred version
            blurred_frame[y1:y2, x1:x2] = blurred_face
    
    return blurred_frame

def main():
    # Initialize video capture (0 for default webcam)
    cap = cv2.VideoCapture(0)
    
    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps == 0:
        fps = 30
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video properties: {width}x{height} at {fps} FPS")
    
    # Variables for recording
    is_recording = False
    video_writer = None
    recording_start_time = None
    blur_strength = 15  # Start with medium strength (kernel size = 31x31)
    
    # Create recordings directory if it doesn't exist
    if not os.path.exists('recordings'):
        os.makedirs('recordings')
    
    print("Face Blurring Application Started")
    print("=" * 50)
    print("Controls:")
    print("s - Start/stop recording")
    print("+ - Increase blur strength (makes faces more blurry)")
    print("- - Decrease blur strength (makes faces clearer)")
    print("c - Capture screenshot")
    print("d - Toggle debug mode (show face boxes)")
    print("q - Quit application")
    print("=" * 50)
    print(f"Current blur strength: {blur_strength} (Kernel size: {blur_strength * 2 + 1}x{blur_strength * 2 + 1})")
    
    recording_blink_counter = 0
    show_debug = False
    
    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Could not read frame")
                break
            
            # Mirror the frame for more natural interaction
            frame = cv2.flip(frame, 1)
            
            # Detect faces
            faces = detect_faces(frame)
            
            # Blur faces with current strength
            processed_frame = blur_faces(frame, faces, blur_strength)
            
            # Add face count information
            face_count_text = f"Faces: {len(faces)}"
            cv2.putText(processed_frame, face_count_text, (10, height - 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Add blur strength information with kernel size
            kernel_size = blur_strength * 2 + 1
            blur_text = f"Blur: {blur_strength} (Kernel: {kernel_size}x{kernel_size})"
            cv2.putText(processed_frame, blur_text, (10, height - 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            # Show face rectangles in debug mode
            if show_debug:
                for (x, y, w, h) in faces:
                    cv2.rectangle(processed_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(processed_frame, "Face", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # Add recording indicator with blinking effect
            if is_recording:
                recording_blink_counter += 1
                if recording_blink_counter % 30 < 15:
                    cv2.putText(processed_frame, "RECORDING", (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.circle(processed_frame, (width - 30, 30), 8, (0, 0, 255), -1)
            
            # Add debug mode indicator
            if show_debug:
                cv2.putText(processed_frame, "DEBUG MODE", (width - 150, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            # Display the processed frame
            cv2.imshow('Face Blurring - Press + to increase blur, - to decrease', processed_frame)
            
            # Write frame to video if recording
            if is_recording and video_writer is not None:
                video_writer.write(processed_frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                if not is_recording:
                    # Start recording
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"recordings/face_blurred_{timestamp}.avi"
                    
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
                    
                    is_recording = True
                    recording_start_time = datetime.datetime.now()
                    print(f"🎥 Started recording: {filename}")
                    
                else:
                    # Stop recording
                    if video_writer is not None:
                        video_writer.release()
                        video_writer = None
                    
                    recording_duration = (datetime.datetime.now() - recording_start_time).total_seconds()
                    print(f"⏹️ Stopped recording. Duration: {recording_duration:.2f} seconds")
                    is_recording = False
            
            elif key == ord('c'):
                # Capture screenshot
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_filename = f"recordings/screenshot_{timestamp}.jpg"
                cv2.imwrite(screenshot_filename, processed_frame)
                print(f"📸 Screenshot saved: {screenshot_filename}")
            
            elif key == ord('+'):
                # Increase blur strength - PROPERLY FIXED
                old_strength = blur_strength
                blur_strength = min(75, blur_strength + 5)  # Max kernel size ~151x151
                kernel_size = blur_strength * 2 + 1
                if old_strength != blur_strength:
                    print(f"🔺 Blur strength increased to: {blur_strength} (Kernel: {kernel_size}x{kernel_size})")
            
            elif key == ord('-'):
                # Decrease blur strength
                old_strength = blur_strength
                blur_strength = max(5, blur_strength - 5)  # Min kernel size ~11x11
                kernel_size = blur_strength * 2 + 1
                if old_strength != blur_strength:
                    print(f"🔻 Blur strength decreased to: {blur_strength} (Kernel: {kernel_size}x{kernel_size})")
            
            elif key == ord('d'):
                # Toggle debug mode
                show_debug = not show_debug
                status = "ON" if show_debug else "OFF"
                print(f"🐛 Debug mode: {status}")

    finally:
        # Cleanup
        if video_writer is not None:
            video_writer.release()
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Application closed successfully!")

if __name__ == "__main__":
    main()