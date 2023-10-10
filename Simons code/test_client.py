import socket
HOST = '127.0.0.1'
PORT = 12345

x = 62    
y = -26
z = 580

# Set a timeout value (in seconds)
TIMEOUT = 5

def client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("Attempting to connect to server...")
            s.settimeout(TIMEOUT)  # Set the timeout
            s.connect((HOST, PORT))
            print("Connected to server.")

            message = f"{x},{y},{z}".encode('utf-8')
            print(f"Sending message: {message.decode('utf-8')}")
            s.sendall(message)

            try:
                data = s.recv(1024)
                print('Received from server:', repr(data))
            except socket.timeout:
                print(f'No data received after {TIMEOUT} seconds')
            except Exception as e:
                print(f"Error while receiving data: {e}")

    except ConnectionRefusedError:
        print("Connection refused. Is the server running and listening on the correct IP and port?")
    except socket.timeout:
        print(f"Connection attempt timed out after {TIMEOUT} seconds.")
    except Exception as e:
        print(f"Error: {e}")


client()
