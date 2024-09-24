# Jaziel Herrera
# jazielh@uci.edu

# ds_protocol.py

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from JSON messages.
DataTuple = namedtuple('DataTuple', ['response_type', 'message', 'token'])

def extract_json(json_msg: str) -> DataTuple:
    """
    Call the json.loads function on a JSON string and convert it to a DataTuple object.
    
    :param json_msg: The JSON message as a string.
    :return: A DataTuple object with the extracted values.
    """
    try:
        json_obj = json.loads(json_msg)
        response = json_obj.get('response', {})
        response_type = response.get('type')
        message = response.get('message')
        token = response.get('token')
        return DataTuple(response_type, message, token)
    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return DataTuple(None, None, None)
