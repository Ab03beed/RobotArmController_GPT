import os 
import openai 
import speech_recognition as sr 
#ABBE HAR ÄNDRAT HÄR.
# Initialize recognizer 
recognizer = sr.Recognizer() 

# Capture audio from the microphone 
with sr.Microphone() as source: 
    print("WHich box should I move?") 
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
    "box two", "box 2", "box to", "box too", "barks two", "fox two", "books two", 
    "boks two", "bok two", "boxen two", "box tu", "bax two", "bux two", 
    "boks två", "bok två", "box två", "bex two", "bogs two", "bog two", 
    "buck two", "buck två", "bokk two", "bokks two", "boxen två", "box tu två", 
    "boks tu", "boxen tu", "bok tu", "boxen too", "boxen två", "bokks too",  
    "bokks tu", "bokks två", "bex too", "bex tu", "bex två" 
] 
box_3_variants = [ 
    "box three", "box 3", "barks three", "fox three", "books three", 
    "boks three", "bok three", "boxen three", "box tree", "bax three", "bux three", 
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
        {"role": "system", "content": "You are a helpful assistant."}, 
        {"role": "user", "content": f""" 
        Imagine we are working with a collaborative robot with the task of moving boxes between two tables.  
        After each task the robot arm moves back to its home position.Such that each task starts out from the home position. 
        There are three different boxes at different positions.
        The three boxes are called BOX_1, BOX_2 and BOX_3. The position of boxes is given in XYZ coordinates. 
        The box’s pick-up positions: BOX_1_pickup(5,3,4), BOX_2_pickup(5,4,4), BOX_3_pickup(5,5,4).  
        The box’s release-positions: BOX_1_release(-5,3,4), BOX_2_release(-5,4,4), BOX_3_release(-5,5,4)
          
        The functions you can use are: 
        go_to_location(box_name_...pickup or release): Moves robot arm to a location specified by XYZ coordinates. Returns nothing. 
        grab_box(box_name): Robot arm end effector grabs the box of interest. Returns nothing. 
        release_box(box_name): Robot arm end effector releases the box being grabbed. 
        go_to_home_position(): Robot arm moves back to starting position at XYZ coordinate (0,0,0) 
        Please have the robot move {which_box} from its pick-up position to its release-position. 
        """} 
    ] 
) 
gpt_response = gpt_call['choices'][0]['message']['content'] 
print(gpt_response) 

# Function to send commands to the robotic arm 
def send_to_robotic_arm(command): 
    # This function will send the command to the robotic arm through the socket. 
    # You'll need to implement the socket communication here. 
    pass 

# Mapping high-level functions to actual robotic arm commands 
def go_to_location(box_name): 
    if box_name.endswith("pickup"): 
        coords = box_name.replace("_pickup", "") 
        x, y, z = box_coords[coords]  # Assuming you have a dictionary with box coordinates 
    elif box_name.endswith("release"): 
        coords = box_name.replace("_release", "") 
        x, y, z = box_coords[coords] 
    else: 
        print("Invalid box name for location.") 
        return 
    command = f"MOVE P[{x},{y},{z}]"  # This is a hypothetical command; adjust based on actual syntax 
    send_to_robotic_arm(command) 

def grab_box(box_name): 
    command = "GRAB"  # Hypothetical command to close the end effector 
    send_to_robotic_arm(command) 

def release_box(box_name): 
    command = "RELEASE"  # Hypothetical command to open the end effector 
    send_to_robotic_arm(command) 

def go_to_home_position(): 
    command = "MOVE P[0,0,0]"  # Moving to the home position 
    send_to_robotic_arm(command) 

# Parsing GPT-3's response to call the appropriate functions 
# This is a basic example; you might need to adjust based on the exact response format 
if "go_to_location" in gpt_response: 
    box_name = gpt_response.split("go_to_location(")[1].split(")")[0] 
    go_to_location(box_name) 
elif "grab_box" in gpt_response: 
    box_name = gpt_response.split("grab_box(")[1].split(")")[0] 
    grab_box(box_name) 
elif "release_box" in gpt_response: 
    box_name = gpt_response.split("release_box(")[1].split(")")[0] 
    release_box(box_name) 
elif "go_to_home_position" in gpt_response: 
    go_to_home_position() 