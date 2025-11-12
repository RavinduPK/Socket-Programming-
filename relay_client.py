import socket
import threading

# ===== Configuration =====
SERVER_IP = "13.62.126.225"  # Replace with your EC2 public IPv4
PORT = 5000                  # Make sure this matches your server

# ===== Function to Receive Messages =====
def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if not msg:
                print("\n[!] Server closed the connection.")
                break
            print(f"\n{msg}")  # Already includes username from server
        except ConnectionResetError:
            print("\n[!] Connection lost. Server may have stopped.")
            break
        except Exception as e:
            print(f"\n[!] Error receiving message: {e}")
            break

# ===== Main Client Code =====
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[*] Connecting to {SERVER_IP}:{PORT} ...")
    client.settimeout(10)  # Optional: 10s timeout
    client.connect((SERVER_IP, PORT))
    client.settimeout(None)
    print("[+] Connected to server successfully!\n")
except socket.timeout:
    print("[X] Connection timed out. Check your EC2 IP, port, and security group.")
    exit()
except ConnectionRefusedError:
    print("[X] Connection refused. Make sure the server is running.")
    exit()
except Exception as e:
    print(f"[X] Failed to connect: {e}")
    exit()

# ===== Enter Username Once =====
username = ""
while not username:
    username = input("Enter your username: ").strip()

# Start thread to listen for server messages
threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

# ===== Send Messages Loop =====
try:
    while True:
        msg = input()  # No "You:" prompt to avoid duplication
        if msg.strip().lower() == "exit":
            client.sendall(f"{username} has left the chat.".encode())
            break
        if msg.strip():
            full_msg = f"{username}: {msg}"
            client.sendall(full_msg.encode())
except KeyboardInterrupt:
    client.sendall(f"{username} has disconnected.".encode())

client.close()
print("[-] Client closed.")
