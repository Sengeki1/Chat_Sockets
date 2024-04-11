# Multi-Threading and Python Sockets with Pygame

This is an example of socket programming that is able to connect multiple clients to a server using python sockets. It can send messages from clients to server, and server to clients using Pygame library for user interface.

## Server.py

### Header Script

```py
  header = 64
```
First message length sent to server needs to always be of length 64 (bytes). Represents length of message about to come. We read that, get the number, then our program expects to receive the size of the message that is incoming.

```py
  SERVER = "192.10.0.100"
  SERVER = socket.gethostbyname(socket.gethostname())
```
For Mac user, type ```ifconfig``` and for Windows user, type ```ipconfig``` in the terminal and will show ```inet``` (your local IP address). Another way to get the local IP address automatically is the second script. 

### Other Scripts

```py
port = 5050
addr = (server, port)
FORMAT = 'utf-8'

clients = {}
```
* ```addr``` Address, a tuple which arguments are the server and the port that we gonna bind to the socket
* Every time we send a message we need to encode that (in UTF form).

### Indicating Specific Connection

```py
  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Type of family (IPV4 and method)
  SERVER.bind(addr) # anything that connects to the address it hits the socket
```
* What type of socket or IP address are we going to be looking for specific connections. Matches the inet which we took our IP address from running the ifconfig command.
* Then pick method which is ```SOCK_STREAM```.

### Handle Client

```py
  def handle_client(connection, address):
      (code...)
```
This function will handle the individual connection between the client and the server. In its own thread, concurrently for each client.

```py
  msg_length = connection.recv(header).decode(FORMAT) # it waits for a message to be received (blocking line of code)
```
* Called blocking line of code, which means we will not pass this line of code until we receive a message from our client.
* Decoding the encoded format from bytes into a string using UTF-8. (the ```FORMAT```)

#### Protocol

* Need a protocol for determining how many bytes we are receiving.
* We need a check to to make sure ```msg``` is not ```none```. Because when we connect, a message is sent to the server telling us that we connected, but we are trying to immediately handle the message being sent with the length of the message that is about to come...which we haven't sent yet. So, we need to make sure the ```msg``` is a valid message we can convert into an integer other wise we will run into an issue.

```py
  if msg_length:
    msg_length = int(msg_length) # get the integer size of bytes of the message
    msg = connection.recv(msg_length).decode(FORMAT)
    if msg == "Client Disconnected":
      connected = False

print(f"[{address}] {msg}")
```

### Sending Message Logic

For every client in our server excluding the connected client that sent a message, after receiving that message in the server we send that message back to all of the clients excluding the one that is connected or sended the message.

```py
for client_conn in clients:
  if client_conn != connection:
    client_conn.send(f"{msg}".encode(FORMAT))
```

for the same client that established the connection or sended a message we send a message back from the server to that client as a feedback.
```py
  connection.send("Message was Sent!".encode(FORMAT))
```

if we receive a message  ```Client Disconnected``` we automatically exit our connection and delete that same connection from the clients buffer which stores the clients connected within the server.
```py
  connection.close()
  del clients[connection]
```
  
### Start Server 

```py
  SERVER.listen() # listen for connection
  print(f"[LISTENING] Server is listening on {server}")
  (code...)
```
Listening for connections, and then passing those connections to ```handle client``` which will run in a new thread.
```py
  while True:
  connection, address = SERVER.accept() # when a new connection occours it stores the data in these two variables (blocking line of code)
  clients[connection] = address
  thread = threading.Thread(target=handle_client, args=(connection, address))
  thread.start()
```
```py
  print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
```
Print active connections, just so we can see that. Always one connection running, so do - 1 to show connections minus the one running.


## Client.py

We initialize pygame and set the height and width of the display screen then we created a font and a clock object 
```py
  pygame.init()
  screen = pygame.display.set_mode((800, 600))
  base_font = pygame.font.Font(None, 32)
  clock = pygame.time.Clock()
```

