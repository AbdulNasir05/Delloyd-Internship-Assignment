import cv2
import numpy as np
import datetime
import os

# DNN model files (will be downloaded automatically if not present)
DNN_MODEL_URL = "https://github.com/opencv/opencv/raw/master/samples/dnn/face_detector/"
DNN_MODEL_FILE = "opencv_face_detector_uint8.pb"
DNN_CONFIG_FILE = "opencv_face_detector.pbtxt"

def download_dnn_model():
    """Download DNN model files if they don't exist"""
    if not os.path.exists(DNN_MODEL_FILE) or not os.path.exists(DNN_CONFIG_FILE):
        print("⚠️  DNN model files not found. Downloading...")
        try:
            import urllib.request
            urllib.request.urlretrieve(f"{DNN_MODEL_URL}{DNN_MODEL_FILE}", DNN_MODEL_FILE)
            urllib.request.urlretrieve(f"{DNN_MODEL_URL}{DNN_CONFIG_FILE}", DNN_CONFIG_FILE)
            print("✅ DNN model files downloaded successfully!")
        except Exception as e:
            print(f"❌ Failed to download DNN model: {e}")
            return False
    return True

def detect_faces_haar(frame):
    """Haar Cascade face detector (fast but less accurate)"""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(40, 40),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    return faces

def detect_faces_dnn(frame, confidence_threshold=0.7):
    """DNN-based face detector (more accurate but slower)"""
    # Check if model files exist
    if not os.path.exists(DNN_MODEL_FILE) or not os.path.exists(DNN_CONFIG_FILE):
        print("❌ DNN model files missing. Falling back to Haar cascade.")
        return detect_faces_haar(frame)
    
    try:
        # Load DNN model
        net = cv2.dnn.readNetFromTensorflow(DNN_MODEL_FILE, DNN_CONFIG_FILE)
        
        # Create blob from frame
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123])
        net.setInput(blob)
        
        # Run detection
        detections = net.forward()
        
        faces = []
        h, w = frame.shape[:2]
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > confidence_threshold:
                # Get bounding box coordinates
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                x1, y1, x2, y2 = box.astype('int')
                
                # Ensure coordinates are within frame bounds
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                
                width = x2 - x1
                height = y2 - y1
                
                if width > 0 and height > 0:
                    faces.append([x1, y1, width, height])
        
        return faces
        
    except Exception as e:
        print(f"❌ DNN detection error: {e}. Falling back to Haar cascade.")
        return detect_faces_haar(frame)

def detect_faces_yunet(frame, confidence_threshold=0.8):
    """YuNet face detector (modern, accurate)"""
    try:
        # Initialize YuNet detector
        detector = cv2.FaceDetectorYN.create(
            "face_detection_yunet_2023mar.onnx",  # Model file
            "",
            (320, 320),  # Input size
            confidence_threshold,
            0.3,  # NMS threshold
            5000  # Top K
        )
        
        if detector is None:
            print("❌ YuNet model not available. Falling back to DNN.")
            return detect_faces_dnn(frame)
        
        # Set input size
        h, w = frame.shape[:2]
        detector.setInputSize((w, h))
        
        # Detect faces
        _, faces = detector.detect(frame)
        
        if faces is None:
            return []
        
        # Convert YuNet format to [x, y, w, h]
        result = []
        for face in faces:
            x, y, w, h = face[:4].astype(int)
            result.append([x, y, w, h])
        
        return result
        
    except Exception as e:
        print(f"❌ YuNet detection error: {e}. Falling back to DNN.")
        return detect_faces_dnn(frame)

def detect_faces_multi_method(frame, detector_type='haar', confidence=0.7):
    """Unified face detection function supporting multiple methods"""
    if detector_type == 'haar':
        return detect_faces_haar(frame)
    elif detector_type == 'dnn':
        return detect_faces_dnn(frame, confidence)
    elif detector_type == 'yunet':
        return detect_faces_yunet(frame, confidence)
    else:
        return detect_faces_haar(frame)  # Default fallback

