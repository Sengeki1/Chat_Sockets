import socket
import pygame
import threading
from interface import Interface

header = 64
port = 5050
FORMAT = 'utf-8'

pygame.init()
screen = pygame.display.set_mode((800, 600))
base_font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()

interface = Interface(screen)

server = socket.gethostbyname(socket.gethostname())
address = (server, port)

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
CLIENT.connect(address)

def send():
    connected = True
    threshold_value = 30
    msg = ''

    print("To Disconnect Please Type !DISCONNECT")

    while connected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                msg = "!DISCONNECT"
                connected = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    msg = msg[:-1]
                elif event.key == pygame.K_RETURN:
                    message = msg.encode(FORMAT)  # encode the string into bytes to be sent to the sockets

                    msg_length = len(message)
                    send_length = str(msg_length).encode(FORMAT)
                    send_length += b' ' * (header - len(send_length))

                    CLIENT.send(send_length)
                    CLIENT.send(message)

                    msg = ''
                else:
                    msg += event.unicode

                    if len(msg) >= threshold_value:
                        msg += '\n'
                        threshold_value += 30

        if msg == "!DISCONNECT":
            message = "Client Disconnected".encode(FORMAT)

            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (header - len(send_length))

            CLIENT.send(send_length)
            CLIENT.send(message)

            msg = ''

        screen.fill((0, 0, 0))
        interface.draw()

        text_split = msg.split('\n')
        new_surface = []
        for sentence in text_split:
            text_surface = base_font.render(sentence, True, (0, 0, 0))
            new_surface.append(text_surface)

        for line in range(len(new_surface)):
            screen.blit(new_surface[-1], (interface.inputRect.x + 10, interface.inputRect.y + 12))
            interface.inputRect.w = max(400, new_surface[-1].get_width() + 20)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

def receive_message(sock):
    while True:
        message = sock.recv(1024).decode()
        if not message: break
        print(f"Received: {message}")

receive_thread = threading.Thread(target=receive_message, args=(CLIENT,))
receive_thread.start()

send()