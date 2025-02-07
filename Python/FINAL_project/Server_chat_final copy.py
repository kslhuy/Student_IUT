import socket
import time
import tkinter as tk
from tkinter import messagebox
import threading

class ProportionalControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Proportional Control Server")

        # GUI elements
        self.canvas = tk.Canvas(root, width=400, height=200, bg="white")
        self.canvas.pack()

        self.label = tk.Label(root, text="Time: 0.0s | Position: 0.00 | Velocity: 0.00", font=("Arial", 14))
        self.label.pack()

        # Connection status label
        self.status_label = tk.Label(root, text="Status: Waiting for connection...", font=("Arial", 12), fg="blue")
        self.status_label.pack()

        # Simulation variables
        self.setpoint = 300
        self.vehicle_pos = 50
        self.Kp = 1  # Proportional gain
        self.dt = 0.1  # Time step
        self.time_elapsed = 0  # Track elapsed time

        # Socket setup
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", 9998))
        self.server_socket.listen(1)
        print("Server started, waiting for connection...")

        # Start a thread to handle client connections
        self.conn = None
        self.client_thread = threading.Thread(target=self.handle_client)
        self.client_thread.daemon = True
        self.client_thread.start()

    def handle_client(self):
        """Handle client connection and simulation updates."""
        self.conn, addr = self.server_socket.accept()
        print(f"Connection established with {addr}")

        # Update the status label to show successful connection
        self.status_label.config(text=f"Status: Connected to {addr}", fg="green")

        # Wait for the "start" command from the client
        command = self.conn.recv(1024).decode()
        if command == "start":
            self.status_label.config(text="Status: Simulation running...", fg="orange")
            self.run_simulation()

        self.conn.close()
        self.status_label.config(text="Status: Connection closed.", fg="red")

    def run_simulation(self):
        """Run the simulation and update the GUI and client."""
        while abs(self.setpoint - self.vehicle_pos) > 2:  # Stop when close enough
            error = self.setpoint - self.vehicle_pos
            velocity = self.Kp * error  # P control
            self.vehicle_pos += velocity * self.dt  # Update position
            self.time_elapsed += self.dt

            # Update the server GUI
            self.canvas.delete("all")
            self.canvas.create_oval(self.setpoint-5, 90, self.setpoint+5, 110, fill="red")  # Setpoint
            self.canvas.create_oval(self.vehicle_pos-5, 90, self.vehicle_pos+5, 110, fill="blue")  # Vehicle position
            self.label.config(text=f"Time: {self.time_elapsed:.1f}s | Position: {self.vehicle_pos:.2f} | Velocity: {velocity:.2f}")

            # Send simulation data to the client
            data = f"{self.time_elapsed:.1f},{self.vehicle_pos:.2f},{velocity:.2f}"
            self.conn.sendall(data.encode())

            time.sleep(self.dt)

        self.conn.sendall(b"Simulation ended")
        self.status_label.config(text="Status: Simulation ended.", fg="purple")
        messagebox.showinfo("Simulation Ended", "The simulation has ended.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProportionalControl(root)
    root.mainloop()