def blur_faces(frame, faces, blur_strength=15):
    """Blur detected faces with adjustable strength"""
    blurred_frame = frame.copy()
    
    for (x, y, w, h) in faces:
        # Ensure we don't go out of frame bounds
        y1, y2 = max(0, y), min(frame.shape[0], y + h)
        x1, x2 = max(0, x), min(frame.shape[1], x + w)
        
        if y2 > y1 and x2 > x1:
            # Extract the face region
            face_region = frame[y1:y2, x1:x2]
            
            # Calculate kernel size based on blur strength
            kernel_size = blur_strength * 2 + 1
            kernel_size = max(11, min(151, kernel_size))
            
            # Apply Gaussian blur
            blurred_face = cv2.GaussianBlur(face_region, (kernel_size, kernel_size), 0)
            
            # Replace the face region with the blurred version
            blurred_frame[y1:y2, x1:x2] = blurred_face
    
    return blurred_frame

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    # Set resolution for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Video properties: {width}x{height} at {fps} FPS")
    
    # Download DNN models if needed
    download_dnn_model()
    
    # Application settings
    is_recording = False
    video_writer = None
    recording_start_time = None
    blur_strength = 15
    show_debug = False
    
    # Available detectors
    detectors = [
        ('haar', 'Haar Cascade (Fast)'),
        ('dnn', 'DNN (Accurate)'),
        ('yunet', 'YuNet (Modern)')
    ]
    current_detector_index = 0
    detection_confidence = 0.7
    
    # Create recordings directory
    os.makedirs('recordings', exist_ok=True)
    
    print("🎯 Advanced Face Blurring with Multiple Detection Models")
    print("=" * 60)
    print("Controls:")
    print("s - Start/stop recording")
    print("+ - Increase blur strength")
    print("- - Decrease blur strength")
    print("m - Switch detection model")
    print("c - Increase detection confidence")
    print("v - Decrease detection confidence")
    print("d - Toggle debug mode")
    print("x - Capture screenshot")
    print("q - Quit application")
    print("=" * 60)
    
    current_detector_name = detectors[current_detector_index][1]
    print(f"🔍 Current detector: {current_detector_name}")
    print(f"🎯 Detection confidence: {detection_confidence}")
    
    recording_blink_counter = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Error: Could not read frame")
                break
            
            frame = cv2.flip(frame, 1)
            
            # Detect faces using current method
            current_detector_type = detectors[current_detector_index][0]
            faces = detect_faces_multi_method(frame, current_detector_type, detection_confidence)
            
            # Blur faces
            processed_frame = blur_faces(frame, faces, blur_strength)
            
            # UI Overlay
            y_offset = 30
            cv2.putText(processed_frame, f"Faces: {len(faces)}", (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            y_offset += 25
            
            detector_display = detectors[current_detector_index][1].split(' ')[0]
            cv2.putText(processed_frame, f"Detector: {detector_display}", (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            y_offset += 20
            
            kernel_size = blur_strength * 2 + 1
            cv2.putText(processed_frame, f"Blur: {blur_strength}", (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 200, 0), 1)
            y_offset += 20
            
            cv2.putText(processed_frame, f"Confidence: {detection_confidence:.2f}", (10, y_offset), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 150, 255), 1)
            
            # Debug mode - show face boxes and confidence
            if show_debug:
                for (x, y, w, h) in faces:
                    cv2.rectangle(processed_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(processed_frame, f"Face", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
            # Recording indicator
            if is_recording:
                recording_blink_counter += 1
                if recording_blink_counter % 30 < 15:
                    cv2.putText(processed_frame, "RECORDING", (width - 120, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    cv2.circle(processed_frame, (width - 30, 30), 6, (0, 0, 255), -1)
            
            # Display
            cv2.imshow('Advanced Face Blurring - Multiple Detection Models', processed_frame)
            
            # Recording
            if is_recording and video_writer is not None:
                video_writer.write(processed_frame)
            
            # Key handling
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                if not is_recording:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"recordings/face_blurred_{timestamp}.avi"
                    
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    video_writer = cv2.VideoWriter(filename, fourcc, fps, (width, height))
                    
                    is_recording = True
                    recording_start_time = datetime.datetime.now()
                    print(f"🎥 Started recording: {filename}")
                    
                else:
                    if video_writer is not None:
                        video_writer.release()
                        video_writer = None
                    
                    duration = (datetime.datetime.now() - recording_start_time).total_seconds()
                    print(f"⏹️ Stopped recording. Duration: {duration:.2f} seconds")
                    is_recording = False
            
            elif key == ord('+'):
                old_strength = blur_strength
                blur_strength = min(75, blur_strength + 5)
                if old_strength != blur_strength:
                    kernel_size = blur_strength * 2 + 1
                    print(f"🔺 Blur strength: {blur_strength} (Kernel: {kernel_size}x{kernel_size})")
            
            elif key == ord('-'):
                old_strength = blur_strength
                blur_strength = max(5, blur_strength - 5)
                if old_strength != blur_strength:
                    kernel_size = blur_strength * 2 + 1
                    print(f"🔻 Blur strength: {blur_strength} (Kernel: {kernel_size}x{kernel_size})")
            
            elif key == ord('m'):
                # Switch detection model
                current_detector_index = (current_detector_index + 1) % len(detectors)
                detector_name = detectors[current_detector_index][1]
                print(f"🔁 Detection model: {detector_name}")
            
            elif key == ord('c'):
                # Increase detection confidence
                old_confidence = detection_confidence
                detection_confidence = min(0.95, detection_confidence + 0.05)
                if old_confidence != detection_confidence:
                    print(f"🎯 Detection confidence: {detection_confidence:.2f}")
            
            elif key == ord('v'):
                # Decrease detection confidence
                old_confidence = detection_confidence
                detection_confidence = max(0.3, detection_confidence - 0.05)
                if old_confidence != detection_confidence:
                    print(f"🎯 Detection confidence: {detection_confidence:.2f}")
            
            elif key == ord('d'):
                show_debug = not show_debug
                status = "ON" if show_debug else "OFF"
                print(f"🐛 Debug mode: {status}")
            
            elif key == ord('x'):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recordings/screenshot_{timestamp}.jpg"
                cv2.imwrite(filename, processed_frame)
                print(f"📸 Screenshot saved: {filename}")

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if video_writer is not None:
            video_writer.release()
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Application closed successfully!")

if __name__ == "__main__":
    main()