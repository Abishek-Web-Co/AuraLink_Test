from gpiozero import Servo
import smbus
from time import sleep

# Setup servo on GPIO pin 4
servo = Servo(17)

# MPU6050 Registers and Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F

bus = smbus.SMBus(1)  # I2C bus
Device_Address = 0x68  # MPU6050 device address

def MPU_Init():
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr + 1)
    value = ((high << 8) | low)
    if value > 32768:
        value = value - 65536
    return value

# Function to set servo angle (0 to 180 degrees)
def set_angle(angle):
    # Map 0â€“180 to -1 to 1
    value = (angle - 90) / 90
    value = max(-1, min(1, value))  # Clamp to [-1, 1]
    servo.value = value

# Initialize MPU6050
MPU_Init()

try:
    while True:
        # Read Accelerometer raw values
        acc_x = read_raw_data(ACCEL_XOUT)
        acc_y = read_raw_data(ACCEL_YOUT)
        acc_z = read_raw_data(ACCEL_ZOUT)

        # Convert to 'g'
        Ax = acc_x / 16384.0
        Ay = acc_y / 16384.0
        Az = acc_z / 16384.0

        # Map Ay (-1 to 1) â†’ Servo Angle (0 to 180)
        in_min = -1.0
        in_max = 1.0
        out_min = 0
        out_max = 180

        value = (Ay - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        value = max(0, min(180, int(value)))  # Clamp between 0 and 180

        print(f"Ay={Ay:.2f}, Servo Angle={value}")
        set_angle(value)

        sleep(0.08)

except KeyboardInterrupt:
    print("Program stopped by user")
