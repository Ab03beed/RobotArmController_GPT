'''
This Python script is designed to run on a Raspberry Pi and integrates several components 
to control a grabbing mechanism. It utilizes a load cell for measuring force, 
a time-of-flight distance sensor for object detection, an LCD display for visual feedback, 
a servo motor for grabbing and releasing objects, and a Raspberry Pi Camera for capturing images.

'''

# Import necessary libraries and modules
from hx711 import HX711
import RPi.GPIO as GPIO
import statistics
import time
import VL53L1X
import picamera
#from robot_arm.final_all_server import ENABLE
import smbus2 as smbus

# Calibration factors for the load cell
calibration_factor = -39850 * 0.85
calibration_offset = 1096000

# Define LCD display parameters
I2C_ADDR = 0x27  # I2C device address
LCD_WIDTH = 16  # Maximum characters per line

# Define LCD constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_BACKLIGHT = 0x08  # LCD backlight

# Timing constants for LCD
E_PULSE = 0.0005
E_DELAY = 0.0005

# Initialize I2C interface for LCD
bus = smbus.SMBus(1)  # Use 1 for Rev 2 Pi

# Initialize the LCD display
def lcd_init():
    # Initialize display
    lcd_byte(0x33, LCD_CMD)  # Initialize
    lcd_byte(0x32, LCD_CMD)  # Initialize
    lcd_byte(0x06, LCD_CMD)  # Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # Display On, Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(E_DELAY)

# Send a byte to the LCD
def lcd_byte(bits, mode):
    # Send byte to data pins
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

# Toggle enable to send data
def lcd_toggle_enable(bits):
    time.sleep(E_DELAY)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(E_PULSE)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(E_DELAY)

# Send a string to the LCD
def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

# Initialize the servo motor
def initialize_servo():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    p = GPIO.PWM(servoPIN, 50)
    p.start(2.5)
    return p

# Control the servo to grab an object
def grab(p):
    try:
        p.ChangeDutyCycle(6)
        time.sleep(2)
        p.ChangeDutyCycle(2)
    except KeyboardInterrupt:
        pass

# Control the servo to release the grabbed object
def release(p):
    try:
        p.ChangeDutyCycle(6)
        time.sleep(2)
        p.ChangeDutyCycle(2)
    except KeyboardInterrupt:
        pass

# Capture an image using the Raspberry Pi Camera
def capture_image():
    print("About to take a picture:")
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)  # Adjust the resolution as needed
        camera.capture('/home/pi/Desktop/newimage.jpg')  # Updated file path
    print("Picture taken.")

# Main control loop
def main():
    # Initialize the servo
    servo = initialize_servo()

    # Initialize the LCD
    lcd_init()

    tof = None
    try:
        # Initialize the HX711 load cell
        hx711 = HX711(
            dout_pin=5,
            pd_sck_pin=6,
            channel='A',
            gain=64
        )

        # Initialize the VL53L1X distance sensor
        tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        tof.open()
        tof.start_ranging(1)

        while True:
            # Read force measurements from HX711 load cell
            hx711.reset()
            measures = hx711.get_raw_data(times=5)
            mean_value_grams = int(statistics.mean(measures))
            mean_value_kg = (mean_value_grams - calibration_offset) / calibration_factor

            # Read distance from VL53L1X distance sensor
            distance_in_mm = tof.get_distance()

            # Print force and distance values
            print("Force (kg):", mean_value_kg)
            print("Distance:", distance_in_mm, "mm")

            # Display information on the LCD
            lcd_string("Force (kg): {:.2f}".format(mean_value_kg), LCD_LINE_1)
            lcd_string("Distance: {} mm".format(distance_in_mm), LCD_LINE_2)

            if distance_in_mm < 40 or mean_value_kg > 75:
                # Perform grabbing action and capture an image
                grab(servo)
                time.sleep(10)
                capture_image()
            if distance_in_mm > 40:
                # Release the grabbed object
                release(servo)
                time.sleep(5)
            if distance_in_mm > 100:
                print("There is no object")

            time.sleep(1)  # Wait for a second before the next loop iteration

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup GPIO and close sensors
        if tof is not None:
            tof.stop_ranging()
            tof.close()
        servo.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
