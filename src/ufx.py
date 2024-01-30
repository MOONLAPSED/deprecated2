#! /usr/bin/env python3
# /src/ufx.py - define the ABCs for the UnixFilesystem and its interfaces and methods as well as core dataclasses.
from abc import *
import os
import shutil

# Define the constant limits
limit = 10  # Arbitrary limit for iterations and permutations (loops, dfs, bfs, etc.)
llimit = 10 * 1000000  # 10 MB file size limit

def copy(src, dst):
    total_size = 0  # Variable to track the total size of copied files

    # Iterate over the source elements up to the specified limit
    for i, src_el in enumerate(src):
        if i >= limit:
            break  # Break out of the loop if the iteration limit is reached

        # Perform the copying logic based on the type of source element
        if type(src_el) == list:
            if type(dst) == list:
                try:
                    for j in range(len(src_el)):
                        if os.path.isfile(src_el[j]):
                            shutil.copy(src_el[j], dst[j])
                            total_size += os.path.getsize(src_el[j])
                        else:
                            shutil.copytree(src_el[j], dst[j]+'/'+src_el[j], dirs_exist_ok=True)
                            total_size += get_directory_size(src_el[j])
                        
                        # Check the total size against the limit
                        if total_size >= llimit:
                            print("File size limit reached. Stopping further copies.")
                            return
                except IndexError:
                    pass
            else:
                for src_item in src_el:
                    if os.path.isfile(src_item):
                        shutil.copy(src_item, dst)
                        total_size += os.path.getsize(src_item)
                    else:
                        shutil.copytree(src_item, dst+'/'+src_item, dirs_exist_ok=True)
                        total_size += get_directory_size(src_item)

                    # Check the total size against the limit
                    if total_size >= llimit:
                        print("File size limit reached. Stopping further copies.")
                        return
        else:
            if os.path.isfile(src_el):
                shutil.copy(src_el, dst)
                total_size += os.path.getsize(src_el)
            else:
                dst_list = [d + '/' + src_el for d in dst]  # Append src_el to each element in dst
                shutil.copytree(src_el, dst_list, dirs_exist_ok=True)
                total_size += get_directory_size(src_el)

            # Check the total size against the limit
            if total_size >= llimit:
                print("File size limit reached. Stopping further copies.")
                return

def get_directory_size(directory):
    # Helper function to get the size of a directory and its contents
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size


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