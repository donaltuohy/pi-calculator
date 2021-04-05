import requests
import logging

logging.basicConfig(level=logging.INFO)

class WorkerClient:

    def __init__(self, config):
        self.address = config['address']
        self.port = config['port']

    def get_base_url(self):
        base_url = self.address + ":" +  str(self.port)
        return base_url

    def get_url(self, uri):
        return self.get_base_url() + uri

    def ping(self):
        try:
            response = requests.get(self.get_url("/ping"))
            return response.status_code == 200
        except Exception as exception:
            logging.error("[Worker - " + self.get_base_url() + "] Error pinging worker: " + str(exception) )
            return False

    def calculate(self, start, end):
        logging.info("[Worker - " + self.get_base_url() + "] Sending request to calculate from " + str(start) + " to " + str(end))
        # body = "" #build json here to send to worker
        # response = requests.post(self.getUrl("/calculate"))
        return 0
