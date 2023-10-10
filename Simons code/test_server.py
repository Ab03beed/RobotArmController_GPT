import socket
def server():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the socket to a public host and a port
    s.bind(('127.0.0.1', 12345))
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
