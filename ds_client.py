# Jaziel Herrera
# jazielh@uci.edu
# 78328456

# ds_client.py

import socket
import json
import time

def send(server: str, port: int, username: str, password: str, message: str, bio: str = None) -> dict:
    """
    The send function joins a DS server and sends a message, bio, or both.
    
    :param server: The IP address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    :return: Dictionary with response data, including the token if successful.
    """
    try:
        print(f"Connecting to {server}:{port} with username: {username}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(10)  # timeout for the connection
            client_socket.connect((server, port))
            print("Connection established.")
            
            join_msg = json.dumps({"join": {"username": username, "password": password, "token": ""}})
            print(f"Sending join message: {join_msg}")
            response = _send_and_receive(client_socket, join_msg)
            print(f"Join response: {response}")
            token = response.get("response", {}).get("token")
            
            if not token:
                print("Failed to retrieve token.")
                return {"response": {"type": "error", "message": "Failed to retrieve token"}}
            
            if message:
                post_msg = json.dumps({"token": token, "post": {"entry": message, "timestamp": str(time.time())}})
                print(f"Sending post message: {post_msg}")
                response = _send_and_receive(client_socket, post_msg)
                print(f"Post response: {response}")
                if response.get("response", {}).get("type") != "ok":
                    print("Failed to post message.")
                    return {"response": {"type": "error", "message": "Failed to post message"}}
            
            if bio:
                bio_msg = json.dumps({"token": token, "bio": {"entry": bio, "timestamp": str(time.time())}})
                print(f"Sending bio message: {bio_msg}")
                response = _send_and_receive(client_socket, bio_msg)
                print(f"Bio response: {response}")
                if response.get("response", {}).get("type") != "ok":
                    print("Failed to post bio.")
                    return {"response": {"type": "error", "message": "Failed to post bio"}}
            
            print("Operation successful.")
            return {"response": {"type": "ok", "token": token}}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"response": {"type": "error", "message": str(e)}}


def _send_and_receive(client_socket: socket.socket, message: str) -> dict:
    try:
        client_socket.sendall((message + '\r\n').encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        return json.loads(response)
    except Exception as e:
        print(f"Error during send/receive: {e}")
        return {"response": {"type": "error", "message": str(e)}}
