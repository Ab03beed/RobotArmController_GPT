""""
import socket
tcp1 = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcp_ip = ""         #Any interface
port = 12345        #Arbitrary non-privileged port
buffer_size = 1024
msg = ("Connected...")
tcp1.bind ((tcp_ip , port))
tcp1.listen(1)
con, addr = tcp1.accept()
print ("TCP Connection from: ", addr)

while True:
	data = con.recv(buffer_size).decode('utf-8')
	if not data:
		break
	print ("Data received: " + data)
	print ("Sending response: "  + data)
	con.send (data.encode('utf-8'))
tcp1.close()
""""

import socket
def server():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a public host and a port
    s.bind(('127.0.0.1', 54321))
    s.listen(5)  # Listen for client connections
    
    # Set a timeout of 10 seconds for accepting client connections
    s.settimeout(10)
    
    print('Server listening...')
    
    try:
        # Establish connection with the client
        c, addr = s.accept()
    except socket.timeout:
        print("No client connected in 10 seconds. Exiting...")
        s.close()
        return
    
    print(f'Got connection from {addr}')
    
    # Receive data from the client
    data = c.recv(1024).decode('utf-8')
    print(f'Received: {data}')
    
    # Close the connection
    c.sendall(b"Received your message")
    c.close()

server()
