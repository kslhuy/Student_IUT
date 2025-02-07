import socket
import keyboard  # Install using: pip install keyboard

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

def send_input(key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(key.encode())

def start_client():
    print("Client started. Use arrow keys to control Pacman.")
    print("Press 'Esc' to exit.")

    # Listen for arrow key presses
    keyboard.on_press_key('up', lambda _: send_input('UP'))
    keyboard.on_press_key('down', lambda _: send_input('DOWN'))
    keyboard.on_press_key('left', lambda _: send_input('LEFT'))
    keyboard.on_press_key('right', lambda _: send_input('RIGHT'))

    # Exit on 'Esc' key
    keyboard.wait('esc')

if __name__ == "__main__":
    start_client()