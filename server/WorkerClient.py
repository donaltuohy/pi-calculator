import requests

class WorkerClient:

    def __init__(self, config):
        self.address = config['address']
        self.port = config['port']

    def get_base_url(self):
        return (self.address + ":" +  str(self.port))

    def get_url(self, uri):
        return self.get_base_url() + uri

    def ping(self):
        response = requests.get(self.get_url("/ping"))
        print("\n")
        print(self.get_base_url() + str(response.status))
        print("\n")
        return True

    def calculate(self, start, end):
        response = requests.post(self.getUrl("/calculate"), json=shaDict)
        return response
