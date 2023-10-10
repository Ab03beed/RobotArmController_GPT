import socket 
import time
HOST = '127.0.0.1'
PORT=10002
#PORT = 10003

x=62    
y=-26
z=580

# Set a timeout value (in seconds)
TIMEOUT = 5
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(TIMEOUT)  # Set the timeout
    s.connect((HOST, PORT))
    #s.sendall(b'20')
    message = f"{x},{y},{z}".encode('utf-8')
    s.sendall(message)
    try:
        data = s.recv(1024)
        print('Received', repr(data))
    except socket.timeout:
        print('No data received after', TIMEOUT, 'seconds')
        

