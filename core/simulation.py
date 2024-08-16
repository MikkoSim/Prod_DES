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


t = 0.0
dt = 0.001
workstation_dict = WorkstationManager()
job_dict = JobManager()
event_dict = EventManager()

"""
Creates jobs. Updates JobManager with new jobs and creates events "job_arrival".
Args:


Returns:

"""


def create_jobs(num_jobs, cv_options):
    for i in range(num_jobs):
        event_dict.add_event(t, "job_created", job_dict.job_id_counter, 0)
        job_dict.add_job(0, 0, 1, "job_created", random.choice([1,1,1]), 0)
    #export_jobs_to_csv(job_dict, filename="jobs.csv")                      ### Export jobs to CSV-file

"""
Creates single non-parallel workstations in series. Updates workstation manager with new workstations and creates events for empty workstations.


"""


def create_workstations(num_workstations, list_of_mean_times, cv_options):
    for i in range(num_workstations):
        event_dict.add_event(t, "workstation_starvation", -1, workstation_dict.workstation_id_counter)
        workstation_dict.add_workstation((i+1), 0, list_of_mean_times[i], random.choice(cv_options), 0, "Vacant", 0, 0)
    return 1

"""
Creates single non-parallel workstations in series. Updates workstation manager with new workstations and creates events for empty workstations.


"""

def create_source(source_type, target_object, num_of_elements, distr_func, mean, sigma):
    if source_type == "Job":
        if isinstance(target_object, Workstation):
            ### OK
            return 1
        else:
            print(f"Error: Source type does not match with target object")
    elif source_type == "Material":
        if isinstance(target_object, Workstation):
            ### OK
            return 1
        else:
            print(f"Error: Source type does not match with target object")
        return 1
    elif source_type == "Worker":
        if isinstance(target_object, Workstation):
            ### OK
            return 1
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
    global t
    num_of_workstations = 3
    num_of_jobs = 1
    print(f"Creating default settings, {num_of_jobs} job(s) and {num_of_workstations} workstation(s).")
    load_test_settings()
    print("SIMULATION STARTS.")

    #print("Test printing JobManager:")
    #print(job_dict.jobs)
    #print("Test printing WorkstationManager:")
    #print(workstation_dict.workstations)

    #print("Print all workstations:")
    #print(f"ID: {workstation_dict.workstations[1].id}, location: {workstation_dict.workstations[1].location}")
    #print(f"ID: {workstation_dict.workstations[2].id}, location: {workstation_dict.workstations[2].location}")
    #print(f"ID: {workstation_dict.workstations[3].id}, location: {workstation_dict.workstations[3].location}")

    heapq.heapify(event_dict.events) # list converted into heap
    
    while event := event_dict.get_next_event():
        event_id = event[0]
        t = event[1]                    ### SIMULATION TIME UPDATED
        event_type = event[2]
        job_id = event[3]
        workstation_id = event[4]
        workstation = workstation_dict.get_workstation(workstation_id)
        #print(f"Next event: event_id: {event_id}, t: {t}, event_type: {event_type}, job_id: {job_id}, workstation_id: {workstation_id}")


        if event_type == "job_created":
            print(f"TIME: {t}, Handling jog creation: job {job_id} at source.")
            handle_job_created(job_id, workstation_id)
        elif event_type == "job_arrival":
            print(f"TIME: {t}, Handling jog arrival: job {job_id} at workstation {workstation_id}, location {workstation.location}")
            handle_job_arrival(job_id, workstation_id)
        elif event_type == "job_waiting":
            print(f"TIME: {t}, Handling jog waiting: job {job_id} at workstation {workstation_id}")
            handle_job_waiting(job_id, workstation_id)
        elif event_type == "job_phase_ready":
            print(f"TIME: {t}, Handling jog phase ready: job {job_id} at workstation {workstation_id}")
            handle_job_phase_ready(job_id, workstation_id)
        elif event_type == "job_completion":
            print(f"TIME: {t}, Handling jog completion: job {job_id} at workstation {workstation_id}")
            handle_job_completion(job_id, workstation_id)
        elif event_type == "job_processing":
            print(f"TIME: {t}, Handling jog processing: job {job_id} at workstation {workstation_id}")
            handle_job_processing(job_id, workstation_id)
        elif event_type == "workstation_ready":
            handle_workstation_ready()
        elif event_type == "workstation_starvation":
            handle_workstation_starvation()
        elif event_type == "workstation_congestion":
            handle_workstation_congestion()
    print(f"Total simulation time: {t} of some units.")
    print("SIMULATION ENDS.")
    t = 0
    ### Save list to excel?


"""  (SEND)  (RECEIVE)                                             (SEND)     (RECEIVE)
    GEN    =>    ARRIVE  =>  PROCESS          =>          PHASE_READY     =>     ARRIVE
     WAIT           =>  WAITING                                =>   COMPLETION
       PROCESS            =>  PROCESS         
"""


