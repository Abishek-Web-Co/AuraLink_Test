import gpiozero
import time

# --- HC-SR04 Setup ---
# The DistanceSensor class handles both the trigger and echo pins
# It automatically performs the correct timing measurements
ultrasonic = gpiozero.DistanceSensor(echo=24, trigger=23)

print("HC-SR04 Initialized.")

# Main test loop
try:
    print("Starting ultrasonic sensor test. Press 'Ctrl+C' to quit.")
    
    while True:
        # The .distance property gives you the distance in meters
        # We multiply by 100 to convert to centimeters
        dist_cm = ultrasonic.distance * 100
        
        print("Distance: {:.2f} cm".format(dist_cm))
        time.sleep(1) # Wait 1 second before the next measurement

except KeyboardInterrupt:
    print("Test stopped by user.")

finally:
    # gpiozero handles cleanup automatically
    print("Cleanup complete.")
