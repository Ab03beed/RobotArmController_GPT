import os 
import openai 
import speech_recognition as sr 
import socket
# Initialize recognizer 
recognizer = sr.Recognizer() 
#sssss
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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Establishing connection to the control unit socket and arm
CONTROL_UNIT_IP = "YOUR_CONTROL_UNIT_IP"  # Replace with your control unit's IP address
CONTROL_UNIT_PORT = "YOUR_CONTROL_UNIT_PORT"  # Replace with your control unit's port number
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((CONTROL_UNIT_IP, CONTROL_UNIT_PORT))

def send_to_robotic_arm(command): #Sends a command to the Mitsubishi robotic arm over a socket connection, waits for a response, and then returns that response as a string.
    """Send command to the Mitsubishi robotic arm."""
    sock.sendall(command.encode())#After sending the command to the robotic arm
    response = sock.recv(1024) #Waits for a response from the robotic arm. 1024 specifies the maximum amount of data (in bytes) that should be read at once.
    return response.decode() 

# Mapping high-level functions to real-world counterparts
def go_to_location(x, y, z):
    # Translate to the actual command for the Mitsubishi robotic arm
    command = f"MOVE TO {x},{y},{z}"  #PLACEHOLDER: replace with the actual command format
    response = send_to_robotic_arm(command)
    print(response)  # For debugging purposes

def grab():
    # Communicate with the Raspberry Pi to close the claw
    #PLACEHOLDER: replace with the actual method to communicate with the Raspberry Pi
    pass

def release():
    # Communicate with the Raspberry Pi to open the claw
    #PLACEHOLDER: replace with the actual method to communicate with the Raspberry Pi
    pass

#Parsing and executing the gpt_response
for line in gpt_response.split("\n"):  # Split the gpt_response into individual lines and iterate over each line.
    if "go_to_location" in line:  # Check if the line contains the "go_to_location" command.
        coords = [int(coord) for coord in line.split("(")[1].split(")")[0].split(",")] # Extract the coordinates from the line.For a line like "go_to_location(5,3,4)", this will extract the list [5, 3, 4].
        go_to_location(*coords)  # Call the go_to_location function with the extracted coordinates.
    elif "grab()" in line:  # Check if the line contains the "grab()" command.
        grab()  # Call the grab function to execute the grab action.
    elif "release()" in line:  # Check if the line contains the "release()" command.
        release()  # Call the release function to execute the release action.

sock.close()  # Close the connection after executing all commands