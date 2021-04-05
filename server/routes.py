import flask, requests, os, sys, subprocess
from flask import Flask, request, jsonify

from Server import Server
from RequestValidator import RequestValidator

work_queue = {}
available_workers = {}
requests = {}

server = Server()
validator = RequestValidator()

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    valid_request, validation_message = validator.validate_request(request)
    if (valid_request):
        json = request.get_json()
        result = server.calculate(json['n'], json['x'])
        return jsonify({'result' : result })
    else:
        return validation_message, 400


if __name__ == "__main__":

    portNum = 5000
    app.run(debug=True, port=portNum)
    
    


