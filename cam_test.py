from picamera2 import Picamera2
import time
import sys

# Initialize the camera
picam2 = Picamera2()

# Configure the camera to use a specific preview size
# This helps with stability
preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(preview_config)

print("Starting camera preview...")

try:
    picam2.start()
    
    # Wait for a moment to let the camera warm up
    time.sleep(2)
    
    # Keep the preview window open until the user stops the script
    print("Camera is active. Press 'Ctrl+C' to close the preview.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nTest stopped by user.")

finally:
    # Always stop the camera and close the preview window
    picam2.stop()
    print("Camera preview closed.")
    sys.exit()
