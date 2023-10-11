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

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Which box should I move?")
    audio = recognizer.listen(source)
    

# Convert the captured audio to text using Google's speech recognition
try:
    voice_command = recognizer.recognize_google(audio)
    print(f"You said: {voice_command}")
except sr.UnknownValueError:
    # Handle unrecognized audio
    print("Could not understand the audio.")
    exit()
except sr.RequestError:
    # Handle request errors
    print("Could not request results from the speech recognition service.")
    exit()

# Lists of possible transcriptions for each box to handle misinterpretations
# or different pronunciations/accent variations
box_1_variants = [ 
    "box one", "box 1", "box won", "barks one", "fox one", "books one",  
    "boks one", "bok one", "boxen one", "box on", "bax one", "bux one", 
    "boks ett", "bok ett", "box ett", "bex one", "bogs one", "bog one", 
    "buck one", "buck ett", "bokk one", "bokks one", "boxen ett", "box on ett", 
    "boks on", "boxen on", "bok on", "boxen won", "boxen ett", "bokks won",  
    "bokks on", "bokks ett", "bex won", "bex on", "bex ett", "volkswagen" 
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

# Convert the voice command to lowercase for easier matching
voice_command_lower = voice_command.lower()

# Check which box the user referred to in their voice command
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

# Set OpenAI API key
openai.api_key = os.getenv("GPT_API_KEY")
# Make a call to the OpenAI GPT model to get instructions for robot operations
gpt_call = openai.ChatCompletion.create( 
    model="gpt-4", 
    messages=[ 
        {"role": "system", "content": "You are an experienced robot operations coder that will help the user to code a collaborative robot."}, 
        {"role": "user", "content": f""" 
        Imagine we are working with a collaborative robot with the task of moving boxes from a "pick-up table" to a "release table".  
        The three boxes is called BOX_1, BOX_2 and BOX_3. The position of boxes at the pick up table is given in XYZ coordinates: BOX_1(410,-200,100), BOX_2(300,-200,100), BOX_3(190,-200,100).  
        The the cordinate to release boxes at the release table is: (400,200,100).
        The home position for the robot arm is (270,0,504).
        
        When the arm goes to pick-up table or release table its coordinate must be adjusted to take account for the end effectors size.
        Adjustment is: (X,Y,+200) in relation to box coordinate. After picking up a box is must first move straight up (X,Y,+300)
        in relation to box coordinate, before going to release position.
         
        Each time the robot arm has succesfully accomplished what the user asked for, it is very important that it moves back to its home position.
         
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