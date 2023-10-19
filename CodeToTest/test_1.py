import socket
import keyboard
import time

class RobotController:
    def __init__(self, robot_host, robot_port, pi_host, pi_port):
        self.robotConfig = (robot_host, robot_port)
        self.raspConfig = (pi_host, pi_port)

        self.robotSoc = self._establish_connection(self.robotConfig)
        self.raspSoc  = self._establish_connection(self.raspConfig)

    def _establish_connection(self, config):
        print(f"Attempting to connect to {repr(config)}...")
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.connect(config)
            print(f"Connected to {repr(config)}!")
            return soc
        except:
            print(f"Couldn't connect to {repr(config)}!")
            return None

    def sendTo(self, target, command):
        print(f"Sending command: {command}...")
        target.sendall(command.encode('utf-8'))
        response = target.recv(1024).decode()
        print(f"Received response: {response}")
        
        if "COMPLETED" not in response:
            print("Something went wrong while operating!") 
        else:
            return response

class GPT_API:
    def __init__(self):
        pass

    def move_box(self, box_number):
        print(f"Preparing instructions for BOX_{box_number}...")
                # Directly return the steps to move the boxes based on the box_number
        if box_number == 1:
            return [
                ("go_to_location", (402, -203, 100), "Move to BOX_1's location"),
                ("grab", None, "Grab BOX_1"),
                ("go_to_location", (400, 100, 100), "Move to release position"),
                ("release", None, "Release BOX_1"),
                ("go_to_location", (270, 0, 504), "Return to home position")
            ]
        elif box_number == 2:
            return [
                ("go_to_location", (300, -203, 100), "Move to BOX_2's location"),
                ("grab", None, "Grab BOX_2"),
                ("go_to_location", (400, 100, 100), "Move to release position"),
                ("release", None, "Release BOX_2"),
                ("go_to_location", (270, 0, 504), "Return to home position")
            ]
        elif box_number == 3:
            return [
                ("go_to_location", (203, -203, 100), "Move to BOX_3's location"),
                ("grab", None, "Grab BOX_3"),
                ("go_to_location", (400, 100, 100), "Move to release position"),
                ("release", None, "Release BOX_3"),
                ("go_to_location", (270, 0, 504), "Return to home position")
            ]
        else:
            return []

def main():
    print("Initializing RobotController...")
    r1 = RobotController("127.0.0.1", 10002, "127.0.0.1", 12345)

    print("Initializing GPT_API...")
    gpt = GPT_API()

    print("Ready for input...")
    print("Press 1, 2, or 3 to move the respective box.")
    print("Press 'esc' to exit.\n")

    end = False
    while not end:
        task = keyboard.read_event(suppress=True).name
        print(f"Key pressed: {task}")

        if task == "esc":
            break
        elif task in ["1", "2", "3"]:
            box_number = int(task)
            actions = gpt.move_box(box_number)
            for action, params, explanation in actions:
                print(explanation)
                if action == "go_to_location":
                    coords = params
                    command = f"{coords[0]},{coords[1]},{coords[2]}"
                    res = r1.sendTo(r1.robotSoc, command)
                elif action == "grab":
                    res = r1.sendTo(r1.raspSoc, "GRAB")
                elif action == "release":
                    res = r1.sendTo(r1.raspSoc, "RELEASE")
                print(res)
        else:
            print(f"Unexpected key pressed: {task}")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
