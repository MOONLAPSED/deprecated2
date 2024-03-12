#! /usr/bin/env python3
# /src/ufx.py - define the ABCs for the UnixFilesystem and its interfaces and methods as well as core dataclasses.
from abc import *
import os
import re
import sys
import shutil
import subprocess
# Define the constant limits
limit = 10  # Arbitrary limit for iterations and permutations (loops, dfs, bfs, etc.)
llimit = 10 * 1000000  # 10 MB file size limit

from collections import deque

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





def call(self, cmd, **kwargs):
    """
    In this code snippet, a method called `call()` is defined inside a class. The method takes three arguments - cmd (command), **kwargs (keywords arguments), and an optional `expect` argument containing a list of dictionaries with keys "return_codes", "stdout", and "stderr".

    The main goal of the `call()` function is to execute the command specified in the 'cmd' argument. It does this by creating a subprocess using `subprocess.Popen` and passing in the appropriate keyword arguments such as stdin, stdout, and stderr based on the given kwargs.

    After executing the command, the function collects the output (stdout and stderr) from the subprocess and assigns it to 'out' and 'err' variables. It also captures the return code of the executed command using `process.poll()`. The `return_code` variable stores this value.

    The `match()` function is used to check if the expected output matches with the actual output. For this, it compares the given return codes, stdout and stderr against the values provided in the 'expect' dictionary. If all conditions are met, the function returns True, else False.

    Finally, if the command execution fails (i.e., any of the conditions in `match()` is not met), an exception (`subprocess.CalledProcessError`) is raised with appropriate error messages and return code. Otherwise, a `SubprocessResult` object is returned containing the output, stderr, and return code from the executed command.
    """
    print('Running "{}"'.format(cmd), file=sys.stderr)
    expect = kwargs.pop("expect", [dict(return_codes=[os.EX_OK], stdout=None, stderr=None)])
    process = subprocess.Popen(cmd, stdin=kwargs.get("stdin", subprocess.PIPE), stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, **kwargs)
    out, err = process.communicate()
    return_code = process.poll()
    out = out.decode(sys.stdin.encoding)
    err = err.decode(sys.stdin.encoding)

    def match(return_code, out, err, expected):
        exit_ok = return_code in expected["return_codes"]
        stdout_ok = re.search(expected.get("stdout") or "", out)
        stderr_ok = re.search(expected.get("stderr") or "", err)
        return exit_ok and stdout_ok and stderr_ok
    if not any(match(return_code, out, err, exp) for exp in expect):
        print(err)
        e = subprocess.CalledProcessError(return_code, cmd, output=out)
        e.stdout, e.stderr = out, err
        raise e
    return self.SubprocessResult(out, err, return_code)