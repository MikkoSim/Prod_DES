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
event_list = EventManager()

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

def create_jobs(num_jobs, cv_options, job_manager, event_manager):
    for i in range(num_jobs):
        job = Job(i, 0, 0, random.uniform(30, 30), "Pending", random.choice(cv_options), 0)
        job.calculate_job_std()
        job_manager.add_job(job)
        event_manager.add_event(i, "job_arrival", job_id=job.id)
    export_jobs_to_csv(job_list, filename="jobs.csv")

def create_workstations(num_workstations, cv_options, workstation_manager, event_manager):
    for i in range(num_workstations):
        workstation = Workstation(i, (i + 1), 0, 1, random.choice(cv_options), 0, "Vacant", 0, 0)
        workstation.calculate_workstation_std()
        production_line.add_workstation(workstation)
        event_list.add_event()
        ### KESKEN !!! ###
    return 1


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

    load_test_settings()

    heapq.heapify(event_list.events) # list converted into heap
    
    while event := event_list.get_next_event():
        t = event[0] # update simulation time
        event_type = event[1]
        job_id = event[2]
        workstation_id = event[3]

        if event_type == "job_arrival":
            handle_job_arrival(job_id, production_line, event_list)
        elif event_type == "job_completion":
            handle_job_completion(job_id,workstation_id, job_list, production_line, event_list)
        elif event_type == "job_waiting":
            handle_job_waiting(job_id, workstation_id, job_list, production_line, event_list)
        elif event_type == "job_processing":
            handle_job_processing()
        elif event_type == "workstation_ready":
            handle_workstation_ready()
        elif event_type == "workstation_starvation":
            handle_workstation_starvation()
        elif event_type == "workstation_congestion":
            handle_workstation_congestion()






def handle_job_arrival(job_id, workstation_id):
    job = job_list.get_job(job_id)
    workstation = production_line.get_workstation(workstation_id)

    if workstation_is_found:

        processing_time = calculate_processing_time(job, workstation)

        event_list.add_event(t + processing_time, "job_completion", job_id = job.id, workstation_id = workstation.id)

    else:
        return 1
        #if workstation is NOT available...

def handle_job_waiting(job_id, workstation_id, job_manager, workstation_manager, event_manager):
    job = job_list.get_job(job_id)
    previous_routing_phase = job_list.get_job_routing(job_id)
    next_routing_phase = previous_routing_phase + 1
    if workstation_is_available_in_routing(next_routing_phase):
        return 1
        # move job to the next vacant workstation
        # schedule next "job_arrival" event
    else:
        return 1
        # should we start recoring waiting time???


def handle_job_completion(job_id, workstation_id, job_manager, workstation_manager, event_manager):
    job = job_manager.get_job(job_id)
    workstation = workstation_manager.get_workstation(workstation_id)

    if job_has_more_steps_in_routing:
        return 1
        # move job to the next vacant workstation
        # schedule next "job_arrival" event
    else:
        return 1
        # job is completed, remove from system



def handle_job_processing():
    
    return 1



def handle_workstation_ready():

    return 1



def handle_workstation_starvation():

    return 1



def handle_workstation_congestion():

    return 1







### Load 3 jobs, in a simple 1-1-1 prod.line.

def load_test_settings():
    """
    w1 = Workstation(1, 1, 0, 20, 1, 0, "Starvation", 0, 0)
    production_line.add_workstation(w1)
    w2 = Workstation(2, 2, 0, 20, 1, 0, "Starvation", 0, 0)
    production_line.add_workstation(w2)
    w3 = Workstation(3, 3, 0, 20, 1, 0, "Starvation", 0, 0)
    production_line.add_workstation(w3)

    j1 = Job(1, 0, 0, 20, "Pending", 1, 0)
    job_list.add_job(j1)
    j2 = Job(1, 0, 0, 20, "Pending", 1, 0)
    job_list.add_job(j2)
    j3 = Job(1, 0, 0, 20, "Pending", 1, 0)
    job_list.add_job(j3)

    event_list.add_event(1, "job_arrived")
    event_list.add_event(2, "job_arrived")
    event_list.add_event(3, "job_arrived")
    event_list.add_event(4, "workstation_congestion")
    event_list.add_event(5, "workstation_congestion")
    event_list.add_event(6, "workstation_congestion")
    """
    create_workstations
    create_jobs(10, (0.66, 1, 1.33), production_line, event_list)
    return 0



def all_jobs_completed():
    return 1




def workstation_is_available_in_routing():
    return 1



def job_has_more_steps_in_routing(job_id, ):
    ### If a routing is expressed as a vector, a routing has finished if its routing phase is 1 > len(vector)
    job_id = job_list.get_job(job_id)
    if job_list.get_job_routing(job_id) < (len(prod_line) + 1):
        return True
    else:
        return False


def calculate_processing_time(job_id, workstation_id):
    """
    Job mean and true process times are vectors with same dimension as routing vector.
    """
    job = job_list.get_job(job_id)
    current_routing = job.routing
    workstation = production_line.get_workstation(workstation_id)
    true_processing_time = job.true_processing_time[current_routing] * workstation.true_capacity
    return true_processing_time

def workstation_is_found():


    return 1
