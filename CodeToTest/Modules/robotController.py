import socket

class RobotController:

    #parametrized cunstructor
    def __init__(self, robot_host, robot_port, pi_host, pi_port):

        robotConfig = (robot_host, robot_port)
        raspConfig = (pi_host, pi_port)

        self.robotSoc = self._establish_connection(robotConfig)
        self.raspSoc  = self._establish_connection(raspConfig)
        

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
            print(f"Something went wrong while operating! res --> {response}") 
            exit()
        else:
            return response






        
    

