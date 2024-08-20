###
###
### Handles user interactions, visualization.
### Additional GUI modules if needed (e.g., layouts)
###
###

import tkinter as tk
from core.simulation import *
from utils.utils import *
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Disctere Event Simulation")
        master.geometry("500x600")

        self.label = tk.Label(master, text="Toimii!")
        self.label.pack()

        self.jobs_button = tk.Button(master, text="Generate job list", command=self.handle_jobs_button, )
        self.jobs_button.config(state=tk.DISABLED)
        self.jobs_button.pack()

        self.simulation_window_button = tk.Button(master, text="Simulate", command=self.handle_simulation)
        self.simulation_window_button.pack()

        self.exit_button = tk.Button(master, text="Exit", command = master.quit)
        self.exit_button.pack()




        values = [1, 2, 3, 4, 5]
        categories = ['A', 'B', 'C', 'D', 'E']

        fig = Figure(figsize= (5, 5), dpi = 100)
        plot1 = fig.add_subplot(111) 

        plot1.bar(categories, values)
        plot1.set_xlabel("Categories")
        plot1.set_ylabel("Values")
        plot1.set_title("Random bar chart")
    
        canvas = FigureCanvasTkAgg(fig, master = self.master)   
        canvas.draw() 
    
        canvas.get_tk_widget().pack() 
    
        #toolbar = NavigationToolbar2Tk(canvas, self.master) 
        #toolbar.update() 
    
        #canvas.get_tk_widget().pack() 


    def handle_simulation(self):
        run_simulation()

    def handle_jobs_button(self):
        create_jobs(10, [0.66, 1, 1.33])