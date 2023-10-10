"""import socket
tcp1 = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
tcp_ip = "127.0.0.1"
port = 12345
buffer_size = 1024
msg = ("Client test.")


tcp1.connect((tcp_ip , port))
print ("Sending message: " + msg)
tcp1.send(msg.encode('utf8'))

data = tcp1.recv(buffer_size).decode('utf-8')

print ("Data reveived: " +  data)

"""

import socket

HOST ='127.0.0.1'
PORT =54321

x = 62    
y = -26
z = 580

# Set a timeout value (in seconds)
TIMEOUT = 5

def main():
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

if __name__ == "__main__":
    main()
