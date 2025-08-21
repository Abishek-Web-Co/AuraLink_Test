from picamera2 import Picamera2
import time
import sys
import cv2
import numpy as np

# Initialize the camera
picam2 = Picamera2()

# Configure the camera to use a specific preview size
# The main stream needs to have a format that OpenCV can use (like BGR888)
# We also use a smaller resolution for better performance
preview_config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "XBGR8888"})
picam2.configure(preview_config)

# Start the camera without a default preview window
picam2.start()

print("Starting camera preview in OpenCV window...")
print("Press 'q' to close the window.")

try:
    while True:
        # Capture a single frame as a NumPy array
        frame = picam2.capture_array()
        
        # Convert the frame to a BGR format for OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        
        # Flip the frame horizontally to mirror the video
        frame = cv2.flip(frame, 1)
        
        # Display the frame in a new window named 'Camera Preview'
        cv2.imshow('Camera Preview', frame)
        
        # Check for the 'q' key to quit the program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
except KeyboardInterrupt:
    print("\nTest stopped by user.")

finally:
    # Stop the camera and close all OpenCV windows
    picam2.stop()
    cv2.destroyAllWindows()
    print("Camera preview closed.")
    sys.exit()
