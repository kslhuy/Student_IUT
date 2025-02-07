import socket
import tkinter as tk
from tkinter import messagebox

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proportional Control Client")

        self.canvas = tk.Canvas(root, width=400, height=200, bg="white")
        self.canvas.pack()

        self.label = tk.Label(root, text="Time: 0.0s | Position: 0.00 | Velocity: 0.00", font=("Arial", 14))
        self.label.pack()

        self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        # Initialize socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 9998))

    def start_simulation(self):
        # Send "start" command to the server
        self.client_socket.sendall(b"start")

        # Start receiving updates from the server
        self.receive_updates()

    def receive_updates(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if data == "Simulation ended":
                    messagebox.showinfo("Simulation Ended", "The simulation has ended.")
                    break

                # Parse the data (time, position, velocity)
                time_elapsed, vehicle_pos, velocity = map(float, data.split(","))

                # Update the GUI
                self.canvas.delete("all")
                self.canvas.create_oval(300-5, 90, 300+5, 110, fill="red")  # Setpoint
                self.canvas.create_oval(vehicle_pos-5, 90, vehicle_pos+5, 110, fill="blue")  # Vehicle position
                self.label.config(text=f"Time: {time_elapsed:.1f}s | Position: {vehicle_pos:.2f} | Velocity: {velocity:.2f}")

                self.root.update()
            except Exception as e:
                print(f"Error: {e}")
                break

        self.client_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()