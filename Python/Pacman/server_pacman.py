import socket
import pygame
import threading

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pacman Server")
clock = pygame.time.Clock()

# Pacman properties
pacman_x, pacman_y = 400, 300
pacman_speed = 5

def handle_client(conn, addr):
    global pacman_x, pacman_y
    print(f"Connected by {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        # Update Pacman position based on client input
        if data == 'UP':
            pacman_y -= pacman_speed
        elif data == 'DOWN':
            pacman_y += pacman_speed
        elif data == 'LEFT':
            pacman_x -= pacman_speed
        elif data == 'RIGHT':
            pacman_x += pacman_speed

        # Ensure Pacman stays within screen bounds
        pacman_x = max(0, min(pacman_x, 800 - 20))
        pacman_y = max(0, min(pacman_y, 600 - 20))

    conn.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear screen
            screen.fill((0, 0, 0))

            # Draw Pacman
            pygame.draw.circle(screen, (255, 255, 0), (pacman_x, pacman_y), 20)

            # Update display
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    start_server()