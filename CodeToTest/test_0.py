from Modules.robotController import RobotController
import keyboard
import time


def main():

    r1 = RobotController("127.0.0.1", 10002, "127.0.0.1", 12345)

    print("\n'1' --> Box 1 \n'2' --> Box 2 \n'3' --> Box 3 \n'4' --> Box 4 \n'ESC' --> EXIT")
    box = keyboard.read_event(suppress=True) #Wait for user to press a key
    time.sleep(0.5)
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
                    res = r1.sendTo(r1.raspSoc, f"GRAB")
                elif command.name == 'r':
                    res = r1.sendTo(r1.raspSoc, f"RELEASE")
                elif command.name == 'd':
                    res = r1.sendTo(r1.robotSoc, f"410, 200, 300")
                elif command.name == 'h':
                    res = r1.sendTo(r1.robotSoc, f"270, 0, 504")
                elif command.name == 'esc':
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