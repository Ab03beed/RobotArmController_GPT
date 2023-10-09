import socket 
import time
HOST = '127.0.0.1'
PORT=12345
#PORT = 10003

x=1
y=2
z=22

# Set a timeout value (in seconds)
TIMEOUT = 5
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(TIMEOUT)  # Set the timeout
    s.connect((HOST, PORT))
    #s.sendall(b'20')
    order=f"{x},{y},{z}"
    s.sendall(order.encode('utf-8'))
    try:
        data = s.recv(1024)
        print('Received', repr(data))
    except socket.timeout:
        print('No data received after', TIMEOUT, 'seconds')
        
s.close()
