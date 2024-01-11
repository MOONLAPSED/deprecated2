import os
import sqlite3
from datetime import datetime

# Define the abstract base class
class Entity:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

# Define the concrete subclasses
class Attribute(Entity):
    def __init__(self, name, type):
        super().__init__(name, "Attribute of {}".format(name))
        self.type = type

    def __str__(self):
        return "{}: {}".format(self.name, self.type)

class Description(Entity):
    def __init__(self, name, description):
        super().__init__(name, description)

    def __str__(self):
        return self.name

# Define the specific data types as subclasses of Attribute
class TEXT(Attribute):
    def __init__(self, name):
        super().__init__(name, "TEXT")

    def __str__(self):
        return "{}: TEXT".format(self.name)

class INTEGER(Attribute):
    def __init__(self, name):
        super().__init__(name, "INTEGER")

    def __str__(self):
        return "{}: INTEGER".format(self.name)

class REAL(Attribute):
    def __init__(self, name):
        super().__init__(name, "REAL")

    def __str__(self):
        return "{}: REAL".format(self.name)

class BLOB(Attribute):
    def __init__(self, name):
        super().__init__(name, "BLOB")

    def __str__(self):
        return "{}: BLOB".format(self.name)

class VARCHAR(Attribute):
    def __init__(self, name, length):
        super().__init__(name, "VARCHAR({})".format(length))
        self.length = length

    def __str__(self):
        return "{}: VARCHAR({})".format(self.name, self.length)

class UnixFilesystem(Description):
    def __init__(self, inode, pathname, filetype, permissions, owner, group_id, PID, unit_file, unit_file_addr, size, mtime, atime):
        super().__init__(inode, "Unix filesystem")
        self.pathname = pathname
        self.filetype = filetype
        self.permissions = permissions
        self.owner = owner
        self.group_id = group_id
        self.size = size
        self.PID = PID
        self.unit_file = unit_file
        self.unit_file_addr = unit_file_addr
        self.mtime = mtime
        self.atime = atime

    def __str__(self):
        return "{}: {}".format(self.inode, self.pathname)
