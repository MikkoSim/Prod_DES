###
###
### Core simulation logic, event handling, scheduling
### Other core modules (e.g., statistics collection)
###
###

import numpy as np
import csv
import random
from core.resources import *


t = 0
dt = 0.001
production_line = WorkstationManager()
job_list = JobManager()
event_list = EventManager()

"""
Creates jobs. Updates JobManager with new jobs and creates events "job_arrival".
Args:


Returns:

"""


def create_jobs(num_jobs, cv_options):
    for i in range(num_jobs):
        event_list.add_event(t, "job_arrival", job_list.job_id_counter, 1)
        job_list.add_job(1, 0, 1, "job_arrival", random.choice([1,1,1]), 0)
    export_jobs_to_csv(job_list, filename="jobs.csv")

"""
Creates single non-parallel workstations in series. Updates workstation manager with new workstations and creates events for empty workstations.


"""


def create_workstations(num_workstations, cv_options):
    for i in range(num_workstations):
        event_list.add_event(t, "workstation_starvation", -1, production_line.workstation_id_counter)
        production_line.add_workstation((i+1), 0, 1, random.choice([1,1,1]), 0, "Vacant", 0, 0)
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
    num_of_workstations = 3
    num_of_jobs = 1
    print(f"Creating default settings, {num_of_jobs} job(s) and {num_of_workstations} workstation(s).")
    load_test_settings()
    print("SIMULATION STARTS.")

    #print("Test printing JobManager:")
    #print(job_list.jobs)
    #print("Test printing WorkstationManager:")
    #print(production_line.workstations)

    #print("Print all workstations:")
    #print(f"ID: {production_line.workstations[1].id}, location: {production_line.workstations[1].location}")
    #print(f"ID: {production_line.workstations[2].id}, location: {production_line.workstations[2].location}")
    #print(f"ID: {production_line.workstations[3].id}, location: {production_line.workstations[3].location}")

    heapq.heapify(event_list.events) # list converted into heap
    
    while event := event_list.get_next_event():
        event_id = event[0]
        t = event[1]                    ### SIMULATION TIME UPDATED
        event_type = event[2]
        job_id = event[3]
        workstation_id = event[4]
        #print(f"Next event: event_id: {event_id}, t: {t}, event_type: {event_type}, job_id: {job_id}, workstation_id: {workstation_id}")

        if event_type == "job_arrival":
            print(f"Handling jog arrival: job {job_id} at workstation {workstation_id}")
            handle_job_arrival(job_id, workstation_id)
        elif event_type == "job_waiting":
            print(f"Handling jog waiting: job {job_id} at workstation {workstation_id}")
            handle_job_waiting(job_id, workstation_id)
        elif event_type == "job_phase_ready":
            print(f"Handling jog phase ready: job {job_id} at workstation {workstation_id}")
            handle_job_phase_ready(job_id, workstation_id)
        elif event_type == "job_completion":
            print(f"Handling jog completion: job {job_id} at workstation {workstation_id}")
            handle_job_completion(job_id, workstation_id)
        elif event_type == "job_processing":
            print(f"Handling jog processing: job {job_id} at workstation {workstation_id}")
            handle_job_processing(job_id, workstation_id)
        elif event_type == "workstation_ready":
            handle_workstation_ready()
        elif event_type == "workstation_starvation":
            handle_workstation_starvation()
        elif event_type == "workstation_congestion":
            handle_workstation_congestion()
    print("SIMULATION ENDS.")


"""                                             (SEND)      (RECEIVE)
ARRIVE  =>  PROCESS          =>          PHASE_READY     =>     ARRIVE
    =>  WAITING                             =>      COMPLETION
          =>  PROCESS         
"""




"""
If workstation == None, then job has to be at the beginning of routing.
    => Place job at first routing step with vacant workstation
    If vacant workstation is found
        => Create job_processing event
    If vacant workstation is NOT found
        => Create job_waiting event


If workstation > 0, then routing is incremented.
    => Place job to incremented vacant workstation
    If vacant workstation is found
        => Create job_processing event
    If vacant workstation is NOT found
        => Create job_waiting event
     

"""

def handle_job_arrival(job_id, workstation_id):
    requested_routing = job_list.get_job_routing(job_id)
    print(f"Job {job_id} is looking workstation from step {requested_routing}...")
    if production_line.search_vacant_workstation_in_routing(requested_routing):
        print(f"Job {job_id} found a workstation  {requested_routing}!")
        event_list.add_event(t, "job_processing", job_id, workstation_id)
    else:
        print(f"Job {job_id} did not find vacant workstation.")
        event_list.add_event(t, "job_waiting", job_id, workstation_id)


"""
Schedule next open workstation in next routing.
Must calculate what workstation will be available first, then allocate job there.

"""


def handle_job_waiting(job_id, workstation_id):
    job = job_list.get_job(job_id)
    previous_routing_phase = job.location
    next_routing_phase = previous_routing_phase + 1
    waiting_time = time_for_vacancy(next_routing_phase)
    event_list.add_event(t + waiting_time, "job_processing", job_id, workstation_id)

"""
Check if routing is available.

This acts as placeholder for transportation events. Without an event, transportation happens instantly.

If workstation > 1, then job has to be at the beginning of routing.
    => Place job at incremented workstation
    If vacant workstation is found
        => Create job_processing event
    If vacant workstation is NOT found
        => Create job_waiting event


If workstation == routing length
    => Schedule completion event

"""


def handle_job_phase_ready(job_id, workstation_id):
    job = job_list.get_job(job_id)
    workstation = production_line.get_workstation(workstation_id)
    if job_has_more_steps_in_routing():
        target_location = current_location + 1
        # Set target location, incremented
        # Check if target workstation has vacancy
        if production_line.search_vacant_workstation_in_routing()
    else:



"""
Remove job from system. Collect any data.

"""


def handle_job_completion(job_id, workstation_id):
    job = job_list.get_job(job_id)
    workstation = production_line.get_workstation(workstation_id)

    if job_has_more_steps_in_routing:
        return 1
        # move job to the next vacant workstation
        # schedule next "job_arrival" event
    else:
        return 1
        # job is completed, remove from system


"""
Schedule phase ready event.
Calculate processing time.

"""


def handle_job_processing(job_id, workstation_id):
    #job = job_list.get_job(job_id)
    #workstation = production_line.get_workstation(workstation_id)

    processing_time = calculate_processing_time(job_id, workstation_id)
    event_list.add_event(t + processing_time, "job_phase_ready", job_id, workstation_id)



def handle_workstation_ready():

    return 1



def handle_workstation_starvation():

    return 1



def handle_workstation_congestion():

    return 1







### Load 3 jobs, in a simple 1-1-1 prod.line.

def load_test_settings():
    create_workstations(3, [1, 1, 1])
    create_jobs(1, [1, 1, 1])
    return 0



def all_jobs_completed():
    return 1


### def search_vacant_workstation_in_routing(self, location):
###     for workstation in self.workstations.values():
###         if workstation.location == location and workstation.status == 'Vacant':
###             return True
###     return False

def time_for_vacancy(routing_phase):
    
    return 0



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
    print(f"Calculating process time for job: {job_id} at workstation: {workstation_id}")
    job = job_list.get_job(job_id)
    current_routing = job.location
    workstation = production_line.get_workstation(workstation_id)
    true_processing_time = job.true_processing_time * workstation.true_capacity
    return true_processing_time