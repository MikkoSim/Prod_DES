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


"""
DICTIONARIES

"""


"""
WorkstationManager is a dictionary, stores Workstation objects.

"""


### def __init__(self, id, location, true_capacity, mean_capacity, cv, std, status, wip, time_passed):
class WorkstationManager:
    def __init__(self):
        self.workstations = {}
        self.workstation_id_counter = 1

    def add_workstation(self, location, true_capacity, mean_capacity, cv, std, status, wip, time_when_freed):
        workstation = Workstation(self.workstation_id_counter, location, true_capacity, mean_capacity, cv, std, status, wip, time_when_freed)
        workstation.calculate_workstation_std()
        self.workstations[self.workstation_id_counter] = workstation
        self.workstation_id_counter += 1

    def get_workstation(self, id):
        if id == 0:
            return None
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
            if workstation.location == location and workstation.status == "Vacant":
                return True
        return False


"""
JobManager is a dictionary, stores Job objects.

"""


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


"""
EventManager is a dictionary, stores Event objects.

"""


class EventManager:
    def __init__(self):
        self.events = [] # converted into heap later...
        self.event_id_counter = 1
        self.event_log = []
    
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
        heapq.heappush(self.events, event)
        

    def get_next_event(self):
        """
        Gets the next event from the event queue.

        Returns:
            The next event as a tuple (time, event_type, job_id, workstation_id), 
            or None if the queue is empty
        """
        if self.events:
            event = heapq.heappop(self.events)
            self.event_log.append(event)
            return event
        else:
            return None

    def update_event(self, id, type, target_time):
        return 0
    
    def remove_event(self, id):
        return 0


"""
SourceManager is a dictionary, stores Source objects.

"""


class SourceManager:
    def __init__(self):
        self.sources = {}
        self.source_id_counter = 0

    def add_source(self, source_type, target_object, num_of_elements, distr_func, mean, sigma):
        source = Source(self.source_id_counter, source_type, target_object, num_of_elements, distr_func, mean, sigma)
        self.sources[self.source_id_counter] = source
        self.source_id_counter += 1


"""
RoutingNodeManager is a dictionary, stores RoutingNode objects.

"""


class RoutingNodeManager:
    def __init__(self):
        self.stages = {}
        self.head_node = None


"""
SERVER OBJECTS

"""


"""
Base class Server.

"""


class Server:
    def __init__(self, id):
        self.id = id


"""
Workstation capacity is represented here are as a multiplier and selected from a probability distribution function.

Args:
    id:

    location:

    bom:

    true_capacity:

    mean_capacity:

    cv:

    std:

    status:

    job:

    time_when_freed:

"""


class Workstation(Server):
    def __init__(self, id = -1, location = -1, true_capacity = 0, mean_capacity = 0, cv = 0, std = 0, status = "Vacant", job = None, time_when_freed = 0):
        self.id = id
        self.location = location
        self.true_capacity = true_capacity
        self.mean_capacity = mean_capacity
        self.cv = cv
        self.std = std
        self.status = status
        self.job = job
        self.time_when_freed = time_when_freed


    def calculate_workstation_std(self):
        self.std = self.mean_capacity * self.cv
        self.true_capacity = abs(np.random.normal(self.mean_capacity, self.std, 1))


"""
ENTITY OBJECTS

"""


"""
Base class Entity

"""


class Entity:
    def __init__(self, id):
        self.id = id


"""
Job

Args:
    id:

    location:

    bom:

    true_capacity:

    mean_capacity:

    cv:

    std:

    status:

    job:

    time_when_freed:

"""


class Job(Entity):
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
        self.true_processing_time = abs(np.random.normal(self.mean_processing_time, self.std, 1))


"""
Worker

Args:
    id:

    location:

    status:

    job:

"""


class Worker(Entity):
    def __init__(self, id):
        self.id = id


"""
Material.

Args:
    id:

    location:

    bom:

    status:

    job:

"""


class Material(Entity):
    def __init__(self, id):
        self.id = id



### Job.status = {"Pending", "WIP", "Idle", "Complete"}
### Workstation.status = {"Vacant", "Received", "Processing", "Complete"}
### Event.status = {"job_arrived", "job_processing", "job_waiting", 
###                 "job_phase_ready", "job_completed", "workstation_ready", 
###                 "workstation_starvation", "workstation_congestion"}


"""
ENVIRONMENT OBJECTS

"""


"""
RoutingNode

Args:

"""



class RoutingNode:
    def __init__(self, workstations, next_node=None):
        self.workstations = workstations
        self.next_node = next_node


"""
Source

Args:

Methods:


"""



class Source:
    def __init__(self, id, source_type, target_object, num_of_elements, distr_func, mean, sigma):
        self.id = id
        self.source_type = source_type
        self.target_object = target_object
        self.num_of_elements = num_of_elements
        self.distr_func = distr_func
        self.mean = mean
        self.sigma = sigma

    def generate_entity(self):
        if self.source_type == "job":
            job = 1
            return job
        elif self.source_type == "material":
            material = 1
            return material