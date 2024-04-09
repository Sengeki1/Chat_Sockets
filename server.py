import socket
import threading

header = 64
port = 5050
server = socket.gethostbyname(socket.gethostname()) # gets IP address of the current host
addr = (server, port)
FORMAT = 'utf-8'

clients = {}

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Type of family (IPV4 and method)
SERVER.bind(addr) # anything that connects to the address it hits the socket

def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")

    connected = True
    while connected:
        msg_length = connection.recv(header).decode(FORMAT) # it waits for a message to be received (blocking line of code)

        if msg_length:
            msg_length = int(msg_length) # get the integer size of bytes of the message
            msg = connection.recv(msg_length).decode(FORMAT)

            if msg == "!DISCONNECT":
                connected = False
            else:
                print(f"[{address}] {msg}")

                for client_conn in clients:
                    if client_conn != connection:
                        client_conn.send(f"{msg}".encode(FORMAT))

    connection.close()
    del clients[connection]

def start():
    SERVER.listen() # listen for connection
    print(f"[LISTENING] Server is listening on {server}")
    while True:
        connection, address = SERVER.accept() # when a new connection occours it stores the data in these two variables (blocking line of code)
        clients[connection] = address
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()