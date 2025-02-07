"""
This script sets up a server that captures video frames from a webcam and sends them to a connected client over a socket connection.
Modules:
    cv2: OpenCV library for video capturing and image processing.
    socket: Provides low-level networking interface.
    pickle: Python object serialization library.
    struct: Provides functions to work with C-style data structures.
Functions:
    None
Usage:
    Run this script to start the server. The server will wait for a client to connect, then start capturing video frames from the webcam and send them to the client.
Attributes:
    server_socket (socket.socket): The server socket that listens for incoming connections.
    conn (socket.socket): The socket object for the accepted connection.
    cap (cv2.VideoCapture): The video capture object for the webcam.
"""
import cv2
import socket
import pickle
import struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))
server_socket.listen(1)
print("Waiting for a connection...")

conn, _ = server_socket.accept()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    data = pickle.dumps(frame)
    conn.sendall(struct.pack("Q", len(data)) + data)
