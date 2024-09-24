# Jaziel Herrera
# jazielh@uci.edu
# 78328456
# test_ds_protocol.py

import ds_protocol

def test_send_direct_message():
    token = "user_token"
    message = "Hello World!"
    recipient = "ohhiimark"
    timestamp = 1603167689.3928561
    expected_output = '{"token": "user_token", "directmessage": {"entry": "Hello World!", "recipient": "ohhiimark", "timestamp": 1603167689}}'
    
    actual_output = ds_protocol.send_direct_message(token, message, recipient, timestamp)
    assert actual_output == expected_output, f"Expected: {expected_output}, but got: {actual_output}"
    print("test_send_direct_message passed.")

def test_get_messages():
    token = "user_token"
    expected_output_new = '{"token": "user_token", "directmessage": "new"}'
    expected_output_all = '{"token": "user_token", "directmessage": "all"}'
    
    assert ds_protocol.get_messages(token, "new") == expected_output_new
    assert ds_protocol.get_messages(token, "all") == expected_output_all
    print("test_get_messages passed.")

def test_process_response():
    json_response = '{"response": {"type": "ok", "messages": [{"message": "Hello User 1!", "from": "markb", "timestamp": 1603167689.3928561}, {"message": "Bzzzzz", "from": "thebeemoviescript", "timestamp": 1603167689.3928561}]}}'
    expected_output = [
        {"message": "Hello User 1!", "from": "markb", "timestamp": 1603167689.3928561},
        {"message": "Bzzzzz", "from": "thebeemoviescript", "timestamp": 1603167689.3928561}
    ]
    
    assert ds_protocol.process_response(json_response) == expected_output
    print("test_process_response passed.")

if __name__ == "__main__":
    test_send_direct_message()
    test_get_messages()
    test_process_response()
