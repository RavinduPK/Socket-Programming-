import socket
import threading

SERVER_IP = "13.62.126.225"  # <-- Replace with your EC2 public IP
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(f"\nReceived: {msg}")
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
print("[+] Connected to server")

threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

while True:
    msg = input("You: ")
    if msg.lower() == "exit":
        break
    client.sendall(msg.encode())

client.close()
print("[-] Disconnected")
