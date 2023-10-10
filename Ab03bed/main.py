from robotController import RobotController
from speechToText import SpeechToText
from GPT_API import GPT_API
import time
import os


def main():
    #Object of RobotController class
    #r1 = RobotController("127.0.0.1", 10002, "raspiry", 242)
    #Object of SpeechToText class
    sp = SpeechToText()
    gpt = GPT_API()
    

    
  
    while True:
        
        res = r1.sendTo(r1.robotSoc,  "200,0,645")
        print("res: ", res)
        time.sleep(1)
        res = r1.sendTo(r1.robotSoc,  "300,0,645")
        print("res: ", res)
        
    task = sp.talk()
    print(task)

    print(gpt.ask(task))


main()