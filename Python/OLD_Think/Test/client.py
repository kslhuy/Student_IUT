import socket
import struct
import pickle
import cv2

def start_client(server_ip="127.0.0.1", port=9999):
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))
    print(f"Connected to server {server_ip}:{port}")
    
    data = b""
    payload_size = struct.calcsize("Q")
    
    try:
        while True:
            # Receive message size
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)  # 4KB chunks
                if not packet:
                    break
                data += packet
            
            if len(data) < payload_size:
                break
            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            
            # Receive frame data
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            
            frame_data = data[:msg_size]
            data = data[msg_size:]
            
            # Deserialize the frame
            frame = pickle.loads(frame_data)
            
            # Display the frame
            cv2.imshow("Video Stream", frame)
            if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
                break
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        client_socket.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    start_client()
