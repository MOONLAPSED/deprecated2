#! /usr/bin/env python3
# /src/ufx.py - define the ABCs for the UnixFilesystem and its interfaces and methods as well as core dataclasses.
from abc import *
import os

from collections import deque



class SerializationInterface(ABC):
    """serialize/de-serialize refers to pickle if not otherwise specified."""
    abstract_methods = ['serialize', 'deserialize', 'json', 'to_json', 'path', 'to_Path', 'is_mutable', 'from_sock', 'to_sock', 'from_pipe', 'to_pipe', 'yaml', 'from_env', 'to_env']
#    for method in abstract_methods:
#        exec(f'@abstractmethod\ndef {method}(self): pass')

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self):
        pass

class JsonSerializer(SerializationInterface):

    def serialize(self):
        return f"Serialized to JSON"

    def deserialize(self):
        return f"Deserialized from JSON:\n{os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app.log')}"

# Create an instance of JsonSerializer directly
serializer = JsonSerializer()
print(serializer.serialize())