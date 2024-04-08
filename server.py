import socket
import threading

header = 64
port = 5050
server = socket.gethostbyname(socket.gethostname()) # gets IP address of the current host
addr = (server, port)
format = 'utf-8'

SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Type of family (IPV4 and method)
SOCKET.bind(addr) # anything that connects to the address it hits the socket

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")

    connected = True
    while connected:
        msg_length = connection.recv(header).decode(format) # it waits for a message to be received (blocking line of code)
        msg_length = int(msg_length)
        msg = connection.recv(msg_length).decode(format)

        if msg == "!DISCONNECT":
            connected = False

        print(f"[{address}] {msg}")

    connection.close()

def start():
    SOCKET.listen() # listen for connection
    print(f"[LISTENING] Server is listening on {server}")
    while True:
        connection, address = SOCKET.accept() # when a new connection occours it stores the data in these two variables (blocking line of code)
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()