###
###
### Handles user interactions, visualization.
### Additional GUI modules if needed (e.g., layouts)
###
###

import tkinter as tk
from core.simulation import *

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Disctere Event Simulation")

        self.label = tk.Label(master, text="Toimii!")
        self.label.pack()

        self.jobs_button = tk.Button(master, text="Generate job list", command=self.handle_jobs_button)
        self.jobs_button.pack()

        self.simulation_window_button = tk.Button(master, text="Simulate", command=self.handle_simulation)
        self.simulation_window_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command = master.quit)
        self.exit_button.pack()

    def handle_simulation(self):
        new_window = tk.Toplevel(self.master)
        new_window.title ("Simulation")

        new_label = tk.Label(new_window, text="Toimii!")
        new_label.pack()

    def handle_jobs_button(self):
        generate_jobs(10, [1,1,1], (10,20), [0.66, 1, 1.33])