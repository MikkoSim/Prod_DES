###
###
### Helper functions (e.g., logging, configuration)
###
###

import csv
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 

"""
Exports all jobs from the JobManager to a CSV file.

Args:
    job_manager: The JobManager object containing the jobs.
    filename: The name of the CSV file (default: "jobs.csv").
"""

def export_jobs_to_csv(job_manager, filename="jobs.csv"):

    jobs = list(job_manager.jobs.values())  # Get all Job objects from the JobManager

    with open(filename, "w", newline="") as csvfile:
        # Get all unique keys from all job dictionaries
        fieldnames = set().union(*(job.__dict__.keys() for job in jobs)) 
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for job in jobs:
            writer.writerow(job.__dict__)  # Write each job's attributes as a row


"""
Export all events from log to a CSV file.

Args:
    filename:

"""

def export_event_log_to_csv(filename="event_log.csv"):

    return 1


"""
Plot workstation throughput to a column diagram.

Args:
    workstation_

Return:
    Matplotlib figure

"""

def plot_workstation_throughput(workstation_list):
    workstations = []
    throughputs = []
    for workstation in workstation_list:
        return 1