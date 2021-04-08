#Python libraries
import flask, requests, os, sys, subprocess
from flask import Flask, request, jsonify

#Custom classes
from Server import Server
from RequestValidator import RequestValidator


server = Server()
validator = RequestValidator()

app = Flask(__name__)

# Accept post requests to /calculate and validate them before processing
@app.route('/calculate', methods=['POST'])
def calculate():
    valid_request, validation_message = validator.validate_request(request)
    if (valid_request):
        json = request.get_json()
        success, result = server.calculate(json['n'], json['x'])
        if(success):
            return result, 200
        else: 
            return result, 500
    else:
        return validation_message, 400


if __name__ == "__main__":

    portNum = 5000
    app.run(debug=True, port=portNum, host='0.0.0.0')
    
    


