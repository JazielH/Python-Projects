# Jaziel Herrera
# jazielh@uci.edu
# 78328456
# Profile.py

import json
import time
from pathlib import Path

class DsuFileError(Exception):
    pass

class DsuProfileError(Exception):
    pass

class Post(dict):
    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry
    
    def set_time(self, time: float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)

class DirectMessage:
    def __init__(self, sender=None, recipient=None, message=None, timestamp=None):
        self.sender = sender
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp

class Profile:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self._posts = []
        self.friends = []
        self.messages = []
        self.direct_messenger = None

    def add_post(self, post):
        self._posts.append(post)

    def del_post(self, index):
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False
        
    def get_posts(self):
        return self._posts

    def add_friend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)

    def add_message(self, message):
        self.messages.append(message)

    def save_profile(self, path):
        p = Path(path)
        if p.suffix == '.dsu':
            try:
                with open(p, 'w') as f:
                    json.dump(self.__dict__, f, default=lambda o: o.__dict__, indent=4)
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path):
        p = Path(path)
        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r') as f:
                    obj = json.load(f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.bio = obj['bio']
                    self._posts = [Post(post_obj['entry'], post_obj['timestamp']) for post_obj in obj['_posts']]
                    self.friends = obj.get('friends', [])
                    self.messages = [DirectMessage(msg['sender'], msg['recipient'], msg['message'], msg['timestamp']) for msg in obj['messages']]
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()