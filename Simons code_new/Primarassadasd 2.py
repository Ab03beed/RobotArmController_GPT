import os
import openai


# Constants for Raspberry Pi and Control Unit connection details
which_box="BOX_1"
print(which_box)

# Set OpenAI API key
openai.api_key = os.getenv("GPT_API_KEY")
# Make a call to the OpenAI GPT model to get instructions for robot operations
print("waiting for response from GPT 4 API")
gpt_call = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[ 
        {"role": "system", "content": "You are an experienced robot operations coder that will help the user to code a collaborative robot."}, 
        {"role": "user", "content": f"""
        Imagine we are working with a collaborative robot with the task of moving four boxes from a "grabbing table" to a "release table".  
         
         
         

        The four boxes is called BOX_1, BOX_2 and BOX_3 and BOX_4. 
         
        The coordinates (XYZ) to grab boxes: BOX_1(90,-220,245), BOX_2(90,-400,245), BOX_3(-90,-400,245), BOX_4(-90,-220,245).  .  
         
        The cordinates (XYZ) to release boxes: BOX_1(90, 400, 245), BOX_2(90, 220, 245), BOX_3(-90, 220, 245), BOX_4(-90, 400, 245).

         When moving to and from grab & release positions, the robot arm should follow this general logic:
        
        1. The step just before moving to grab position should always be the following coordinates: BOX_1(90,-220,345), BOX_2(90,-400,345), BOX_3(-90,-400,345), BOX_4(-90,-220,345)
        2. The step just before moving from release position should always be the following coordinates: BOX_1(90, 400, 345), BOX_2(90, 220, 345), BOX_3(-90, 220, 345), BOX_4(-90, 400, 345)
        3. Avoid collisions with other boxes by visiting collision avoidance coordinates when going to and from grab and release positions:
            *collision avoidance coordinates when grabbing:BOX_1(90,-220,435), BOX_2(90,-400,435), BOX_3(-90,-400,435), BOX_4(-90,-220,435)
            *collision avoidance coordinates when releasing: BOX_1(90, 400, 435), BOX_2(90, 220, 435), BOX_3(-90, 220, 435), BOX_4(-90, 400, 435)
       
         
        The home position (XYZ) for the robot arm is: (270,0,504).
        The program should always end with the robot arm going to its home position.
         
         
        *The functions you can use are: 
            -go_to_location(X,Y,Z): Moves robot arm end effector to a location specified by XYZ coordinates. Returns nothing. 
            -grab(): Robot end effector grabs box. Returns nothing. 
            -release(): Robot arm end effector releases box.

          Example when moving BOX_1:
         *Go to BOX_1(90,-220,435)
         *Go to BOX_1(90,-220,345)
         *Go to BOX_1(90,-220,245)
         *grab()
         *Go to BOX_1(90,-220,435)
         *Go to BOX_1(90, 400, 245)
         *release()
         *go to BOX_1(90, 400, 345)
         *go to BOX_1(90, 400, 435)
         *go to (270,0,504)
         
        
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
