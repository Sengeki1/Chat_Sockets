import socket

header = 64
port = 5050
format = 'utf-8'
disconnect_message = '!DISCONNECT'
server = socket.gethostbyname(socket.gethostname())
address = (server, port)

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(address)

def send():
    print("To Disconnect Please Type !DISCONNECT")

    connected = True
    while connected:
        msg = input()

        if msg == '!DISCONNECT':
            connected = False

        message = msg.encode(format) # encode the string into bytes to be sent to the sockets
        msg_length = len(message)
        send_length = str(msg_length).encode(format)
        send_length += b' ' * (header - len(send_length))

        CLIENT.send(send_length)
        CLIENT.send(message)

send()