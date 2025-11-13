import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext
from datetime import datetime

SERVER_IP = "13.62.126.225"  # Replace with your EC2 IP
PORT = 5000

class ClientFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f0f0f0", bd=2, relief="groove", padx=5, pady=5)

        # Ask for username
        self.username = simpledialog.askstring("Username", "Enter username for this client:", parent=master)
        if not self.username:
            self.username = "Anonymous"

        # Connect to server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((SERVER_IP, PORT))
        self.client_socket.sendall(self.username.encode())

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(self, state='disabled', width=50, height=20, font=("Arial", 12))
        self.chat_area.pack(padx=5, pady=5)

        # Input box
        self.msg_entry = tk.Entry(self, width=50, font=("Arial", 12))
        self.msg_entry.pack(padx=5, pady=(0,5))
        self.msg_entry.bind("<Return>", self.send_message)

        # Start listener thread
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def listen_for_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break

                message = data.decode()
                timestamp = datetime.now().strftime("%H:%M")

                self.chat_area.config(state='normal')

                # Differentiate own messages
                if message.startswith(f"[{self.username}]"):
                    # Right-aligned and green
                    self.chat_area.tag_config("own", foreground="green", justify="right")
                    self.chat_area.insert(tk.END, f"{timestamp} {message}\n", "own")
                else:
                    # Left-aligned and blue
                    self.chat_area.tag_config("other", foreground="blue", justify="left")
                    self.chat_area.insert(tk.END, f"{timestamp} {message}\n", "other")

                self.chat_area.yview(tk.END)
                self.chat_area.config(state='disabled')
            except:
                break

    def send_message(self, event=None):
        msg = self.msg_entry.get().strip()
        if msg == "":
            return
        self.client_socket.sendall(msg.encode())
        self.msg_entry.delete(0, tk.END)

    def close(self):
        self.client_socket.close()


# Main GUI window
root = tk.Tk()
root.title("Creative Python Chat")

# Frames for two clients
client1 = ClientFrame(root)
client1.pack(side='left', padx=10, pady=10)

client2 = ClientFrame(root)
client2.pack(side='right', padx=10, pady=10)

def on_closing():
    client1.close()
    client2.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
