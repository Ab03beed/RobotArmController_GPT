import socket

def server():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to a public host and a port
    s.bind(('127.0.0.1', 12345))
    s.listen(5)  # Listen for client connections
    
    print('Server listening...')
    
    # Establish connection with the client
    c, addr = s.accept()
    print(f'Got connection from {addr}')
    
    # Receive data from the client
    data = c.recv(1024).decode('utf-8')
    print(f'Received: {data}')
    
    # Close the connection
    c.close()

server()