import tkinter as tk
import time

class ProportionalControl:
    def __init__(self, root):
        self.root = root
        self.root.title("Proportional Control")

        self.canvas = tk.Canvas(root, width=400, height=200, bg="white")
        self.canvas.pack()

        self.setpoint = 300
        self.vehicle_pos = 50
        self.Kp = 1 # Proportional gain
        self.dt = 0.1  # Time step

        self.time_elapsed = 0  # Track elapsed time

        self.label = tk.Label(root, text=f"Time: {self.time_elapsed:.1f}s | Position: {self.vehicle_pos:.2f} | Velocity: {0:.2f}", font=("Arial", 14))
        self.label.pack()

        self.run_simulation()

    def run_simulation(self):
        while abs(self.setpoint - self.vehicle_pos) > 2:  # Stop when close enough
            error = self.setpoint - self.vehicle_pos
            velocity = self.Kp * error  # P control
            self.vehicle_pos += velocity * self.dt  # Update position

            self.canvas.delete("all")
            self.canvas.create_oval(self.setpoint-5, 90, self.setpoint+5, 110, fill="red")
            self.canvas.create_oval(self.vehicle_pos-5, 90, self.vehicle_pos+5, 110, fill="blue")
            self.label.config(text=f"Time: {self.time_elapsed:.1f}s | Position: {self.vehicle_pos:.2f} | Velocity: {velocity:.2f}")

            self.root.update()
            time.sleep(self.dt)

root = tk.Tk()
app = ProportionalControl(root)
root.mainloop()
