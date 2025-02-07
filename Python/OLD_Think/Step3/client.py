"""
This script connects to a server via a socket and receives video frames to display using OpenCV.
Modules:
    cv2: OpenCV library for image processing.
    socket: Provides low-level networking interface.
    pickle: Python object serialization module.
    struct: Provides functions to interpret bytes as packed binary data.
Functions:
    None
Usage:
    Run this script to connect to a server at 127.0.0.1 on port 9999 and display the received video frames.
Details:
    - The client socket is created and connected to the server.
    - Data is received in chunks and accumulated until the full payload size is reached.
    - The message size is unpacked from the received data.
    - The frame data is received and deserialized using pickle.
    - The frame is displayed using OpenCV's imshow function.
    - Press the ESC key to exit the video display.
"""
import cv2
import socket
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9999))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4 * 1024)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = pickle.loads(frame_data)
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break
