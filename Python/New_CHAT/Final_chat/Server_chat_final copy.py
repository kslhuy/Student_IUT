import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9998))
server_socket.listen(1)
print("Server started, waiting for connection...")

conn, addr = server_socket.accept()
print(f"Connection established with {addr}")

while True:
    message = conn.recv(1024).decode()
    if not message:
        break
    print(f"Client: {message}")
    conn.sendall("Message received".encode())