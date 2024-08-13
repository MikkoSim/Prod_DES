###
###
### Core simulation logic, event handling, scheduling
### Other core modules (e.g., statistics collection)
###
###

import numpy as np
import csv
import random
from core.simulation import *
from core.resources import *


t = 0
dt = 0.001
production_line = WorkstationManager()
job_list = JobManager()

"""
Generates a list of jobs with production order ID, mean process time,
coefficient of variation, status, and location in routing.

Args:
    num_jobs: The number of jobs to generate.
    routing: The routing (sequence of workstations) for all jobs.
    mean_process_time_range: A tuple (min, max) specifying the range for mean process times.
    cv_options: A list of possible coefficient of variation values.

Returns:
    A list of dictionaries representing the jobs.
"""


def generate_jobs(num_jobs, routing, mean_process_time_range, cv_options):
    for i in range(num_jobs):
        job = Job(i, 0, 0, random.uniform(30, 30), "Pending", random.choice(cv_options), 0)
        job.calculate_job_std()
        job_list.add_workstation(job)
    export_jobs_to_csv(job_list, filename="jobs.csv")

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

def run_simulation():
    while(1):

        t = t + dt
        handle_events()


def handle_events():
    return 0