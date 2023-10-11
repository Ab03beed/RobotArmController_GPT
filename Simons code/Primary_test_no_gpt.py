import os
import openai
import speech_recognition as sr
import socket
import time

# Constants for Raspberry Pi and Control Unit connection details
RASPBERRY_PI_IP = '127.0.0.1'
RASPBERRY_PI_PORT = 12345
CONTROL_UNIT_IP = '127.0.0.1'
CONTROL_UNIT_PORT = 10002


gpt_response = """1. go_to_location(190,-200,300) # Moves robot arm end effector to the location of BOX_3
2. grab() # Robot arm end effector grabs BOX_3
3. go_to_location(190,-200,430) # The robot moves straight up (+130 in Z axis) to avoid collision with other boxes
4. go_to_location(190,200,430) # The robot moves above the release location for BOX_3, while still maintaining a higher position to avoid collision
5. go_to_location(190,200,300) # The robot moves down to the release location for BOX_3
6. release() # The robot releases BOX_3 at the designated position
7. go_to_location(270,0,504) # The robot goes back to its home position"""
print(gpt_response)

# Establishing connection to the control unit socket and arm
def establish_connection(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    return s

control_unit_socket = establish_connection(CONTROL_UNIT_IP, CONTROL_UNIT_PORT)#The establish_connection function is invoked with the CONTROL_UNIT_IP and CONTROL_UNIT_PORT as arguments.
raspberry_pi_socket = establish_connection(RASPBERRY_PI_IP, RASPBERRY_PI_PORT)#--''--


def send_to_robotic_arm(command):
    control_unit_socket.sendall(command.encode())
    response = control_unit_socket.recv(1024).decode()
    return response

def send_to_raspberry_pi(command):
    raspberry_pi_socket.sendall(command.encode())
    response = raspberry_pi_socket.recv(1024).decode()
    return response

def real_go_to_location(x, y, z):
    command = f"{x},{y},{z}"
    response = send_to_robotic_arm(command)
    if "MOVE COMPLETED" not in response:
        print(f"Error moving to location {x},{y},{z}: {response}")
        exit()
    print(response)

def real_grab():
    response = send_to_raspberry_pi("GRAB")
    if "GRAB COMPLETE" not in response:
        print(f"Error grabbing: {response}")
        exit()
    print(response)

def real_release():
    response = send_to_raspberry_pi("RELEASE")
    if "RELEASE COMPLETE" not in response:
        print(f"Error releasing: {response}")
        exit()
    print(response)

def main():
    for line in gpt_response.split("\n"):
        if "go_to_location" in line:
            coords = [int(coord) for coord in line.split("(")[1].split(")")[0].split(",")]
            real_go_to_location(*coords)
        elif "grab()" in line:
            real_grab()
        elif "release()" in line:
            real_release()

if __name__ == "__main__":
    main()

#closing the sockets after all tasks are done
control_unit_socket.close()
raspberry_pi_socket.close()