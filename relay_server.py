import socket
import threading

# ===== Server Configuration =====
HOST = '0.0.0.0'   # Listen on all interfaces (important for EC2)
PORT = 5000
clients = []

# ===== Handle Each Client =====
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[DISCONNECTED] {addr}")
                break

            msg = data.decode().strip()
            print(f"[{addr}] {msg}")

            # Send message to all other clients
            for c in clients:
                if c != conn:
                    try:
                        c.sendall(f"{addr}: {msg}".encode())
                    except:
                        pass
    except ConnectionResetError:
        print(f"[ERROR] Connection reset by {addr}")
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        if conn in clients:
            clients.remove(conn)
        conn.close()
        print(f"[-] {addr} connection closed. Active clients: {len(clients)}")

# ===== Start the Server =====
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")
    print("[WAITING] For connections...")

    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {len(clients) + 1}")
        except KeyboardInterrupt:
            print("\n[SERVER STOPPING] Keyboard interrupt received.")
            break
        except Exception as e:
            print(f"[ERROR] Server: {e}")

    server.close()
    print("[SERVER STOPPED]")

# ===== Main Entry Point =====
if __name__ == "__main__":
    start_server()
