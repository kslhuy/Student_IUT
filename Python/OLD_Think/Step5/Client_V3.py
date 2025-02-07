import cv2
import socket
import struct
import pickle
import threading
from tkinter import Tk, Text, Entry, Button, Scrollbar, END, Frame, Label
from PIL import Image, ImageTk


def receive_video_stream(video_socket, video_label, stop_event):
    """
    Receive and display video stream.
    Args:
        video_socket (socket.socket): The socket object used to receive video data.
        video_label (tkinter.Label): The Tkinter label widget where the video frames will be displayed.
        stop_event (threading.Event): An event object used to signal when to stop receiving the video stream.
    Raises:
        Exception: If an error occurs while receiving or processing the video stream.
    """
    """Receive and display video stream."""
    data = b""
    payload_size = struct.calcsize("Q")
    try:
        while not stop_event.is_set():
            while len(data) < payload_size:
                packet = video_socket.recv(4 * 1024)
                if not packet:
                    return
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += video_socket.recv(4 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Deserialize frame
            frame = pickle.loads(frame_data)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert frame to Tkinter-compatible image
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
    except Exception as e:
        print(f"Video receiving error: {e}")


def handle_chat(chat_socket, chat_log, stop_event):
    """
    Handles receiving chat messages from the server and updating the chat log.

    Args:
        chat_socket (socket.socket): The socket object used to receive messages from the server.
        chat_log (tkinter.Text): The text widget where chat messages are displayed.
        stop_event (threading.Event): An event used to signal when to stop receiving messages.

    Raises:
        Exception: If an error occurs while receiving messages.

    This function runs in a loop, continuously receiving messages from the server
    until the stop_event is set. Received messages are decoded and inserted into
    the chat_log widget. If an error occurs, it is printed to the console, and the
    chat socket is closed in the finally block.
    """
    """Receive chat messages from the server."""
    try:
        while not stop_event.is_set():
            message = chat_socket.recv(1024).decode()
            if not message:
                break
            chat_log.insert(END, f"Server: {message}\n")
            chat_log.see(END)
    except Exception as e:
        print(f"Chat error: {e}")
    finally:
        chat_socket.close()

"""Send message to the server."""
def send_message(chat_socket, chat_log, input_box):
    """
    Send a message to the server and update the chat log.

    Args:
        chat_socket (socket.socket): The socket object used to send the message to the server.
        chat_log (tkinter.Text): The chat log widget where the message will be displayed.
        input_box (tkinter.Entry): The input box widget where the user types the message.

    Returns:
        None
    """
    message = input_box.get()
    input_box.delete(0, END)
    if message.strip():
        chat_log.insert(END, f"You: {message}\n")
        chat_log.see(END)
        chat_socket.sendall(message.encode())


def on_close(root, video_socket, chat_socket, stop_event):
    """Handle application close event."""
    stop_event.set()  # Signal threads to stop
    video_socket.close()
    chat_socket.close()
    root.destroy()


def start_client(server_ip="127.0.0.1", video_port=9999, chat_port=9998):
    """
    Starts the client application that connects to a video and chat server, and initializes the GUI.
    Args:
        server_ip (str): The IP address of the server to connect to. Defaults to "127.0.0.1".
        video_port (int): The port number for the video server. Defaults to 9999.
        chat_port (int): The port number for the chat server. Defaults to 9998.
    Creates:
        - Two sockets for video and chat communication.
        - A GUI window with a video display, chat log, input box, and send button.
        - Threads for handling video streaming and chat communication.
    Note:
        The function sets up a stop event to handle the closing of the application gracefully.
    """
    # Create sockets
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    video_socket.connect((server_ip, video_port))
    print(f"Connected to video server on {server_ip}:{video_port}")
    chat_socket.connect((server_ip, chat_port))
    print(f"Connected to chat server on {server_ip}:{chat_port}")

    # Create GUI
    root = Tk()
    root.title("Client Chat & Video")

    frame = Frame(root)
    frame.pack()

    # Video label
    video_label = Label(frame)
    video_label.pack()

    # Chat log
    chat_log = Text(frame, height=15, width=50)
    chat_log.pack(side="left")
    chat_log.config(state="normal")

    # Scrollbar for chat log
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    chat_log.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=chat_log.yview)

    # Input box for chat
    input_box = Entry(root, width=40)
    input_box.pack()

    # Send button
    send_button = Button(root, text="Send", command=lambda: send_message(chat_socket, chat_log, input_box))
    send_button.pack()

    # Stop event for threads
    stop_event = threading.Event()

    # Handle close event
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, video_socket, chat_socket, stop_event))

    # Start threads for video streaming and chat
    video_thread = threading.Thread(target=receive_video_stream, args=(video_socket, video_label, stop_event), daemon=True)
    chat_thread = threading.Thread(target=handle_chat, args=(chat_socket, chat_log, stop_event), daemon=True)

    video_thread.start()
    chat_thread.start()

    root.mainloop()


if __name__ == "__main__":
    start_client()
