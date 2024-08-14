###
###
### Data structures representing queues, entities, etc.
### Other core modules (e.g., statistics collection)
###
###

import heapq
import numpy as np

prod_line = [1,1,1]
prod_line_var = [0,0,0]
prod_line_cv = [0.66, 1, 1.33]

### def __init__(self, id, location, true_capacity, mean_capacity, cv, std, status, wip, time_passed):
class WorkstationManager:
    def __init__(self):
        self.workstations = {}
        self.workstation_id_counter = 1

    def add_workstation(self, location, true_capacity, mean_capacity, cv, std, status, wip, time_passed):
        workstation = Workstation(self.workstation_id_counter, location, true_capacity, mean_capacity, cv, std, status, wip, time_passed)
        workstation.calculate_workstation_std()
        self.workstations[self.workstation_id_counter] = workstation
        self.workstation_id_counter += 1

    def get_workstation(self, id):
        workstation = self.workstations.get(id)
        if workstation:
            return workstation
        else:
            print(f"Error (get_workstation): Workstation with ID {id} not found!")
            return None
    
    def update_workstation(self, id):
        print("Unfinished\r\n")
        return 0
    
    def remove_workstation(self, id):
        print("Unfinished\r\n")
        return 0
    
    def search_vacant_workstation_in_routing(self, location):
        for workstation in self.workstations.values():
            if workstation.location == location and workstation.status == 'Vacant':
                return True
        return False

### def __init__(self, id, routing, true_process_time, mean_process_time, status, cv, std):
class JobManager:
    def __init__(self):
        self.jobs = {}
        self.job_id_counter = 1

    def add_job(self, location, true_process_time, mean_process_time, status, cv, std):
        job = Job(self.job_id_counter, location, true_process_time, mean_process_time, status, cv, std)
        job.calculate_job_std()
        self.jobs[self.job_id_counter] = job
        self.job_id_counter += 1

    def get_job(self, id):
        return self.jobs.get(id)
    
    def get_job_routing(self, id):
        job = self.jobs.get(id)
        if job:
            return job.location
        else:
            print(f"Error (get job): Job with ID {id} not found!")
            return None
    
    def update_job(self, id):
        print("Unfinished\r\n")
        return 0
    
    def remove_job(self, id):
        print("Unfinished\r\n")
        return 0

class EventManager:
    def __init__(self):
        self.events = [] # converted into heap later...
        self.event_id_counter = 1
    
    def add_event(self, time, event_type, job_id=None, workstation_id=None):
        """
        Adds an event to the event queue.

        Args:
            time: The scheduled time of the event.
            event_type: The type of event (e.g., "job_arrival," "job_completion").
            job_id: The ID of the job associated with the event (if applicable).
            workstation_id: The ID of the workstation associated with the event (if applicable).
        """

        event = (self.event_id_counter, time, event_type, job_id, workstation_id)
        self.event_id_counter += 1
        print(f"Added event: {event_type} at time t: {time}.")
        heapq.heappush(self.events, event)
        

    def get_next_event(self):
        """
        Gets the next event from the event queue.

        Returns:
            The next event as a tuple (time, event_type, job_id, workstation_id), 
            or None if the queue is empty
        """
        if self.events:
            return heapq.heappop(self.events)
        else:
            return None

    def update_event(self, id, type, target_time):
        return 0
    
    def remove_event(self, id):
        return 0
    
class SourceManager:
    def __init__(self):
        self.sources = []
        self.source_id_counter = 0

    def add_source(self, id, source_type, source_parameters):
        return 1


"""
Workstation capacity is represented here are as a multiplier and selected from a probability distribution function.

"""

class Workstation:
    def __init__(self, id, location, true_capacity, mean_capacity, cv, std, status, wip, time_passed):
        self.id = id
        self.location = location
        self.true_capacity = true_capacity
        self.mean_capacity = mean_capacity
        self.cv = cv
        self.std = std
        self.status = "Vacant"
        self.wip = wip
        self.time_passed = time_passed


    def calculate_workstation_std(self):
        self.std = self.mean_capacity * self.cv
        self.true_capacity = np.random.normal(self.mean_capacity, self.std, 1)


class Job:
    def __init__(self, id, location, true_processing_time, mean_processing_time, status, cv, std):
        self.id = id
        self.location = location
        self.true_processing_time = true_processing_time
        self.mean_processing_time = mean_processing_time
        self.status = status
        self.cv = cv
        self.std = std

    def calculate_job_std(self):
        self.std = self.mean_processing_time * self.cv
        self.true_process_time = np.random.normal(self.mean_processing_time, self.std, 1)

### Job.status = {"Pending", "WIP", "Idle", "Complete"}
### Workstation.status = {"Starvation", "Congestion", "Processing"}
### Event.status = {"job_arrived", "job_processing", "job_waiting", 
###                 "job_phase_ready", "job_completed", "workstation_ready", 
###                 "workstation_starvation", "workstation_congestion"}

class Event:
    def __init__(self, id, type, status):
        self.id = id
        self.type = type
        self.status = status

    def update_event_time(self, id, new_time):
        return 0
    
    def update_event_type(self, id, new_type):
        return 0
    

class Source:
    def __init__(self, id, source_type, generation_parameters):
        self.id = id
        self.source_type = source_type
        self.generation_parameters = generation_parameters

    def generate_entity(self):
        if self.source_type == "job":
            job = 1
            return job
        elif self.source_type == "material":
            material = 1
            return material