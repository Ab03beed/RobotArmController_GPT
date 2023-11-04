'''
This Python script is designed to run on a Raspberry Pi and 
serves as a control system for a mechanical grabbing mechanism. 
It communicates with a load cell (HX711) to measure the force applied and
a servo motor to control the grabbing and releasing of objects
'''

# Import necessary libraries and modules
from hx711 import HX711
import RPi.GPIO as GPIO
import socket
import statistics
import pigpio
import smbus2 as smbus
import time

# Calibration factors for the load cell
calibration_factor = -39850 * 0.85
calibration_offset = 1096000

# Global variables
servo_action_completed = False
GPIO.setwarnings(False)

# The `pressure` variable defines the threshold force for grabbing.
pressure = 1

# Define the GPIO pin used for the servo motor.
servo = 17

# Function to initialize the servo motor
def initialize_servo():
    servoPIN = 17

    # Initialize the pigpio instance for servo control
    p = pigpio.pi()
    p.set_mode(servo, pigpio.OUTPUT)
    p.set_PWM_frequency(servo, 50)

    # Initialize the servo position
    p.set_servo_pulsewidth(servo, 500)
    return p

# Initialize the HX711 load cell
try:
    hx711 = HX711(
        dout_pin=5,
        pd_sck_pin=6,
        channel='A',
        gain=64
    )
except Exception as e:
    print("Error initializing HX711:", e)
hx711.reset()

# Initialize a variable to store old measured values
oldMeasuredValue = 0

# Function to measure force using the load cell
def measure_force():
    global oldMeasuredValue
    measure_false = True

    while measure_false:
        measures = hx711.get_raw_data(times=2)
        mean_value_grams = int(statistics.mean(measures))
        mean_value_kg = (mean_value_grams - calibration_offset) / calibration_factor

        # Wait until the measured force stabilizes
        if abs(mean_value_kg - oldMeasuredValue) < 1:
            measure_false = False
            oldMeasuredValue = mean_value_kg

    return mean_value_kg

# Function to control the servo to grab an object
def grab(p):
    DutyCycle = 500

    while measure_force() < pressure:

        # Increase the servo's pulse width incrementally
        DutyCycle = min(DutyCycle + 100, 2500)
        p.set_servo_pulsewidth(servo, DutyCycle)

# Function to release the grabbed object
def release(p):
    # Reset the servo to its initial position
    p.set_servo_pulsewidth(servo, 500)

    # Wait for a specified time (1.5 seconds) before resetting the oldMeasuredValue
    time.sleep(1.5)
    global oldMeasuredValue
    oldMeasuredValue = 0

# Function to start the server and listen for commands
def start_server():
    global servo_action_completed
    global oldMeasuredValue
    oldMeasuredValue = 0

    # Define the server's host and port
    HOST = '192.168.0.71'
    PORT = 12348

    # Create a socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print("Waiting for connection...")

    # Initialize the servo control
    p = initialize_servo()

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        while True:
            if conn is None:
                conn, addr = s.accept()
                print(f"Connected by {addr}")

            data = conn.recv(1024).decode()
            print(data)

            if not data:
                break

            if data == "GRAB":
                grab(p)
                measure_force()
                time.sleep(1.5)
                conn.sendall("GRAB COMPLETED".encode())

            elif data == "RELEASE":
                release(p)
                conn.sendall("RELEASE COMPLETED".encode())

    conn.close()

# Start the server
start_server()
