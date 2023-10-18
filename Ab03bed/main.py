from robotController import RobotController
from speechToText import SpeechToText
from GPT_API import GPT_API
import keyboard
import time


def main():
    #Object of RobotController class
    r1 = RobotController("127.0.0.1", 10002, "127.0.0.1", 12345)
    #Object of SpeechToText class
    sp = SpeechToText()
    #Object of GPT_API class
    gpt = GPT_API()
  
    while True:
        task = sp.talk()
        if task == "exit":
            break
        elif task != "none":
            gptResponse = gpt.ask(task)

            print(gptResponse)

            print("\nPress ENTER to preform the action or ESC to exit: ")
            print("Press anything eles for new task\n")
            key = keyboard.read_hotkey() #Wait for user to press a key

            if(key == "enter"):
                for line in gptResponse.split("\n"):
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
            elif(key == "esc"):
                break
                
           
                    

            
        
        
        
        
    


main()