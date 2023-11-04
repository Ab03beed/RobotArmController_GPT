'''
This Python script facilitates communication with a Raspberry Pi to control a grabbing mechanism
(the code is just for a test only for the electro without data).
It establishes a network connection to the Raspberry Pi, 
enabling the user to send commands for grabbing objects with adjustable strength and releasing them.

'''

import socket
import time

# Raspberry Pi network configuration
RASPBERRY_PI_IP = "192.168.0.71"
RASPBERRY_PI_PORT = 12348

# Function to send a command to the Raspberry Pi
def send_to_raspberry_pi(command):
    # Send the command to the Raspberry Pi and receive a response
    raspberry_pi_socket.sendall(command.encode())
    response = raspberry_pi_socket.recv(1024).decode()
    return response

# Function to establish a network connection to the Raspberry Pi
def establish_connection(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    return s

# Placeholder function for measuring force (to be implemented)
def measure_force():
    pass

# Initialize the network connection to the Raspberry Pi
raspberry_pi_socket = establish_connection(RASPBERRY_PI_IP, RASPBERRY_PI_PORT)

# Function to perform a grab action with adjustable strength
def grab(strength):
    # Adjust the servo control logic here based on your hardware
    print(f"Grabbing with strength: {strength}")
    time.sleep(2)  # Simulated grab
    if strength == "0" or strength == "1" or strength == "2":
        # Perform the real grab action and measure the force
        response = send_to_raspberry_pi("GRAB")
        if "COMPLETED" in response:
            measure_force()
        else:
            print(f"Error grabbing: {response}")
            exit()
        print(response)

# Function to release the grabbed object
def real_release():
    response = send_to_raspberry_pi("RELEASE")
    if "COMPLETED" not in response:
        print(f"Error releasing: {response}")
        exit()
    print(response)

# Main control loop for user interaction
def main():
    try:
        while True:
            value = input("Enter 0 for soft grab, 1 for middle grab, 2 for hard grab, 3 for release, or X to exit: ").lower()
            if value == "0" or value == "1" or value == "2":
                grab(value)
            elif value == "3":
                real_release()
            elif value == "x":
                break
            else:
                print("Invalid value. Please enter 0, 1, 2, 3, or X to exit.")
            
            run_again = input("Do you want to run the code again? (Y/N): ").lower()
            if run_again != "y":
                break

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
