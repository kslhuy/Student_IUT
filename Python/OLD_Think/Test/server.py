import cv2
import socket
import struct
import pickle

def start_server(ip="127.0.0.1", port=9999):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Server started at {ip}:{port}, waiting for client...")
    
    conn, addr = server_socket.accept()
    print(f"Connection established with: {addr}")
    
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)  # Change `0` to your camera index if necessary

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Serialize the frame
            data = pickle.dumps(frame)
            # Pack the size of the frame
            message = struct.pack("Q", len(data)) + data
            # Send the frame to the client
            conn.sendall(message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cap.release()
        conn.close()
        server_socket.close()

        

if __name__ == "__main__":
    start_server()
