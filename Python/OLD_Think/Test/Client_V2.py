import cv2
import socket
import struct
import pickle
import threading
from tkinter import Tk, Text, Entry, Button, Scrollbar, END, Frame


def receive_video_stream(video_socket, video_label):
    """Receive and display video stream."""
    data = b""
    payload_size = struct.calcsize("Q")
    try:
        while True:
            while len(data) < payload_size:
                packet = video_socket.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            if len(data) < payload_size:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]

            while len(data) < msg_size:
                data += video_socket.recv(4 * 1024)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Deserialize frame
            frame = pickle.loads(frame_data)
            # Convert frame to Tkinter-compatible image
            cv2.imshow("Client Video Stream", frame)
            if cv2.waitKey(1) == 27:  # Press ESC to exit
                break
    except Exception as e:
        print(f"Video receiving error: {e}")
    finally:
        cv2.destroyAllWindows()


def handle_chat(chat_socket, chat_log):
    """Receive chat messages from the server."""
    try:
        while True:
            message = chat_socket.recv(1024).decode()
            if not message:
                break
            chat_log.insert(END, f"Server: {message}\n")
            chat_log.see(END)
    except Exception as e:
        print(f"Chat error: {e}")
    finally:
        chat_socket.close()


def send_message(chat_socket, chat_log, input_box):
    """Send message to the server."""
    message = input_box.get()
    input_box.delete(0, END)
    if message.strip():
        chat_log.insert(END, f"You: {message}\n")
        chat_log.see(END)
        chat_socket.sendall(message.encode())


def start_client(server_ip="127.0.0.1", video_port=9999, chat_port=9998):
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

    # Start threads for video streaming and chat
    video_thread = threading.Thread(target=receive_video_stream, args=(video_socket, None))
    chat_thread = threading.Thread(target=handle_chat, args=(chat_socket, chat_log))

    video_thread.start()
    chat_thread.start()

    root.mainloop()

    video_thread.join()
    chat_thread.join()


if __name__ == "__main__":
    start_client()
