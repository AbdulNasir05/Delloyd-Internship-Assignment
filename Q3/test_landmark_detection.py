import cv2
import numpy as np
from face_landmark_detection import FaceLandmarkDetector

def test_with_sample_images():
    """Test the landmark detector with sample functionality"""
    detector = FaceLandmarkDetector()
    
    # Create a simple test image with faces (or use a real image)
    print("🧪 Testing Face Landmark Detector...")
    
    # Example of how to use the detector
    image_path = "your_test_image.jpg"  # Replace with actual image path
    
    try:
        result = detector.process_image(image_path, "test_output.jpg")
        if result:
            print("✅ Test passed! Face landmarks detected successfully.")
        else:
            print("❌ Test failed! No faces detected.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_with_sample_images()