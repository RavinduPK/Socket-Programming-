import socket
import threading

# Ask the user to choose a nickname
input_nickname = input("Choose your nickname: ")

# Create a TCP/IP socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client to the server (host: 127.0.0.1, port: 8081)
client.connect(('127.0.0.1', 8081))

# Function to continuously receive messages from the server
def receive():
    while True:
        try:
            # Receive message from the server (max size: 1024 bytes)
            message = client.recv(1024).decode('ascii')

            # If the server asks for a nickname, send it
            if message == "NICK":
                client.send(input_nickname.encode('ascii'))
            else:
                # Otherwise, print the message to the console
                print(message)

        except:
            # If there’s an error (e.g., server closed or lost connection)
            print("An error occurred!")
            client.close()
            break

# Function to continuously send messages typed by the user
def write():
    while True:
        # Get user input and prepend nickname
        message = f'{input_nickname}: {input("")}'
        # Send the message to the server
        client.send(message.encode('ascii'))

# Create and start a thread for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Create and start a thread for sending messages
write_thread = threading.Thread(target=write)
write_thread.start()
