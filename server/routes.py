import flask, requests, os, sys, subprocess

from Server import Server
from flask import Flask, request, jsonify

work_queue = {}
available_workers = {}
requests = {}

server = Server()

app = Flask(__name__)

@app.route('/calculate')
def calculate():
    server.get_available_workers
    return "Pi is 3.14"

if __name__ == "__main__":

    portNum = 5000
    app.run(debug=True, port=portNum)
    
    


