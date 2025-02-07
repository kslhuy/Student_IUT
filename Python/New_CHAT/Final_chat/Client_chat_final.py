import socket
from tkinter import Tk, Text, Entry, Button, END, messagebox
import threading

# Function to handle receiving messages from the server
def receive_messages():
    while True:
        try:
            response = client_socket.recv(1024).decode()
            if not response:
                break
            chat_log.insert(END, f"Server: {response}\n")
        except ConnectionAbortedError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

# Function to send messages to the server
def send_message():
    message = input_box.get()
    if message:
        try:
            client_socket.sendall(message.encode())
            chat_log.insert(END, f"You: {message}\n")
            input_box.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

# Function to close the connection and GUI
def on_closing():
    client_socket.close()
    root.destroy()

# Initialize the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9998))

# Initialize the Tkinter GUI
root = Tk()
root.title("Chat Client")

# Chat log display
chat_log = Text(root, height=15, width=50)
chat_log.pack()

# Message input box
input_box = Entry(root, width=40)
input_box.pack()

# Send button
send_button = Button(root, text="Send", command=send_message)
send_button.pack()

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Handle window closing event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()