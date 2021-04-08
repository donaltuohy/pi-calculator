import flask, sys, os
import logging
from Worker import Worker
from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

worker = Worker()

# Accept get requests to /ping 
@app.route('/ping',  methods=['GET'])
def ping():
    return "pong", 200

# Accept post requests to /calculate
@app.route('/calculate',  methods=['POST'])
def calculate():
    try:
        body = request.get_json()
        result = worker.pi(body['start'], body['end'], body['precision'])
        formatted_result = "{1:.{0}f}".format(body['precision'] + 1, result)
        return jsonify({"result" : formatted_result}), 200
    except Exception as e:
        logging.error("Could not process request from main server. Exception: " + e)
        return jsonify({"exception" : str(e)}), 500

if __name__ == "__main__":
    
    PORT = int(os.getenv('PORT'))
    app.run(debug=True, port=PORT, host='0.0.0.0')
    
    