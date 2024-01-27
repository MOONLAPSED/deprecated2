#! /usr/bin/env python3
# /src/ufx.py - define the ABCs for the UnixFilesystem and its interfaces and methods as well as core dataclasses.
from abc import ABCMeta, abstractmethod
import os

class SerializationInterface(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self):
        pass
    
    @abstractmethod
    def deserialize(self):
        pass

class Element(metaclass=ABCMeta):
    path: str = None

    @abstractmethod
    def _isimmutable(self):
        pass

class Entity(Element):
    serial_model: SerializationInterface = None
    
    @abstractmethod
    def get_stat(self):
        pass

class UnixFilesystem(Entity):
    def get_stat(self):
        return os.stat(self.path)
        
class SerialObject:
    @staticmethod
    def boolgenerator(obj):
        yield obj._isimmutable()
        #...
        
from collections.abc import Sequence

class ElementCollection(Sequence):
    def __getitem__(self, index):
        return self.elements[index]
    
    def __len__(self):
        return len(self.elements)