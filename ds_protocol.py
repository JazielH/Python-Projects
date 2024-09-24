# Jaziel Herrera
# jazielh@uci.edu
# 78328456
# ds_protocol.py

import json
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['response_type', 'message', 'token'])

def extract_json(json_msg: str) -> DataTuple:
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

def send_direct_message(token: str, message: str, recipient: str, timestamp: float) -> str:
    message_dict = {
        "token": token,
        "directmessage": {
            "entry": message,
            "recipient": recipient,
            "timestamp": int(timestamp)  # Convert timestamp to integer
        }
    }
    return json.dumps(message_dict)

def get_messages(token: str, message_type: str) -> str:
    message_dict = {
        "token": token,
        "directmessage": message_type
    }
    return json.dumps(message_dict)

def process_response(json_response: str) -> list:
    try:
        response_obj = json.loads(json_response)
        return response_obj.get('response', {}).get('messages', [])
    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return []