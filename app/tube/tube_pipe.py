# =================xGLOBAL_IMPORTS
import sys
import os
import json
import datetime
import re
import logging
import typing
import typing_extensions
import subprocess
import fcntl
import select
# ==================xSUBMODULE_IMPORTS


import os
import requests
import signal
import select
import requests

class TextStats:
    def __init__(self):
        # ... (Your TextStats implementation goes here)
        pass

    # ...


class UFX:
    def __init__(self, fd=None, inode=0, pid=os.getpid()):
        self.fd = fd
        self.inode = inode 
        self.pid = pid
        # ... (Other initialization code for UFX)

    # ...

    def read(self, length):
        return os.read(self.fd, length)
  
    def write(self, data):  
        return os.write(self.fd, data)

# Example usage of TextStats and UFX
if __name__ == "__main__":
    # Usage of TextStats
    stats = TextStats()
    text = "Your long string of .md files..."  # Stream of ASCII characters
    for char in text:
        stats.process_character(char)
    print(stats.quantities)

    # Usage of UFX
    fs = UFX(fd=open('file.txt'))
    print(fs.inode)  # prints inode of opened file
    print(fs.pid)    # pid of current process

    fs.write(b'hello')  # Writing bytes data to the file



import os
import requests
import signal
import select
import requests

class TextStats:
    # ... (Your TextStats implementation here)
    pass

class UFX:
    def __init__(self, fd=None, inode=0, pid=os.getpid()):
        self.fd = fd
        self.inode = inode
        self.pid = pid
        # ... (Other methods and properties here)
        pass

    @property
    def inode(self):
        if not self._inode:
            self._inode = os.fstat(self.fd).st_ino
        return self._inode

    @inode.setter
    def inode(self, inode):
        self._inode = inode

    @property
    def pid(self):
        return self._pid

    @pid.setter
    def pid(self, pid):
        self._pid = pid

    def read(self, length):
        return os.read(self.fd, length)

    def write(self, data):
        return os.write(self.fd, data)

# Usage example:
if __name__ == "__main__":
    # Example usage of TextStats
    stats = TextStats()
    text = "Your long string of .md files..."  # Stream of ASCII characters
    for char in text:
        stats.process_character(char)
    print(stats.quantities)

    # Example usage of UFX
    fs = UFX(fd=open('file.txt'))
    print(fs.inode)  # prints inode of opened file
    print(fs.pid)  # pid of current process

    fs.write(b'hello')
