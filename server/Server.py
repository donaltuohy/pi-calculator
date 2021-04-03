import config
from WorkerClient import WorkerClient

class Server:

    def __init__(self):
        print("Initialising server")
        self.workers = self.get_available_workers()
        print("Available workers: " + str(self.workers))


    def distribute_work(self, n, cycles):
        print("Hello - got a server method")
        return 0 

    def get_available_workers(self):
        available_workers = {}
        
        for worker_config in config.workers:    
            worker = WorkerClient(worker_config)
           
            if(worker.ping()):
                print("[ Worker - " + str(worker.get_base_url()) + "]" + ": PING successful, marking healthy")
                # Use the base url as the id for the worker - makes sure it's unique
                available_workers[worker.get_base_url] = worker
            else:
                print("[ Worker - " + worker.get_base_url + "]" + ": PING unsuccessful, Marking unhealthy.")
        
        return available_workers

    