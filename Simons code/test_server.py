import socket

HOST = '127.0.0.1'
PORT = 12345

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    s.bind((HOST, PORT))  # Bind the socket to a public host and a port
    s.listen(5)  # Listen for client connections

    print('Server listening...')

    while True:  # This loop will keep the server running and accepting new clients
        try:
            # Establish connection with the client
            c, addr = s.accept()
            print(f'Got connection from {addr}')

            while True:  # This loop will handle the client until it disconnects
                # Receive data from the client
                data = c.recv(1024).decode('utf-8')
                if not data:  # If data is empty, client has disconnected
                    break
                print(f'Received: {data}')

                if data == "GRAB":
                    c.sendall(b"GRAB COMPLETE")
                elif data == "RELEASE":
                    c.sendall(b"RELEASE COMPLETE")
                else:
                    c.sendall(b"not correct message")

            c.close()  # Close the client socket
            print(f'Connection from {addr} closed')
            print('Server listening...')
        except Exception as e:
            print(f"Error: {e}")
            s.close()
            return

server()