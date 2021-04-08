from flask import request, jsonify
from cerberus import Validator

class RequestValidator:
    
    # Validate the post request with different validations.
    # param 1: request - Request to validate.
    # return type: Tuple of type (Boolean, String) - Whether the request is valid and an accompanying message.
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

    # Validate the json meets the defined schema.
    # param 1: json - Json to validate.
    # return type: Tuple of type (Boolean, String) - Whether the json is valid and an accompanying message.
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

    # Validate the input of the json is correct.
    # param 1: n - The number of decimal places - can't be zero.
    # param 2: x - The number of cycles - can't be zero.
    # return type: Tuple of type (Boolean, String) - Whether the input is valid and an accompanying message.
    def valid_input(self, n, x):
        if (x == 0 or n == 0):
            return (False, jsonify({'message' : "Invalid values for n and x. Both must be greater than 0 " }))
        else:
            return (True, "")

