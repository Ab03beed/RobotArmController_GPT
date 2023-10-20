import os
import openai
import speech_recognition as sr
import socket
import time

# Constants for Raspberry Pi and Control Unit
RASPBERRY_PI_IP = "YOUR_RASPBERRY_PI_IP"
RASPBERRY_PI_PORT = int("YOUR_RASPBERRY_PI_PORT")
CONTROL_UNIT_IP = "YOUR_CONTROL_UNIT_IP"
CONTROL_UNIT_PORT = int("YOUR_CONTROL_UNIT_PORT")

# Initialize recognizer
recognizer = sr.Recognizer()

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Which box should I move?")
    audio = recognizer.listen(source)

# Convert audio to text using the default recognizer
try:
    voice_command = recognizer.recognize_google(audio)
    print(f"You said: {voice_command}")
except sr.UnknownValueError:
    print("Could not understand the audio.")
    exit()
except sr.RequestError:
    print("Could not request results from the speech recognition service.")
    exit()

# List of possible transcriptions for each box 
box_1_variants = [ 
    "box one", "box 1", "box won", "barks one", "fox one", "books one",  
    "boks one", "bok one", "boxen one", "box on", "bax one", "bux one", 
    "boks ett", "bok ett", "box ett", "bex one", "bogs one", "bog one", 
    "buck one", "buck ett", "bokk one", "bokks one", "boxen ett", "box on ett", 
    "boks on", "boxen on", "bok on", "boxen won", "boxen ett", "bokks won",  
    "bokks on", "bokks ett", "bex won", "bex on", "bex ett" 
] 
box_2_variants = [ 
    "books to","box two", "box 2", "box to", "box too", "barks two", "fox two", "books two", 
    "boks two", "bok two", "boxen two", "box tu", "bax two", "bux two", 
    "boks två", "bok två", "box två", "bex two", "bogs two", "bog two", 
    "buck two", "buck två", "bokk two", "bokks two", "boxen två", "box tu två", 
    "boks tu", "boxen tu", "bok tu", "boxen too", "boxen två", "bokks too",  
    "bokks tu", "bokks två", "bex too", "bex tu", "bex två" 
] 
box_3_variants = [ 
    "box three", "box 3", "barks three", "fox three", "books three", 
    "boks three","books 3", "bok three", "boxen three", "box tree", "bax three", "bux three", 
    "boks tre", "bok tre", "box tre", "bex three", "bogs three", "bog three", 
    "buck three", "buck tre", "bokk three", "bokks three", "boxen tre", "box tree tre", 
    "boks tree", "boxen tree", "bok tree", "boxen trey", "boxen tre", "bokks tree",  
    "bokks trey", "bokks tre", "bex tree", "bex trey", "bex tre" 
] 
voice_command_lower = voice_command.lower()  # Convert the command to lowercase for easier matching 

# Check if any variant is a substring of the transcribed voice command 
if any(variant in voice_command_lower for variant in box_1_variants): 
    which_box = "BOX_1" 
elif any(variant in voice_command_lower for variant in box_2_variants): 
    which_box = "BOX_2" 
elif any(variant in voice_command_lower for variant in box_3_variants): 
    which_box = "BOX_3" 
else: 
    print("Invalid box name in voice command.") 
    exit()
print(which_box) 

openai.api_key = os.getenv("GPT_API_KEY") 
gpt_call = openai.ChatCompletion.create( 
    model="gpt-3.5-turbo", 
    messages=[ 

        {"role": "system", "content": "You are an experienced robot operations coder that will help the user to code a collaborative robot."}, 
        {"role": "user", "content": f""" 
        Imagine we are working with a collaborative robot with the task of moving boxes from a "pick-up table" to a "release table".  
        The three boxes is called BOX_1, BOX_2 and BOX_3. The position of boxes at the pick up table is given in XYZ coordinates: BOX_1(5,3,4), BOX_2(5,4,4), BOX_3(5,5,4).  
        The the cordinate to release boxes at the release table is: (-5,3,4).
        The home position for the robot arm is (0,0,0).
         
        Each time the robot arm has succesfully accomplished what the user asked for, it must move back to its home position, this is very important.
         
        The functions you can use are: 
        go_to_location(X,Y,Z): Moves robot arm end effector to a location specified by XYZ coordinates. Returns nothing. 
        grab(): Robot end effector grabs box. Returns nothing. 
        release(): Robot arm end effector releases box. 
     
        Please have the robot move {which_box} from its pick-up position to its release-position. Return the order in how functions are used, 
        together with a very brief explanation of each step and keep it on the same row as the function that is used. 
        Like this:
        1. function() #explanation 
        2. function() #explanation
        .
        .
        
        No need for a separate explanation.
        """} 
    ] 
) 
gpt_response = gpt_call['choices'][0]['message']['content'] 
print(gpt_response) #sdfasdd

# Establishing connection to the control unit socket and arm
def connect_to_control_unit():
    """Establish connection to the control unit."""
    control_unit_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_unit_socket.connect((CONTROL_UNIT_IP, CONTROL_UNIT_PORT))
    return control_unit_socket

def connect_to_raspberry_pi():
    """Establish connection to the Raspberry Pi."""
    raspberry_pi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raspberry_pi_socket.connect((RASPBERRY_PI_IP, RASPBERRY_PI_PORT))
    return raspberry_pi_socket

# Mapping high-level functions to real-world counterparts
def real_go_to_location(x, y, z, control_unit_socket):
    """Send move command to the control unit."""
    command = f"MOVE TO {x},{y},{z}"
    control_unit_socket.sendall(command.encode())
    response = control_unit_socket.recv(1024).decode()
    if "SUCCESS" not in response:
        raise Exception(f"Failed to move to location {x},{y},{z}. Error: {response}")
    print(response)

def real_grab(raspberry_pi_socket):
    """Send grab command to the Raspberry Pi."""
    command = "GRAB"
    raspberry_pi_socket.sendall(command.encode())
    response = raspberry_pi_socket.recv(1024).decode()
    if "SUCCESS" not in response:
        raise Exception(f"Failed to grab. Error: {response}")
    print(response)

def real_release(raspberry_pi_socket):
    """Send release command to the Raspberry Pi."""
    command = "RELEASE"
    raspberry_pi_socket.sendall(command.encode())
    response = raspberry_pi_socket.recv(1024).decode()
    if "SUCCESS" not in response:
        raise Exception(f"Failed to release. Error: {response}")
    print(response)

def main():
    # Connect to control unit and Raspberry Pi
    control_unit_socket = connect_to_control_unit()
    raspberry_pi_socket = connect_to_raspberry_pi()
    
    # Parsing and executing the gpt_response
    for line in gpt_response.split("\n"):
        if "go_to_location" in line:
            coords = [int(coord) for coord in line.split("(")[1].split(")")[0].split(",")]
            real_go_to_location(*coords, control_unit_socket)
        elif "grab()" in line:
            real_grab(raspberry_pi_socket)
        elif "release()" in line:
            real_release(raspberry_pi_socket)

    # Close the connections
    control_unit_socket.close()
    raspberry_pi_socket.close()

if __name__ == "__main__":
    main()