def handle_job_created(job_id, workstation_id):
    requested_location = 1
    new_workstation_id = 1
    job = job_dict.get_job(job_id)
    workstation = workstation_dict.get_workstation(new_workstation_id)
    if workstation_dict.search_vacant_workstation_in_routing(requested_location):
        #print(f"Job {job_id} found a workstation  {requested_routing}!")
        allocate_job_to_workstation(job_id, new_workstation_id, requested_location)
        #workstation.status = "Received"
        event_dict.add_event(t, "job_arrival", job_id, new_workstation_id)
    else:
        #print(f"Job {job_id} did not find vacant workstation.")
        event_dict.add_event(t, "job_waiting", job_id, workstation_id)

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
    job = job_dict.get_job(job_id)
    workstation = workstation_dict.get_workstation(workstation_id)
    #print(f"Job {job_id} is looking workstation from step {requested_routing}...")
    if workstation_dict.search_vacant_workstation_in_routing(job.location):
        print(f"Job {job_id} found a workstation from location {job.location}!")
        event_dict.add_event(t, "job_processing", job_id, workstation_id)
        workstation.status = "Processing"
    else:
        print(f"Job {job_id} did not find vacant workstation from location {job.location}.")
        event_dict.add_event(t, "job_waiting", job_id, workstation_id)


"""
Schedule next open workstation in next routing.
Must calculate what workstation will be available first, then allocate job there.

"""


def handle_job_waiting(job_id, workstation_id):
    job = job_dict.get_job(job_id)
    workstation = workstation_dict
    previous_routing_phase = job.location
    next_routing_phase = previous_routing_phase + 1
    waiting_time = time_for_vacancy(next_routing_phase)
    event_dict.add_event(t + waiting_time, "job_processing", job_id, workstation_id)


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
    job = job_dict.get_job(job_id)
    workstation = workstation_dict.get_workstation(workstation_id)
    new_workstation_id = workstation_id + 1
    new_job_location = job.location + 1
    if job_has_more_steps_in_routing(job_id):
        if workstation_dict.search_vacant_workstation_in_routing(new_job_location):        # Check if target workstation has vacancy
            allocate_job_to_workstation(job_id, new_workstation_id, new_job_location)        # Set target location, incremented
            new_workstation = workstation_dict.get_workstation(new_workstation_id)
            workstation.status = "Vacant"
            event_dict.add_event(t, "job_arrival", job_id, new_workstation_id)
            #new_workstation.status = "Received"
        else:
            event_dict.add_event(t, "job_waiting", job_id, new_workstation_id)
    else:
        event_dict.add_event(t, "job_completion", job_id, workstation_id)
        workstation.status = "Vacant"


"""
Remove job from system. Collect any data.

"""


def handle_job_completion(job_id, workstation_id):
    job = job_dict.get_job(job_id)
    workstation = workstation_dict.get_workstation(workstation_id)

    return 1


"""
Schedule phase ready event.
Calculate processing time.

"""


def handle_job_processing(job_id, workstation_id):
    processing_time = calculate_processing_time(job_id, workstation_id)
    event_dict.add_event(t + processing_time, "job_phase_ready", job_id, workstation_id)


def handle_workstation_ready():

    return 1


def handle_workstation_starvation():

    return 1


def handle_workstation_congestion():

    return 1


def load_test_settings():   ### Load 3 jobs, in a simple 1-1-1 prod.line.
    create_workstations(3, [10, 25, 15], [0.01, 0.01, 0.01])
    create_jobs(1, [1, 1, 1])
    create_source("Job", workstation_dict.workstations[1], 0, "None", 0, 0)
    return 0


def time_for_vacancy(routing_phase):
    
    return 0


def job_has_more_steps_in_routing(job_id):
    if job_dict.get_job_routing(job_id) < len(prod_line):
        return True
    else:
        print(f"Job does NOT have anymore steps...")
        return False


def calculate_processing_time(job_id, workstation_id):
    """
    Job mean and true process times are vectors with same dimension as routing vector.
    """
    job = job_dict.get_job(job_id)
    current_routing = job.location
    workstation = workstation_dict.get_workstation(workstation_id)
    true_processing_time = job.true_processing_time * workstation.true_capacity
    #print(f"Process will take: {true_processing_time} time. Job: {job.true_processing_time} WS: {workstation.true_capacity}")
    return true_processing_time


def allocate_job_to_workstation(job_id, new_workstation_id, location_new):
    job = job_dict.get_job(job_id)
    workstation = workstation_dict.get_workstation(new_workstation_id)
    job.location = location_new
    workstation.job = job
    print(f"Workstation {new_workstation_id} at location {workstation.location} has a new job: {workstation.job.id}")
    return location_new