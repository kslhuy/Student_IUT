import cv2
import socket
import struct
import pickle
import threading
from tkinter import Tk, Text, Entry, Button, Scrollbar, END, Frame


def handle_video_stream(video_conn, cap):
    """Function to handle video streaming."""
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
    except Exception as e:
        print(f"Video streaming error: {e}")
    finally:
        cap.release()
        video_conn.close()


def handle_chat(chat_conn, chat_log):
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


def start_server(ip="0.0.0.0", video_port=9999, chat_port=9998):
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

    # Start threads for video streaming and chat
    video_thread = threading.Thread(target=handle_video_stream, args=(video_conn, cap))
    chat_thread = threading.Thread(target=handle_chat, args=(chat_conn, chat_log))

    video_thread.start()
    chat_thread.start()

    root.mainloop()

    video_thread.join()
    chat_thread.join()


if __name__ == "__main__":
    start_server()
