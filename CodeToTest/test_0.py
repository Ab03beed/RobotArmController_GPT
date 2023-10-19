from Modules.robotController import RobotController
import keyboard
import time


#       130 above           box 1               130 above       130 above delv        above     home pos
#box1 = [(410, -200, 430), (410, -200, 300), (410, 200, 430), (410, 200, 300), (410, 200, 430), (270, 0, 504)] 

#print(box1[0][2])




def main():
    gpt_response = """
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

    r1 = RobotController("127.0.0.1", 10002, "127.0.0.1", 12345)

    print("\n'1' --> Box 1 \n'2' --> Box 2 \n'3' --> Box 3 \n'4' --> Box 4 \n'ESC' --> EXIT")
    box = keyboard.read_event(suppress=True) #Wait for user to press a key
    time.sleep(0.1)
    end = False

    while not end:

        if box.name == '1':
            print("\n'B' --> MOV TO BOX POS \n'G' --> GRAB \n'R' --> RELEASE \n'D' --> DESTINATION POS  \n'H' --> HOME POS \n'ESC' --> EXIT")
            while not end:
                res = ""
                command = keyboard.read_event(suppress=True) #Wait for user to press a key
                if command.name == 'b':
                    res = r1.sendTo(r1.robotSoc, f"410, -200, 300")
                elif command.name == 'g':
                    res = r1.sendTo(r1.robotSoc, f"410, -200, 300")
                elif command.name == 'r':
                    res = r1.sendTo(r1.robotSoc, f"410, -200, 300")
                elif command.name == 'd':
                    res = r1.sendTo(r1.robotSoc, f"410, -200, 300")
                elif command.name == 'h':
                    res = r1.sendTo(r1.robotSoc, f"410, -200, 300")
                elif box.name == 'esc':
                    print("EXITING...")
                    end = True
                else:
                    print("Invaild command")

                print(res)
                time.sleep(0.2)

            
        elif box.name == '2':
            print("2")
        elif box.name == '3':
            print("3")
        elif box.name == '4':
            print("4")
        elif box.name == 'esc':
            print("EXITING...")
            end = True
        else:
            print("Invaild command")

        time.sleep(0.2)    



main()