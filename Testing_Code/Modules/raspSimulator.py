import socket
HOST = '127.0.0.1'
PORT = 12349

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
    s.bind((HOST, PORT)) # Bind the socket to a public host and a port
    s.listen(5)  # Listen for client connections
    # Set a timeout of 10 seconds for accepting client connections
    #s.settimeout(10)
    
    print('Server listening...')
    
    try:
        # Establish connection with the client
        c, addr = s.accept()
    except socket.timeout:
        print("No client connected in 10 seconds. Exiting...")
        s.close()
        return
    
    print(f'Got connection from {addr}')

    while True:
        # Receive data from the client
        data = c.recv(1024).decode('utf-8')
        print(f'Received: {data}')
        
        if data=="GRAB":
            c.sendall(b"GRAB COMPLETED")
        elif data=="RELEASE":
            c.sendall(b"RELEASE COMPLETED")
        else:
            c.sendall(f"False command: {data}")

server()
