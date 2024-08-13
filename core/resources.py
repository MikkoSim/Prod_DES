###
###
### Data structures representing queues, entities, etc.
### Other core modules (e.g., statistics collection)
###
###

import numpy as np

prod_line = [1,1,1]
prod_line_var = [0,0,0]
prod_line_cv = [0.66, 1, 1.33]


class WorkstationManager:
    def __init__(self):
        self.workstations = {}

    def add_workstation(self, workstation):
        self.workstations[workstation.id] = workstation

    def get_workstation(self, id):
        return self.workstations.get(id)
    
    def update_workstation(self, id):
        print("Unfinished\r\n")
        return 0
    
    def remove_workstation(self, id):
        print("Unfinished\r\n")
        return 0



class JobManager:
    def __init__(self):
        self.jobs = {}

    def add_workstation(self, job):
        self.jobs[job.id] = job

    def get_job(self, id):
        return self.jobs.get(id)
    
    def update_workstation(self, id):
        print("Unfinished\r\n")
        return 0
    
    def remove_workstation(self, id):
        print("Unfinished\r\n")
        return 0

class EventManager:
    def __init__(self, id):
        self.id = 0
    
    def add_event(self, id, type):
        return 0
    
    def update_event(self, id, type):
        return 0
    
    def remove_event(self, id):
        return 0
    


class Workstation:
    def __init__(self, id, location, true_capacity, mean_capacity, cv, std, status, wip, time_passed):
        self.id = 0
        self.location = 0
        self.true_capacity = 0
        self.mean_capacity = 0
        self.cv = 0
        self.std = 0
        self.status = "Vacant"
        self.wip = 0
        self.time_passed = 0

    def calculate_workstation_std(self, mean_capacity):
        self.std = self.mean_capacity * self.cv
        self.true_capacity = np.random.normal(mean_capacity, self.std, 1)


class Job:
    def __init__(self, id, location, true_process_time, mean_process_time, status, cv, std):
        self.id = 0
        self.location = 0
        self.true_process_time = [0,0,0]
        self.mean_process_time = [0,0,0]
        self.status = "Pending"
        self.cv = 0
        self.std = [0,0,0]

    def calculate_job_std(self):
        for i in range(len(self.true_process_time)):
            self.std[i] = self.mean_process_time[i] * self.cv
            self.true_process_time[i] = np.random.normal(self.mean_process_time[i], self.std[i], 1)

class Event:
    def __init__(self, id):
        self.id = 0

    def update_event_time(self, id, new_time):
        return 0