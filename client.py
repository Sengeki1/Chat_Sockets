import socket
import threading

header = 64
port = 5050
FORMAT = 'utf-8'
disconnect_message = '!DISCONNECT'
server = socket.gethostbyname(socket.gethostname())
address = (server, port)

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(address)

def main():
    receive_thread = threading.Thread(target=receive_message, args=(CLIENT,))
    receive_thread.start()

    send()

def send():
    print("To Disconnect Please Type !DISCONNECT")

    connected = True
    while connected:
        msg = input()

        if msg == "!DISCONNECT":
            connected = False

        message = msg.encode(FORMAT) # encode the string into bytes to be sent to the sockets
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (header - len(send_length))

        CLIENT.send(send_length)
        CLIENT.send(message)

def receive_message(sock):
    while True:
        message = sock.recv(1024).decode()
        if not message: break
        print(f"Received: {message}")

main()