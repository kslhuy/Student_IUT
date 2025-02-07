import tkinter as tk
import time
def run_simulation():
    setpoint = 300  # Target position
    vehicle_pos = 50  # Initial position
    velocity = 10  # Constant velocity
    dt = 0.1  # Time step
    time_elapsed = 0  # Track elapsed time
    # Set up the tkinter root window
    root = tk.Tk()
    canvas = tk.Canvas(root, width=400, height=200)
    canvas.pack()
    label = tk.Label(root, text=f"Time: {time_elapsed:.1f}s | Position: {vehicle_pos:.2f} | Velocity: {velocity:.2f}",
                     font=("Arial", 14))
    label.pack()
    while abs(setpoint - vehicle_pos) >= 0.01 :  # Move until reaching the target
        velocity = setpoint - vehicle_pos  # P control

        vehicle_pos = vehicle_pos + velocity * dt  # Update position
        
        time_elapsed = time_elapsed + dt  # Update time
        canvas.delete("all")  # Clear previous drawings
        # Draw setpoint (target) and current position of the vehicle
        canvas.create_oval(setpoint-5, 90, setpoint+5, 110, fill="red")
        canvas.create_oval(vehicle_pos-5, 90, vehicle_pos+5, 110, fill="blue")
        # Update label with current time and position
        label.config(text=f"Time: {time_elapsed:.1f}s | Position: {vehicle_pos:.2f} | Velocity: {velocity:.2f}")
        root.update()  # Update the tkinter GUI
        time.sleep(dt)  # Wait for the next time step
    root.mainloop()
run_simulation()
