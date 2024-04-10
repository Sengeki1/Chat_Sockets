# Multi-Threading and Python Sockets with Pygame

This is an example of socket programming that is able to connect multiple clients to a server using python sockets. It can send messages from clients to server, and server to clients.

## Server.py

### Header Script

```py
  header = 64
```
First message length to server needs to always be of length 64 (bytes). Represents length of message about to come. We read that, get the number, then our program expects to receive the size of the message that is incoming.

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
*```addr``` Address, a tuple which arguments are the server and the port that we gonna bind to the socket
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

### Sending Message to the other Clients

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

if we receive a message  ```Client Disconnected``` we automatically exit our connection and delete that same connection from the clients buffer which stores the clients connected with the server.
```py
  connection.close()
  del clients[connection]
```
  
