# Server
"""
This script implements a simple TCP server using Python's socket library.
The server performs the following steps:
1. Creates a socket object using IPv4 addressing and TCP protocol.
2. Binds the socket to all available network interfaces on port 9998.
3. Listens for incoming connection requests.
4. Accepts a connection from a client and prints the client's address.
5. Enters a loop to receive messages from the client, print them, and send a confirmation response back to the client.
6. If no message is received, the loop breaks and the connection is closed.
Modules:
    socket: Provides access to the BSD socket interface.
Usage:
    Run this script to start the server. The server will wait for a client to connect and exchange messages.
"""
import socket
# Create a socket object using IPv4 addressing and TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to all available network interfaces on port 9998
# The IP address 0.0.0.0 is a special address that tells the server to bind to all available network 
# interfaces on the machine. This means that the server will accept connections on any network interface,
#  whether it's a local loopback interface, an Ethernet interface, a Wi-Fi interface, etc.
server_socket.bind(("0.0.0.0", 9998))
# Listen for incoming connection requests
server_socket.listen(1)
print("Server started, waiting for connection...")
# Accept a connection from a client and print the client's address
conn, addr = server_socket.accept()
print(f"Connection established with {addr}")
# Enter a loop to receive messages from the client
while True:
    # Receive a message from the client
    message = conn.recv(1024).decode()
    # If no message is received, break the loop
    if not message:
        break
    # Print the received message
    print(f"Client: {message}")
    # Send a confirmation response back to the client
    conn.sendall("Message received".encode())
