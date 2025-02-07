import cv2
import socket
import struct
import pickle
import threading
from tkinter import Tk, Text, Entry, Button, Scrollbar, END, Frame, Label
from PIL import Image, ImageTk

"""Function to handle video streaming."""
def handle_video_stream(video_conn, cap, video_label):
    """
    Function to handle video streaming.
    Args:
        video_conn (socket.socket): The socket connection used to send video frames.
        cap (cv2.VideoCapture): The OpenCV video capture object.
        video_label (tkinter.Label): The label widget in the GUI to display the video frames.
    The function reads frames from the video capture object, serializes them, and sends them over the socket connection.
    It also updates the provided label widget to display the video frames locally in the GUI.
    Raises:
        Exception: If an error occurs during video streaming.
    Note:
        The function runs an infinite loop to continuously read and send video frames until the video capture object
        cannot read any more frames or an error occurs. It ensures that resources are released by closing the video
        capture object and the socket connection in the finally block.
    """
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Serialize the frame
            data = pickle.dumps(frame)
            # Pack the size of the frame
            message = struct.pack("Q", len(data)) + data
            # Send the frame
            video_conn.sendall(message)

            # Display the video frame locally in the GUI
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
    except Exception as e:
        print(f"Video streaming error: {e}")
    finally:
        cap.release()
        video_conn.close()


def handle_chat(chat_conn, chat_log):
    """
    Handles incoming chat messages from a client connection.

    Args:
        chat_conn (socket.socket): The socket connection to the client.
        chat_log (tkinter.Text): The text widget where chat messages are displayed.

    Functionality:
        - Continuously receives messages from the client.
        - Decodes and displays each message in the chat log.
        - Scrolls the chat log to the latest message.
        - Closes the client connection when done or if an error occurs.

    Exceptions:
        - Catches and prints any exceptions that occur during message handling.
    """
    """Function to handle chat messages."""
    try:
        while True:
            message = chat_conn.recv(1024).decode()
            if not message:
                break
            # Display the client's message in the chat log
            chat_log.insert(END, f"Client: {message}\n")
            chat_log.see(END)
    except Exception as e:
        print(f"Chat error: {e}")
    finally:
        chat_conn.close()


def send_message(chat_conn, chat_log, input_box):
    """Send message to the client."""
    message = input_box.get()
    input_box.delete(0, END)
    if message.strip():
        chat_log.insert(END, f"You: {message}\n")
        chat_log.see(END)
        chat_conn.sendall(message.encode())


def on_close(root, video_conn, chat_conn, cap):
    """Handle application close event."""
    video_conn.close()
    chat_conn.close()
    cap.release()
    root.destroy()


def start_server(ip="0.0.0.0", video_port=9999, chat_port=9998):
    """
    Starts a server to handle video streaming and chat communication.
    Args:
        ip (str): The IP address to bind the server to. Defaults to "0.0.0.0".
        video_port (int): The port number for video streaming. Defaults to 9999.
        chat_port (int): The port number for chat communication. Defaults to 9998.
    Creates:
        - Two sockets for video and chat communication.
        - A GUI window with video display, chat log, input box, and send button.
        - Threads to handle video streaming and chat communication.
    The server listens for incoming connections on the specified ports, accepts them,
    and starts separate threads to handle video streaming and chat communication.
    The GUI window allows the user to view the video stream and chat messages, and send chat messages.
    """
    # Create sockets
    video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    video_socket.bind((ip, video_port))
    chat_socket.bind((ip, chat_port))

    video_socket.listen(1)
    chat_socket.listen(1)

    print(f"Server started for video on {ip}:{video_port}")
    print(f"Server started for chat on {ip}:{chat_port}")

    video_conn, _ = video_socket.accept()
    print("Video connection established")
    chat_conn, _ = chat_socket.accept()
    print("Chat connection established")

    cap = cv2.VideoCapture(0)

    # Create GUI
    root = Tk()
    root.title("Server Chat & Video")

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
    send_button = Button(root, text="Send", command=lambda: send_message(chat_conn, chat_log, input_box))
    send_button.pack()

    # Handle close event
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, video_conn, chat_conn, cap))

    # Start threads for video streaming and chat
    video_thread = threading.Thread(target=handle_video_stream, args=(video_conn, cap, video_label), daemon=True)
    chat_thread = threading.Thread(target=handle_chat, args=(chat_conn, chat_log), daemon=True)

    video_thread.start()
    chat_thread.start()

    root.mainloop()


if __name__ == "__main__":
    start_server()
