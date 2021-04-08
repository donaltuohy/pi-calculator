import config
import logging
import time
import numpy as np
from decimal import Decimal, getcontext
from flask import Flask, request, jsonify
from multiprocessing import Manager
from threading import Thread

from WorkerClient import WorkerClient


logging.basicConfig(level=logging.INFO)

class Server:

    # Initialise Server class
    def __init__(self):
        logging.info("Initialising server.")

    # Take in parameters for calculating pi and designate work to workers
    # param 1: n - Number of digits of pi to calculate
    # param 2: cycles - Amount of cycles to use to converge on pi
    # return type: Tuple of type (Boolean, JsonString) - Returns whether if the method was a success and a message to go with the result.
    def calculate(self, n, cycles):
        getcontext().prec = n
        available_workers = self.get_available_workers()
        amount_of_available_workers = len(available_workers)

        if(amount_of_available_workers == 0):
            logging.error("No workers available")
            return (False, jsonify({'message' : "Internal Server Error - No workers available"}))  
        
        else:
            logging.info("Distributing work amongst " + str(len(available_workers)) + " workers")
            results = self.distribute_work(n, self.split_up_work(cycles, amount_of_available_workers), self.get_available_workers())
            final_result = self.handle_results(results)
            final_result_formatted = "{1:.{0}f}".format(n - 1, final_result)

            return (True, jsonify({'pi' : final_result_formatted}))

    # Splits up the work into chunks to be sent to each worker 
    # param 1: cycles - Amount of cycles to use to converge on pi - This is divided by the amount of available workers.
    # param 2: amount_of_available_workers - Used to decide how many chunks of work to create.
    # return type: Array of Array of Ints - Each array is for a worker
    def split_up_work(self, cycles, amount_of_available_workers):
        split_array = np.array_split(range(cycles), amount_of_available_workers)
        return split_array
        
    # Takes in the split up work and sends each worker their piece of work. Need to use threads so that each worker begins at the same time.
    # param 1: precision - Related to n (number of decimal places of pi). Needs to calculate with the precision of n.
    # param 2: pieces_of_work -  Array of arrays specifying the ranges that each worker should calculate pi over.
    # param 3: available_workers -  Array of available workers to be sent work.
    # return type: array of strings - Each workers approximation of pi for the work given. 
    def distribute_work(self, precision, pieces_of_work, available_workers):
        que = Manager().Queue()
        threads = []

        for i, work in enumerate(pieces_of_work, start=0):
            worker = available_workers[i]
            thread = Thread(target=self.thread_request, args=(que, worker, work, precision, 5))
            threads.append(thread)
            thread.start()
       
        for t in threads:
           t.join()
        
        result = []
        
        while not que.empty():
            result.append(que.get())
        
        return result
    
    # Method to be run in the thread. Sends request to worker and retries if there's a failure
    # param 1: queue - Global queue to store the results from the thread
    # param 2: worker -  Worker client to sent work to
    # param 3: work -  Array specifying the range that the worker should calculate pi over.
    # param 4: precision - Related to n (number of decimal places of pi). Needs to calculate with the precision of n.
    # param 5: max_tries -  Number of times to retry if the request fails.
    # return type: array of strings - Each workers approximation of pi for the work given. 
    def thread_request(self, q, worker, work, precision, max_tries):
        for i in range(max_tries):
            try:
                time.sleep(0.3) 
                result = worker.calculate(work, precision)
                q.put(result)
                break
            except Exception as exception:
                logging.error( "[ Worker" + worker.get_base_url() + "] - Could not send request to worker. Retrying. Exception: " + str(exception))
                continue
                
    # Handles array of results returned from workers. Sums them together.
    # param 1: results - Array of 
    # param 2: piece_of_work -  Array of arrays specifying the ranges that each worker should calculate pi over.
    # return type: array of results - Each workers approximation of pi for the work given. They are added together to give the final approximation
    def handle_results(self, results):
        sum = Decimal(0)
        for result in results:
            sum = sum + Decimal(result)
        return sum

    # Checks the health of each worker from the config.
    # return type: array of workers - Workers which are healthy and responded to a ping request 
    def get_available_workers(self):
        available_workers = []
        
        for worker_config in config.workers:
            # Create WorkerClient with the worker_config
            worker = WorkerClient(worker_config)
           
            if(worker.ping()):
                logging.info("[Worker - " + str(worker.get_base_url()) + "]" + ": PING successful, marking healthy")
                available_workers.append(worker)
            else:
                logging.info("[Worker - " + worker.get_base_url() + "]" + ": PING unsuccessful, marking unhealthy.")
        
        return available_workers
        

    