import socket
RASPBERRY_PI_IP = "YOUR_RASPBERRY_PI_IP"
RASPBERRY_PI_PORT = YOUR_RASPBERRY_PI_PORT

def send_to_raspberry_pi(command):
    raspberry_pi_socket.sendall(command.encode())
    response = raspberry_pi_socket.recv(1024).decode()
    return response

def establish_connection(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, int(port)))
    return s
raspberry_pi_socket = establish_connection(RASPBERRY_PI_IP, RASPBERRY_PI_PORT)

def real_grab():
    response = send_to_raspberry_pi("GRAB")
    if "COMPLETED" not in response:
        print(f"Error grabbing: {response}")
        exit()
    print(response)

def real_release():
    response = send_to_raspberry_pi("RELEASE")
    if "COMPLETED" not in response:
        print(f"Error releasing: {response}")
        exit()
    print(response)

value = input("Enter the value 1 to grab and 2 to release: ")
if value == 1:
    real_grab()
elif value == 2:
    real_release()
else:
    print("Invalid value")