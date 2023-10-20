from Modules.robotController import RobotController
import keyboard
import time
    #192.168.0.71
r1 = RobotController("127.0.0.1", 10002, "127.0.0.1", 12345)
end = False

def fetchBox(Pos):
    print("\n'B' --> mov to BOX pos \n'N' --> mov to ABOVE BOX pos \n'-----------------\n'G' --> GRAB \n'R' --> RELEASE \n----------------\n'D' --> mov to RELEASE pos \n'f' --> mov to ABOVE BOX pos \n'H' --> HOME POS \n'ESC' --> EXIT")
    global end
    while not end:
        res = ""
        command = keyboard.read_event(suppress=True).name #Wait for user to press a key
        if command == 'b':
            res = r1.sendTo(r1.robotSoc, Pos[0])
        elif command =='n':
            res = r1.sendTo(r1.robotSoc, Pos[1])
        elif command == 'g':
            res="grab completed"
            #res = r1.sendTo(r1.raspSoc, f"GRAB")
        elif command == 'r':
            res="release completed"
            #res = r1.sendTo(r1.raspSoc, f"RELEASE")
        elif command == 'd':
            res = r1.sendTo(r1.robotSoc, Pos[2])
        elif command == 'f':
            res = r1.sendTo(r1.robotSoc, Pos[3])
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
    #box pos , above box pos, release pos, above release pos
    box1 = ["90,-220,245", "90,-220,445", "90,400,245",  "90, 400, 435"]
    box2 = ["90,-400,245", "90,-400,435", "90, 220, 245", "90, 220, 435"]
    box3 = ["-90,-400,245", "-90,-400,435", "-90,220,245", "-90, 220, 435"]
    box4 = ["-90,-220,245", "-90,-220,435", "-90,400,245",  "-90, 400, 435"]




    print("\n'1' --> Box 1 \n'2' --> Box 2 \n'3' --> Box 3 \n'4' --> Box 4 \n'ESC' --> EXIT")
    box = keyboard.read_event(suppress=True) #Wait for user to press a key
    time.sleep(0.5)
    global end

    while not end:

        if box.name == '1':
            print(f"\nYou have chosen BOX_{box.name}")
            fetchBox(box1)
        elif box.name == '2':
            print(f"\nYou have chosen BOX_{box.name}")
            fetchBox(box2)
        elif box.name == '3':
            print(f"\nYou have chosen BOX_{box.name}")
            fetchBox(box3)
        elif box.name == '4':
            print(f"\nYou have chosen BOX_{box.name}")
            fetchBox(box4)
        elif box.name == 'esc':
            print("EXITING...")
            end = True
        else:
            print("Invaild command")
        
        time.sleep(0.2)  



main()