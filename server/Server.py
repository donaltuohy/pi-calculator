import config
import logging
from WorkerClient import WorkerClient

logging.basicConfig(level=logging.INFO)

class Server:

    def __init__(self):
        logging.info("Initialising server.")
        print(self.calculate(20, 3))

    def calculate(self, n, cycles):
        available_workers = self.get_available_workers()
        logging.info("Distributing work amongst " + str(len(available_workers)) + " workers")
        result = self.distribute_work(self.split_up_work(n, cycles), self.get_available_workers())
        
        return result

    def split_up_work(self, n, cycles):
        numbers_per_cycle = n / cycles
        list = range(n)
        result = []
        for i in range(0, n, numbers_per_cycle):
            result.append(list[i:i + numbers_per_cycle])
        return result

    # Using round robin to send the work to each available worker
    def distribute_work(self, pieces_of_work, available_workers):
        result = []
        for i, work in enumerate(pieces_of_work, start=0):
            worker_id = i % (len(available_workers))
            worker = available_workers[worker_id]
            worker_result = worker.calculate(work[0], work[len(work) - 1])
            result.append(worker_result)
        return result

    def get_available_workers(self):
        available_workers = []
        
        for worker_config in config.workers:    
            worker = WorkerClient(worker_config)
           
            if(worker.ping()):
                logging.info("[Worker - " + str(worker.get_base_url()) + "]" + ": PING successful, marking healthy")
                # Use the base url as the id for the worker - makes sure it's unique
                available_workers.append(worker)
            else:
                logging.info("[Worker - " + worker.get_base_url() + "]" + ": PING unsuccessful, marking unhealthy.")
        
        return available_workers

    