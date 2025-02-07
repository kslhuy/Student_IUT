# UDP Client
import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.sendto(b"Hello, Server!", ("127.0.0.1", 9999))
response, server_address = client_socket.recvfrom(1024)
print("Server response:", response.decode())
client_socket.close()

# UDP Server
import socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 9999))
message, client_address = server_socket.recvfrom(1024)
print(f"Received: {message.decode()}")
server_socket.sendto(b"Message received", client_address)
