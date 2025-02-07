# TCP Client
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9999))
client_socket.sendall(b"Hello, Server!")
response = client_socket.recv(1024)
print("Server response:", response.decode())
client_socket.close()

# TCP Server
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 9999))
server_socket.listen(1)
conn, addr = server_socket.accept()
message = conn.recv(1024).decode()
print(f"Received: {message}")
conn.sendall(b"Message received")
conn.close()
