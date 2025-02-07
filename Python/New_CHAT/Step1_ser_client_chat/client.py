# Client
"""
This script implements a simple TCP client that connects to a server at a specified IP address and port.
The client sends messages to the server and prints the server's responses.
Modules:
    socket: This module provides access to the BSD socket interface.
Usage:
    Run this script to start the client. The client will prompt for user input to send messages to the server.
    The server's responses will be printed to the console.
Functions:
    None
Example:
    $ python client.py
    You: Hello, Server!
    Server: Hello, Client!
"""
import socket  # Import the socket module to work with network connections
# Create a TCP/IP socket
# socket.AF_INET: This specifies the address family for the socket, which in this case is IPv4.
# 127.0.0.1 is the loopback address for local testing.
# This setup is common for testing client-server applications on the same machine.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the server's IP address and port
client_socket.connect(("172.20.10.12", 9998))
# Continuously prompt the user for input and send messages to the server
while True:
    message = input("You: ")  # Prompt the user to enter a message
    client_socket.sendall(message.encode())  # Send the message to the server, encoded as bytes
    response = client_socket.recv(1024).decode()  # Receive the server's response and decode it
    print(f"Server: {response}")  # Print the server's response to the console
