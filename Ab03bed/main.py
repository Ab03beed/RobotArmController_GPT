from robotController import RobotController
from speechToText import SpeechToText
import time


def main():
    #Object of RobotController class
    r1 = RobotController("127.0.0.1", 10002, "raspiry", 242)
    #Object of SpeechToText class
    sp = SpeechToText()
    
    
  
    while True:
        
        res = r1.sendTo(r1.robotSoc,  "200,0,645")
        print("res: ", res)
        time.sleep(1)
        res = r1.sendTo(r1.robotSoc,  "300,0,645")
        print("res: ", res)
        #print(sp.talk())


main()