from Modules.robotController import RobotController
import keyboard
import time

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
    box1_prompt = """
    1. go_to_location(410, -200, 430) #Go above BOX_1 to avoid collision
    2. go_to_location(410, -200, 300) #Going straight down to position of BOX_1
    3. grab() #Grabbing the BOX_1
    4. go_to_location(410, -200, 430) #Lift up BOX_1 above the currentPosition
    5. go_to_location(410, 200, 430)  #Move to above the release location, avoiding collision with other boxes
    6. go_to_location(410, 200, 300)  #Move straight down to the release location
    7. release() #Release the BOX_1 on release table
    8. go_to_location(410, 200, 430)  #Move up to avoid colliding with the box
    9. go_to_location(270, 0, 504) #Move back to home position after task is done
    """

    box2_prompt = ""
    box3_prompt = ""
    box4_prompt = ""


    
    end = False

    while not end:    
        print("\n'1' --> Box 1 \n'2' --> Box 2 \n'3' --> Box 3 \n'4' --> Box 4 \n'ESC' --> EXIT")
        command = keyboard.read_event(suppress=True).name #Wait for user to press a key
        time.sleep(0.5)

        if command == '1':
            fetchBox(box1_prompt)
        elif command == '2':
            fetchBox(box2_prompt)
        elif command == '3':
            fetchBox(box3_prompt)
        elif command == '4':
            fetchBox(box4_prompt)
        elif command == 'esc':
            print("EXITING...")
            end = True
        else:
            print("Invaild command")

        time.sleep(0.2)    



main()