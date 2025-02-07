import tkinter as tk
import time

class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.prev_error = 0
        self.integral = 0

    def compute(self, setpoint, actual_position):
        error = setpoint - actual_position
        self.integral += error
        derivative = error - self.prev_error
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.prev_error = error
        return output

class PositionControlGUI:
    """
    A GUI application for simulating position control using a PID controller.
    Attributes:
        root (tk.Tk): The root window of the Tkinter application.
        pid (PIDController): The PID controller instance for position control.
        setpoint (float): The target position to be achieved.
        actual_position (float): The current position of the vehicle.
        velocity (float): The current velocity of the vehicle.
        dt (float): The time step for the simulation.
        threshold (float): The acceptable range near the setpoint.
        time_elapsed (float): The elapsed time since the start of the simulation.
        canvas (tk.Canvas): The canvas widget for drawing the simulation scene.
        label (tk.Label): The label widget for displaying simulation information.
        start_button (tk.Button): The button widget to start the simulation.
    Methods:
        draw_scene(): Draws the current state of the simulation on the canvas.
        run_simulation(): Runs the position control simulation until the vehicle is within the acceptable range of the setpoint.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Position PID Control")
        
        self.pid = PIDController(kp=1, ki=0.01, kd=0.05)
        self.setpoint = 300  # Target position
        self.actual_position = 50  # Initial position
        self.velocity = 0  # Initial velocity
        self.dt = 0.1  # Time step
        self.threshold = 2  # Acceptable range near setpoint
        self.time_elapsed = 0  # Track elapsed time
        
        self.canvas = tk.Canvas(root, width=400, height=200, bg="white")
        self.canvas.pack()
        
        self.label = tk.Label(root, text=f"Time: {self.time_elapsed:.1f}s | Position: {self.actual_position:.2f} | Velocity: {self.velocity:.2f}", font=("Arial", 14))
        self.label.pack()
        
        self.start_button = tk.Button(root, text="Start", command=self.run_simulation)
        self.start_button.pack()
        
        self.draw_scene()
    
    def draw_scene(self):
        self.canvas.delete("all")
        self.canvas.create_oval(self.setpoint-5, 90, self.setpoint+5, 110, fill="red")  # Setpoint marker
        self.canvas.create_oval(self.actual_position-5, 90, self.actual_position+5, 110, fill="blue")  # Vehicle marker
    
    def run_simulation(self):
        self.time_elapsed = 0  # Reset time at start
        while abs(self.setpoint - self.actual_position) > self.threshold:  # Run until within range
            control_signal = self.pid.compute(self.setpoint, self.actual_position)
            self.velocity = control_signal  # Control affects velocity
            self.actual_position += self.velocity * self.dt  # Update position using velocity
            self.time_elapsed += self.dt  # Update time
            
            self.draw_scene()
            self.label.config(text=f"Time: {self.time_elapsed:.1f}s | Position: {self.actual_position:.2f} | Velocity: {self.velocity:.2f}")
            self.root.update()
            time.sleep(self.dt)

root = tk.Tk()
app = PositionControlGUI(root)
root.mainloop()
