# Jaziel Herrera
# jazielh@uci.edu
# 78328456
# ds_messenger.py

import ds_protocol
import ds_client
import json
import time
import socket

class DirectMessage:
    def __init__(self, sender=None, recipient=None, message=None, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.message = str(message)  # treat as a string not number 
        self.timestamp = timestamp

    def __repr__(self):
        return f"DirectMessage(sender={self.sender}, recipient={self.recipient}, message={self.message}, timestamp={self.timestamp})"

class DirectMessenger:
    def __init__(self, dsserver: str = None, username: str = None, password: str = None):
        self.token = None
        self.dsserver = dsserver
        self.username = username
        self.password = password
    
    def send(self, message: str, recipient: str) -> bool:
        if not self.token:
            self.token = self._join_server()
        
        if self.token:
            timestamp = int(time.time())
            message_json = ds_protocol.send_direct_message(self.token, message, recipient, timestamp)
            print(f"Sending message: {message_json}")  #debugging
            response = self._send_message_to_server(message_json)
            print(f"Server response: {response}")  #debugging
            return response.get('response', {}).get('type') == 'ok'
        return False
    
    def retrieve_new(self) -> list:
        if not self.token:
            self.token = self._join_server()
        
        if self.token:
            message_json = ds_protocol.get_messages(self.token, "new")
            print(f"Retrieving new messages with request: {message_json}")  #debugging
            response = self._send_message_to_server(message_json)
            print(f"Received new messages: {response}")  #debugging
            return self._process_messages(response)
        return []
    
    def retrieve_all(self) -> list:
        if not self.token:
            self.token = self._join_server()
        
        if self.token:
            message_json = ds_protocol.get_messages(self.token, "all")
            print(f"Retrieving all messages with request: {message_json}")  #debugging
            response = self._send_message_to_server(message_json)
            print(f"Received all messages: {response}")  #debugging
            return self._process_messages(response)
        return []

    def _join_server(self) -> str:
        response = ds_client.send(self.dsserver, 3021, self.username, self.password, "", "")
        print(f"Join server response: {response}")  #debugging
        return response.get('response', {}).get('token')

    def _send_message_to_server(self, message_json: str) -> dict:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.settimeout(10)
                client_socket.connect((self.dsserver, 3021))
                return ds_client._send_and_receive(client_socket, message_json)
        except Exception as e:
            print(f"Error sending message to server: {e}")
            return {"response": {"type": "error", "message": str(e)}}

    def _process_messages(self, response: dict) -> list:
        messages = ds_protocol.process_response(json.dumps(response))
        processed_messages = [DirectMessage(msg['from'], self.username, msg['message'], msg['timestamp']) for msg in messages]
        print(f"Processed messages: {processed_messages}")  #debugging
        return processed_messages
