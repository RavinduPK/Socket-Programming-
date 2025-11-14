import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, Canvas, Frame

SERVER_IP = "13.62.126.225"  # Replace with your EC2 IP
PORT = 5000

# Connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# ---------------- THEME SETTINGS ----------------
BG_COLOR = "#1e1e1e"
HEADER_COLOR = "#272727"
TEXT_COLOR = "#ffffff"
INPUT_COLOR = "#333333"
MY_MSG_COLOR = "#4e9eff"
OTHER_MSG_COLOR = "#3b3b3b"
FONT = ("Segoe UI", 11)

# ---------------- GUI WINDOW ----------------
root = tk.Tk()
root.title("Chat Client")
root.geometry("500x600")
root.config(bg=BG_COLOR)

# ---------------- HEADER BAR ----------------
header = tk.Frame(root, bg=HEADER_COLOR, height=60)
header.pack(fill=tk.X)

title_label = tk.Label(header, text="💬 Python Chat Client", font=("Segoe UI", 16, "bold"),
                       bg=HEADER_COLOR, fg="white")
title_label.pack(pady=10)

# ---------------- CHAT AREA ----------------
chat_frame = scrolledtext.ScrolledText(root, state='disabled', bg=BG_COLOR,
                                       fg=TEXT_COLOR, font=FONT, wrap=tk.WORD)
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ---------------- INPUT AREA ----------------
bottom_frame = tk.Frame(root, bg=BG_COLOR)
bottom_frame.pack(fill=tk.X, pady=10)

msg_entry = tk.Entry(bottom_frame, bg=INPUT_COLOR, fg="white", font=FONT,
                     relief=tk.FLAT, width=35)
msg_entry.grid(row=0, column=0, padx=10)

send_btn = tk.Button(bottom_frame, text="Send", bg="#4e9eff", fg="white",
                     font=("Segoe UI", 11, "bold"), relief=tk.FLAT, width=8)
send_btn.grid(row=0, column=1, padx=5)

# ---------------- ASK USERNAME ----------------
username = simpledialog.askstring("Username", "Enter your username:", parent=root)
client_socket.sendall(username.encode())

# ---------------- DISPLAY FUNCTION ----------------
def write_message(sender, message, my_msg=False):
    chat_frame.config(state='normal')

    if my_msg:
        chat_frame.insert(tk.END, f"{sender} (You): ", "me")
        chat_frame.insert(tk.END, message + "\n\n", "my_msg")
    else:
        chat_frame.insert(tk.END, f"{sender}: ", "other")
        chat_frame.insert(tk.END, message + "\n\n", "other_msg")

    chat_frame.tag_config("me", foreground="#4e9eff", font=("Segoe UI", 10, "bold"))
    chat_frame.tag_config("my_msg", foreground="white")
    chat_frame.tag_config("other", foreground="#cccbcb", font=("Segoe UI", 10, "bold"))
    chat_frame.tag_config("other_msg", foreground="white")

    chat_frame.yview(tk.END)
    chat_frame.config(state='disabled')

# ---------------- LISTEN THREAD ----------------
def listen_for_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # SERVER MESSAGE FORMAT:  username: message
            if ": " in data:
                sender, msg = data.split(": ", 1)
                write_message(sender, msg, my_msg=False)
            else:
                write_message("", data, my_msg=False)

        except:
            break

threading.Thread(target=listen_for_messages, daemon=True).start()

# ---------------- SEND MESSAGE ----------------
def send_message(event=None):
    msg = msg_entry.get().strip()
    if msg == "":
        return

    client_socket.sendall(msg.encode())
    write_message(username, msg, my_msg=True)

    msg_entry.delete(0, tk.END)

send_btn.config(command=send_message)
msg_entry.bind("<Return>", send_message)

# ---------------- WINDOW CLOSE ----------------
def on_closing():
    try:
        client_socket.close()
    except:
        pass
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
