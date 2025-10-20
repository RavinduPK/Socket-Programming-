import threading
import socket

# Define server host and port
host = '127.0.0.1'  # Localhost (only accessible on this computer)
port = 8081         # Port number for the server to listen on

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow the server to reuse the address (avoids "address already in use" error)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the host and port
server.bind((host, port))

# Start listening for incoming connections (max queue of 5 clients)
server.listen(5)

# Lists to keep track of connected clients and their nicknames
clients = []
nicknames = []

# Function to broadcast messages to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle messages from a specific client
def handle(client):
    while True:
        try:
            # Receive message from the client
            message = client.recv(1024)
            # Broadcast the message to all clients
            broadcast(message)
        except:
            # If an error occurs (like client disconnects), remove them
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            # Notify others that the client left
            broadcast(f'{nickname} left the chat !'.encode('ascii'))
            # Remove nickname from list
            nicknames.remove(nickname)
            break

# Function to continuously accept and manage new client connections
def receive():
    while True:
        # Accept a new client connection
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        # Ask the client for a nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # Save client and nickname
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')

        # Announce that the new client joined the chat
        broadcast(f'{nickname} joined the chat !'.encode('ascii'))
        # Send confirmation to the new client
        client.send('Connected to the server !'.encode('ascii'))

        # Start a new thread to handle messages from this client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start the server
print('Server is listening ...')
receive()
