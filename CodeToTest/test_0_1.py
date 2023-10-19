from Modules.robotController import RobotController
import keyboard
import time

r1 = RobotController("127.0.0.1", 10002, "127.0.0.1", 12345)
end = False

def fetchBox(boxPos, boxDestPos):
    print("\n'B' --> MOV TO BOX POS \n'G' --> GRAB \n'R' --> RELEASE \n'D' --> DESTINATION POS  \n'H' --> HOME POS \n'ESC' --> EXIT")
    global end
    while not end:
        res = ""
        command = keyboard.read_event(suppress=True).name #Wait for user to press a key
        if command == 'b':
            res = r1.sendTo(r1.robotSoc, boxPos)
        elif command == 'g':
            res = r1.sendTo(r1.raspSoc, f"GRAB")
        elif command == 'r':
            res = r1.sendTo(r1.raspSoc, f"RELEASE")
        elif command == 'd':
            res = r1.sendTo(r1.robotSoc, boxDestPos)
        elif command == 'h':
            res = r1.sendTo(r1.robotSoc, f"270, 0, 504")
        elif command == 'esc':
            print("EXITING...")
            end = True
        else:
            print("Invaild command")

        print(res)
        time.sleep(0.2)



def main():

    box1_Pos = f"410, -200, 300"
    box1_DestPos = f"410, 200, 300"

    box2_Pos = f"410, -200, 300"
    box2_DestPos = f"410, 200, 300"
    
    box3_Pos = f"410, -200, 300"
    box3_DestPos = f"410, 200, 300"

    box4_Pos = f"410, -200, 300"
    box4_DestPos = f"410, 200, 300"
    

    print("\n'1' --> Box 1 \n'2' --> Box 2 \n'3' --> Box 3 \n'4' --> Box 4 \n'ESC' --> EXIT")
    box = keyboard.read_event(suppress=True) #Wait for user to press a key
    time.sleep(0.5)
    global end

    while not end:

        if box.name == '1':
            fetchBox(box1_Pos, box1_DestPos)
        elif box.name == '2':
            fetchBox(box2_Pos, box2_DestPos)
        elif box.name == '3':
            fetchBox(box3_Pos, box3_DestPos)
        elif box.name == '4':
            fetchBox(box4_Pos, box4_DestPos)
        elif box.name == 'esc':
            print("EXITING...")
            end = True
        else:
            print("Invaild command")

        time.sleep(0.2)    



main()