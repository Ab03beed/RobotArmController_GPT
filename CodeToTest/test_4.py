from Modules.speechToText import SpeechToText

from Modules.robotController import RobotController
import keyboard
import time

#192.168.0.71
r1 = RobotController("127.0.0.1", 10002, "127.0.0.1", 12345)

def fetchBox(prompt):
    for line in prompt.split("\n"):
        if "go_to_location" in line:
            coords = [int(coord) for coord in line.split("(")[1].split(")")[0].split(",")]
            command = f"{coords[0]},{coords[1]},{coords[2]}"
            res = r1.sendTo(r1.robotSoc, command)
            print(res)
        elif "grab()" in line:
            res = r1.sendTo(r1.raspSoc, "GRAB")
            print(res)
        elif "release()" in line:
            res = r1.sendTo(r1.raspSoc, "RELEASE")
            print(res)


def main():
    #Object of RobotController class
    
    #Object of SpeechToText class
    sp = SpeechToText()

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
    box_4_variants = [
            "box 4.","box 4.","box 4","box for", "bucks for","box four","fox four", "box before","box floor","pox for", "blocks for",
            "barks for","box for the","books for","box before the", "boss for","boat's for","box for the win",
            "bucks for the","boxing for","box before four","box for you","backs for","boxing four","box of four",
            "box or four","boxing for the","box it for","bucks for the win","boxed for","books for the","box it before",
            "box or the four"
        ]
    
    box1_reply = """
                1. go_to_location(270,0,504) #Robot arm goes to home position.
                2. go_to_location(90,-220,435) #Robot arm moves to collision avoidance position of BOX_1.
                3. go_to_location(90,-220,245) #Robot arm goes to the position of BOX_1 to pick it up.
                4. grab() #Robot arm grabs BOX_1.
                5. go_to_location(90,-220,435) #Robot arm moves BOX_1 to collision avoidance position before setting off to the release position.
                6. go_to_location(90,400,435) #Robot arm moves BOX_1 to collision avoidance position above the release position.
                7. go_to_location(90,400,245) #Robot arm moves BOX_1 to the release position.
                8. release() #Robot arm releases BOX_1.
                9. go_to_location(90,400,435) #Robot arm moves to collision avoidance position after releasing the BOX_1.     
                10. go_to_location(270,0,504) #Robot arm returns to home position.
                """

    box2_reply ="""
                1. go_to_location(270,0,504) #Starting from the home position.
                2. go_to_location(90,-400,435) # Move to the grabbing collision avoidance position for BOX_2.
                3. go_to_location(90,-400,245) # Move to the exact grabbing position for BOX_2.
                4. grab() # Grab BOX_2 from the grab table.
                5. go_to_location(90,-400,435) # Move to the grabbing collision avoidance position for BOX_2 while holding BOX_2. 
                6. go_to_location(90, 220, 435) # Move to the release collision avoidance position for BOX_2 while holding BOX_2. 
                7. go_to_location(90, 220, 245) # Move to the exact release position for BOX_2 while holding BOX_2.
                8. release() # Release BOX_2 onto the release table.
                9. go_to_location(90, 220, 435) # Move to the release collision avoidance position for BOX_2 after BOX_2 has been 
                released.
                10. go_to_location(270,0,504) # Move the robot arm back to the home position from BOX_2's release position. """

    box3_reply= """
                1. go_to_location(270,0,504) # Start from the home position
                2. go_to_location(-90,-400,435) # Move to the collision avoidance location for BOX_3 on the grabbing table to avoid hitting other boxes
                3. go_to_location(-90,-400,245) # Move to the exact location for BOX_3 on the grabbing table
                4. grab() # Grab the BOX_3
                5. go_to_location(-90,-400,435) # Move to the collision avoidance location for BOX_3 on the grabbing table after grabbing the box
                6. go_to_location(-90,220,435) # Move to the collision avoidance location for BOX_3 on the release table to avoid hitting other 
                boxes or any other possible obstacles
                7. go_to_location(-90,220,245) # Move to the exact location for BOX_3 on the release place
                8. release() # Release the BOX_3
                9. go_to_location(-90,220,435) # Move to the collision avoidance location for BOX_3 on the release table to avoid hitting any boxes or other possible obstacles
                10. go_to_location(270,0,504) # Return to the home position at the end of the operation"""

    box4_reply = """
                1. go_to_location(270,0,504) # Start by positioning the robot arm at the home position.
                2. go_to_location(-90,-220,435) # Move to the collision avoidance point above BOX_4's start location.
                3. go_to_location(-90,-220,245) # Lower the robot arm to BOX_4's start location.
                4. grab() # Grab the BOX_4 with the robot end effector.
                5. go_to_location(-90,-220,435) # Move the BOX_4 up to the collision avoidance point.
                6. go_to_location(-90,400,435) # Move the BOX_4 across the space, above BOX_4's release point.
                7. go_to_location(-90,400,245) # Lower the BOX_4 at its release location.
                8. release() # Release BOX_4.
                9. go_to_location(-90,400,435) # Raise the robot arm to avoid collision with the BOX_4.
                10. go_to_location(270,0,504) # Return the arm to its home position after completing the task.
                """


    
    while True:
        task = sp.talk()
        if task == "exit":
            break
        elif task != "none":
            # Check which box the user referred to in their voice command
            if any(variant in task for variant in box_1_variants): 
                fetchBox(box1_reply)
            elif any(variant in task for variant in box_2_variants): 
                fetchBox(box2_reply)
            elif any(variant in task for variant in box_3_variants): 
                fetchBox(box3_reply)
            elif any(variant in task for variant in box_4_variants): 
                fetchBox(box4_reply)
            else: 
                print("Invalid box name in voice command.") 
                exit()
        time.sleep(0.3)
            
            


main()
