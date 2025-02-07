import tkinter as tk
import time

class MotionSimulation:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=200)
        self.canvas.pack()

        self.setpoint = 300  # Target position
        self.vehicle_pos = 50  # Initial position
        self.velocity = 10  # Constant velocity

        self.dt = 0.1  # Time step
        self.time_elapsed = 0  # Track elapsed time

        self.label = tk.Label(root, text=f"Time: {self.time_elapsed:.1f}s | Position: {self.vehicle_pos:.2f} | Velocity: {0:.2f}", font=("Arial", 14))
        self.label.pack()

        self.run_simulation()
        
    def run_simulation(self):
        while self.vehicle_pos < self.setpoint:  # Move until reaching the target
            self.vehicle_pos += self.velocity * self.dt  # Update position
            self.time_elapsed += self.dt  # Update time

            self.canvas.delete("all")

            self.canvas.create_oval(self.setpoint-5, 90, self.setpoint+5, 110, fill="red")
            self.canvas.create_oval(self.vehicle_pos-5, 90, self.vehicle_pos+5, 110, fill="blue")
            self.label.config(text=f"Time: {self.time_elapsed:.1f}s | Position: {self.vehicle_pos:.2f} | Velocity: {self.velocity:.2f}")

            self.root.update()
            time.sleep(self.dt)

root = tk.Tk()
app = MotionSimulation(root)
root.mainloop()