from flask import request, jsonify
from cerberus import Validator

class RequestValidator:
        
    def validate_request(self, request):
        valid_json, invalid_json_message = self.valid_json(request.get_json())
        if (valid_json):
            json = request.get_json()
            valid_input, inalid_input_message = self.valid_input(json['n'], json['x'])
            if(valid_input):
                return (True, "Valid Request")
            else:
                return (False, inalid_input_message)
        else:
            return (False, invalid_json_message)

    def valid_json(self, json):
        schema = {
            'n': {'type': 'integer', 'required': True},
            'x': {'type': 'integer', 'required': True}
        }
        v = Validator(schema)
        
        if (v.validate(json)):
            return (True, "") 
        else:
            return (False, jsonify({'message' : "Invalid json", 'schema' : schema }))

    def valid_input(self, n, x):
        if (x > n or x == 0 or n == 0):
            return (False, jsonify({'message' : "Invalid values for n and x. n must be >= x and both must be greater than 0 " }))
        else:
            return (True, "")

