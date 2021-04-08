import requests
import logging
from flask import jsonify

logging.basicConfig(level=logging.INFO)

class WorkerClient:

    # Initialise WorkerClient class with given config
    def __init__(self, config):
        self.address = config['address']
        self.port = config['port']

    # Build base url for this worker
    # return type: String 
    def get_base_url(self):
        base_url = self.address + ":" +  str(self.port)
        return base_url

    # Builds worker url with given uri
    # param 1: uri - uri to append to the base url
    # return type: String
    def get_url(self, uri):
        return self.get_base_url() + uri

    # Send request to worker at /ping to decide if the worker is healthy or not
    # return type: Boolean
    def ping(self):
        try:
            response = requests.get(self.get_url("/ping"))
            return response.status_code == 200
        except Exception as exception:
            logging.error("[Worker - " + self.get_base_url() + "] Error pinging worker: " + str(exception))
            return False

    # Send request to worker at /calculate to calculate pi
    # param 1: work - range of numbers for the worker to calculate pi over
    # param 2: precision - Related to n (number of decimal places of pi). Needs to calculate with the precision of n.
    # return type: String (string to ensure decimal places are kept)
    def calculate(self, work, precision):
        logging.info("[Worker - " + self.get_base_url() + "] Sending request to calculate pi. " + str(len(work)) + " cycles designated. From " + str(work[0]) + " to " + str(work[len(work) - 1]))
        
        json_body = {
            'start': work[0],
            'end': work[len(work) - 1],
            'precision': precision
            }

        response = requests.post(self.get_url("/calculate"), json=json_body)
        result = response.json()["result"]
        return result