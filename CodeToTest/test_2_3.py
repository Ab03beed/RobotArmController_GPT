from Modules.robotController import RobotController
import keyboard
import time

#192.168.0.71
r1 = RobotController("192.168.0.20", 10002, "192.168.0.71", 12348)

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
    box1_reply = """
                1. go_to_location(270,0,504) #Robot arm goes to home position.
                2. go_to_location(90,-220,465) #Robot arm moves to collision avoidance position of BOX_1.
                3. go_to_location(90,-220,245) #Robot arm goes to the position of BOX_1 to pick it up.
                4. grab() #Robot arm grabs BOX_1.
                5. go_to_location(90,-220,465) #Robot arm moves BOX_1 to collision avoidance position before setting off to the release position.
                6. go_to_location(90,400,465) #Robot arm moves BOX_1 to collision avoidance position above the release position.
                7. go_to_location(90,400,245) #Robot arm moves BOX_1 to the release position.
                8. release() #Robot arm releases BOX_1.
                9. go_to_location(90,400,465) #Robot arm moves to collision avoidance position after releasing the BOX_1.     
                10. go_to_location(270,0,504) #Robot arm returns to home position.
                """

    box2_reply ="""
                1. go_to_location(270,0,504) #Starting from the home position.
                2. go_to_location(90,-400,465) # Move to the grabbing collision avoidance position for BOX_2.
                3. go_to_location(90,-400,245) # Move to the exact grabbing position for BOX_2.
                4. grab() # Grab BOX_2 from the grab table.
                5. go_to_location(90,-400,465) # Move to the grabbing collision avoidance position for BOX_2 while holding BOX_2. 
                6. go_to_location(90, 220, 465) # Move to the release collision avoidance position for BOX_2 while holding BOX_2. 
                7. go_to_location(90, 220, 245) # Move to the exact release position for BOX_2 while holding BOX_2.
                8. release() # Release BOX_2 onto the release table.
                9. go_to_location(90, 220, 465) # Move to the release collision avoidance position for BOX_2 after BOX_2 has been 
                released.
                10. go_to_location(270,0,504) # Move the robot arm back to the home position from BOX_2's release position. """

    box3_reply= """
                1. go_to_location(270,0,504) # Start from the home position
                2. go_to_location(-90,-400,465) # Move to the collision avoidance location for BOX_3 on the grabbing table to avoid hitting other boxes
                3. go_to_location(-90,-400,245) # Move to the exact location for BOX_3 on the grabbing table
                4. grab() # Grab the BOX_3
                5. go_to_location(-90,-400,465) # Move to the collision avoidance location for BOX_3 on the grabbing table after grabbing the box
                6. go_to_location(-90,220,465) # Move to the collision avoidance location for BOX_3 on the release table to avoid hitting other 
                boxes or any other possible obstacles
                7. go_to_location(-90,220,245) # Move to the exact location for BOX_3 on the release place
                8. release() # Release the BOX_3
                9. go_to_location(-90,220,465) # Move to the collision avoidance location for BOX_3 on the release table to avoid hitting any boxes or other possible obstacles
                10. go_to_location(270,0,504) # Return to the home position at the end of the operation"""


    box4_reply = """
                1. go_to_location(270,0,504) # Start by positioning the robot arm at the home position.
                2. go_to_location(-90,-220,465) # Move to the collision avoidance point above BOX_4's start location.
                3. go_to_location(-90,-220,245) # Lower the robot arm to BOX_4's start location.
                4. grab() # Grab the BOX_4 with the robot end effector.
                5. go_to_location(-90,-220,465) # Move the BOX_4 up to the collision avoidance point.
                6. go_to_location(-90,400,465) # Move the BOX_4 across the space, above BOX_4's release point.
                7. go_to_location(-90,400,245) # Lower the BOX_4 at its release location.
                8. release() # Release BOX_4.
                9. go_to_location(-90,400,465) # Raise the robot arm to avoid collision with the BOX_4.
                10. go_to_location(270,0,504) # Return the arm to its home position after completing the task.
                """


    
    end = False

    while not end:    
        print("\n'1' --> Box 1 \n'2' --> Box 2 \n'3' --> Box 3 \n'4' --> Box 4 \n'ESC' --> EXIT")
        command = keyboard.read_event(suppress=True).name #Wait for user to press a key
        time.sleep(0.5)

        if command == '1':
            fetchBox(box1_reply)
        elif command == '2':
            fetchBox(box2_reply)
        elif command == '3':
            fetchBox(box3_reply)
        elif command == '4':
            fetchBox(box4_reply)
        elif command == 'esc':
            print("EXITING...")
            end = True
        else:
            print("Invaild command")

        time.sleep(0.2)    



main()