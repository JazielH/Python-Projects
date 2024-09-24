# Jaziel Herrera
# jazielh@uci.edu
# test_ds_messenger.py

import ds_messenger

def test_send():
    messenger = ds_messenger.DirectMessenger(dsserver='168.235.86.101', username='luffy', password='nami')
    assert messenger.send('Hello World!', 'yur') == True
    print("test_send passed.")

def test_retrieve_new():
    messenger = ds_messenger.DirectMessenger(dsserver='168.235.86.101', username='luffy', password='nami')
    messages = messenger.retrieve_new()
    assert isinstance(messages, list)
    print("test_retrieve_new passed.")

def test_retrieve_all():
    messenger = ds_messenger.DirectMessenger(dsserver='168.235.86.101', username='luffy', password='nami')
    messages = messenger.retrieve_all()
    assert isinstance(messages, list)
    print("test_retrieve_all passed.")

if __name__ == "__main__":
    test_send()
    test_retrieve_new()
    test_retrieve_all()
