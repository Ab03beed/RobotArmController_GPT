import socket

class RobotController:

    #parametrized cunstructor
    def __init__(self, robot_host, robot_port, pi_host, pi_port):

        self.robotConfig = (robot_host, robot_port)
        self.raspConfig = (pi_host, pi_port)

        self.robotSoc = self._establish_connection(self.robotConfig)
        self.raspSoc  = self._establish_connection(self.raspConfig)
        

    #Private function that create and check if the connection is OK.
    def _establish_connection(self, config):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.connect(config)
            return soc
        except:
            print(f"Couldn't connect to {repr(config)}!")
        

    #Public function that sends data to a target(socket)
    def sendTo(self, target, command):
        target.sendall(command.encode('utf-8'))
        response = target.recv(1024).decode()

        if "COMPLETED" not in response:
            print("Something went wrong while operating!") 
            exit()
        else:
            return response


    



    
#establish_connection ----- establish_connection()
#save_command_to_file
#send_to_robotic_arm ------ sendTo()
#send_to_raspberry_pi ----- sendTo()
#real_go_to_location   ---  sendTo()
#real_grab             ---  sendTo()
#real_release          ---  sendTo()




        
    

