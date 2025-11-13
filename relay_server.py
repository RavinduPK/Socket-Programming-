import socket
import threading

HOST = "0.0.0.0"
PORT = 5000

clients = {}  # conn: username mapping

def handle_client(conn, addr):
    try:
        # Receive username
        username = conn.recv(1024).decode().strip()
        clients[conn] = username
        print(f"[+] {username} connected from {addr}")  # server log

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"[{username}]: {data.decode()}"
            # Broadcast to all clients except sender
            for c in clients:
                if c != conn:
                    c.sendall(message.encode())

    except ConnectionResetError:
        pass
    finally:
        print(f"[-] {clients.get(conn, addr)} disconnected")
        if conn in clients:
            del clients[conn]
        conn.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Relay server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