We Instantiate afterwards the class interface so we have the propreties of that specific class to draw the boxes on the screen.

```py
  client.connect(ADDR)
```
Officially connecting to the server.

### Send Message Function

If we quit the program we set the message as  ```!DISCONNECT``` which will be used to disconnect from the server and if the event type is of type ```KEYDOWN```(if we press a button) and if that button is of type ```K_BACKSPACE```(delete button) we delete the previous inserted letter. If the event key pressed is of type ```RETURN```(enter):
```py
  message = msg.encode(FORMAT)  # encode the string into bytes to be sent to the sockets

  msg_length = len(message)
  send_length = str(msg_length).encode(FORMAT)
  send_length += b' ' * (header - len(send_length))

  CLIENT.send(send_length)
  CLIENT.send(message)

  msg = ''
```
we set ```msg = ''``` so that when we send the message to the server we reset that message to an empty string.
* Encoding the message from a string into bytes so that we can actually send it through the socket.

* Then follow protocol where length of the first message we send is the length of the message that is about to come.

* ```send_length = str(msg_length).encode(FORMAT))``` Length of first message that we send, representing the length of (message) ... which is the message we actually want to send.

* ```send_length += b' ' * (HEADER - len(send_length))``` We need to make sure it is 64 bytes long. We don't know it is going to be 64 and doesn't mean it is 64. So take ```msg_length``` , and subtract from 64 to get the length, so we know how much to Pad it so that it is 64.

Lastely if the event is neither we insert text into msg variable using event.unicode which allows to type in pygame
```py
  msg += event.unicode
```

For the UI we created an if statement that doesn't allow the text to be displayed on a single line after a certain threshold for display issues. That the text doesn't surpass the input box width.
```py
if len(msg) >= threshold_value:
  msg += '\n'
  previous_threshold_value = threshold_value
  threshold_value += 30
  elif len(msg) < previous_threshold_value + 1 and threshold_value > 30:
  threshold_value -= 30
```

To display the text on the screen we first check if the msg contains any ```\n```caracter if not the string stays the same and split method returns a list which will be a list for all the phrases typed on the input box. After createing a text_surface and appending it into a new list we render every sentence of that list using blit function that allows us to specify where we want to render it which in our case its in our input box. And we always render the last newly created line, this is to explain the usage of new_surface[-1]

```py
# on input box, text logic
text_split = msg.split('\n')
new_surface = []
for sentence in text_split:
  text_surface = base_font.render(sentence, True, (0, 0, 0))
  new_surface.append(text_surface)

for line in range(len(new_surface)):
  screen.blit(new_surface[-1], (interface.inputRect.x + 10, interface.inputRect.y + 12))
  interface.inputRect.w = max(400, new_surface[-1].get_width() + 20)
```

Following that same logic now we render the received message from the server
```py
# on view box, received message logic
new_received_surface = []
for message in received_message:
  lines = message.split('\n')
  for line in lines:
    if line == "Message was Sent!":
      text_surface = base_font.render(line, True, (255, 0, 0))
    else:
      text_surface = base_font.render(line, True, (0, 0, 0))
      new_received_surface.append(text_surface)

new_received_surface = new_received_surface[-12:] ## Ensure that the list contains at most 12 elements
for line in range(len(new_received_surface)):
  screen.blit(new_received_surface[line],(interface.viewRect.x + 13, interface.viewRect.y * (line + 1.5))) # line + 15 is an offset
```

Lastely we update our program using flip method on 60 frames p/second. If exited from the while loop pygame quits.

### Receive Message

To ensure we keep track of a received message we create a separate thread that runs the function ```receive_message``` instead of running in a single thread which would cause error in our program.

```py
def receive_message(sock):
    while True:
        message = sock.recv(1024).decode()
        if not message: break
        received_message.append(message)

receive_thread = threading.Thread(target=receive_message, args=(CLIENT,))
receive_thread.start()
```
