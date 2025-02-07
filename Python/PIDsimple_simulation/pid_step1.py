import tkinter as tk

# class SimpleGUI:
#     def __init__(self, root):
#         """
#         Initializes the basic GUI setup for the PID simulation.
#         Args:
#             root (tk.Tk): The root window of the Tkinter application.
#         Attributes:
#             root (tk.Tk): The root window of the Tkinter application.
#             canvas (tk.Canvas): The canvas widget for drawing the setpoint and vehicle.
#             setpoint (int): The target position, represented as a red circle on the canvas.
#             vehicle_pos (int): The initial position of the vehicle, represented as a blue circle on the canvas.
#             time_elapsed (float): The elapsed time since the start of the simulation.
#             label (tk.Label): The label widget displaying the time, position, and velocity.
#         """
#         self.root = root
#         self.root.title("Basic GUI Setup")

#         self.canvas = tk.Canvas(root, width=400, height=200, bg="white")
#         self.canvas.pack()

#         # Draw setpoint (target position in red)
#         self.setpoint = 300
#         self.canvas.create_oval(self.setpoint-5, 90, self.setpoint+5, 110, fill="red")

#         # Draw vehicle (initial position in blue)
#         self.vehicle_pos = 50
#         self.canvas.create_oval(self.vehicle_pos-5, 90, self.vehicle_pos+5, 110, fill="blue")
#         self.time_elapsed = 0  # Track elapsed time


#         self.label = tk.Label(root, text=f"Time: {self.time_elapsed:.1f}s | Position: {self.vehicle_pos:.2f} | Velocity: {0:.2f}", font=("Arial", 14))
#         self.label.pack()
        
# """
# Create the root window.
# Create an instance of PositionControlGUI.
# Start the Tkinter main loop to run the GUI
# """
# root = tk.Tk()
# app = SimpleGUI(root)
# root.mainloop()


"""Fucntion to run the simulation"""


import tkinter as tk
def Graphic():
    setpoint = 300  # Target position , point rouge
    vehicle_pos = 50  # Initial position , point bleu
    velocity = 10  # Constant velocity
    dt = 0.1  # Time step
    time_elapsed = 0  # Track elapsed time
    # Set up the tkinter root window
    root = tk.Tk()  # Create the main window
    canvas = tk.Canvas(root, width=400, height=200)  # Create a canvas widget with specified width and height
    canvas.pack()  # Add the canvas to the main window
    # Create a label to display time, position, and velocity
    label = tk.Label(root, text=f"Time: {time_elapsed:.1f}s | Position: {vehicle_pos:.2f} \
                    | Velocity: {velocity:.2f}", font=("Arial", 14))
    label.pack()  # Add the label to the main window
    canvas.create_oval(setpoint-5, 90, setpoint+5, 110, fill="red")
    canvas.create_oval(vehicle_pos-5, 90, vehicle_pos+5, 110, fill="blue")
    root.mainloop()

Graphic()



"""Just line code"""

import tkinter as tk
setpoint = 300  # Target position , point rouge
vehicle_pos = 50  # Initial position , point bleu
velocity = 10  # Constant velocity

dt = 0.1  # Time step
time_elapsed = 0  # Track elapsed time

# Set up the tkinter root window
root = tk.Tk()  # Create the main window
canvas = tk.Canvas(root, width=400, height=200)  # Create a canvas widget with specified width and height
canvas.pack()  # Add the canvas to the main window

# Create a label to display time, position, and velocity
label = tk.Label(root, text=f"Time: {time_elapsed:.1f}s | Position: {vehicle_pos:.2f} \
                | Velocity: {velocity:.2f}", font=("Arial", 14))
label.pack()  # Add the label to the main window

canvas.create_oval(setpoint-5, 90, setpoint+5, 110, fill="red")
canvas.create_oval(vehicle_pos-5, 90, vehicle_pos+5, 110, fill="blue")
root.mainloop()