import socket 
HOST = '127.0.0.1'
PORT = 10002

import socket
# Set a timeout value (in seconds)
TIMEOUT = 5
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(TIMEOUT)  # Set the timeout
    s.connect((HOST, PORT))
    s.sendall(b'20')
    try:
        data = s.recv(1024)
        print('Received', repr(data))
    except socket.timeout:
        print('No data received after', TIMEOUT, 'seconds')




""" """

"""
i = 0

while True:
    HOST = "192.168.0."
    PORT = 10001
    newHost = HOST + str(i)
    i = i + 1

    try:
        print(newHost)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((newHost,PORT))
            s.sendall(b'20')
            data = s.recv(1024)
        print('Received', data) #repr returns printable data.

        if data == '22':
            print("inside if\n")
            import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((newHost,PORT))
            s.sendall(b'20')
            data = s.recv(1024)
        print('Received', repr(data))
    except:
        print("An exception occurred")

    if i == 255:
        break


print("DONE")
"""


"""

#Define the IP address and port number of the RT ToolBox3 simulation
IP_ADDRESS = '192.168.0.6'
PORT_NUMBER = 10006

#Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to the RT ToolBox3 simulation
client_socket.connect((IP_ADDRESS, PORT_NUMBER))

#Send data to the RT ToolBox3 simulation
client_socket.sendall(b'20')

#Receive data from the RT ToolBox3 simulation
response = client_socket.recv(1024)
print(repr(response))

#Close the socket connection
client_socket.close()
"""



"""
# Sender Socket Configuration
host = '192.168.0.20'  # Replace with the receiver's IP address
port = 10001  # Choose an appropriate port number

# Data to be sent
data_to_send = "Hello, Melfa Basic V!"

# Create a socket object
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the receiver
sender_socket.connect((host, port))

# Send data
sender_socket.send(data_to_send.encode())

# Close the socket
sender_socket.close()
"""