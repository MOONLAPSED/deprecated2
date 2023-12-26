import subprocess
import os
import fcntl
import sys
import json
import select

"""
tube.py - a simple pipe tube for communication between processes.
TODO:
pipetube mpi
pipetube ipc
pipetube socket
pipetube kernel
pipetube shared memory
pipetube thread
pipetube stdio
pipetube non-blocking async
"""

class Pipe_Tube():
    try: input = sys.stdin.readline().strip().encode('ASCII')
    except Exception as e: print(f"Error: {e}")
    def __init__(self, input):
        self.input = input
    def PipetubeServer():
        def __init__(self): 
            self.read_fd, self.write_fd = os.pipe()
            fcntl.fcntl(self.read_fd, fcntl.F_SETFL, os.O_NONBLOCK)

    def read(self, max_bytes: int) -> bytes:
        return os.read(self.read_fd, max_bytes)
    
    def write(self, data: bytes) -> int:
        return os.write(self.write_fd, data)

    def data_available(self) -> bool:
        return select.select([self.read_fd], [], [], 0) == ([self.read_fd], [], [])

    def __enter__(self):
        return self

class PipetubePath:
    def __init__(self, path: str):
        self.path = path
    
    def write(self, data: bytes):
        subprocess.run(f'echo {data.decode("utf-8")} | {self.path}', shell=True)
    
    def read(self) -> bytes:
        return subprocess.check_output(f'{self.path} | cat', shell=True)

    def __str__(self): 
        return f"Pipetube({self.path})"
    
    def pipesocket(path: str):
        if not os.pipe(path):
            raise Exception("Pipe does not exist")
        return Pipetube(path)

    def pipe():
        return Pipetube.pipesocket("/tmp/pipe")

    def pipewrite(data: bytes):
        return Pipetube.pipe().write(data)
    
    def piperead() -> bytes:
        return Pipetube.pipe().read()
        

async def Pipe_Tube_Server():
    while True:
        try:
            with Pipe_Tube.PipetubeServer() as server:
                while True:
                    if server.data_available():
                        data = server.read(1024)
                        if data:
                            print(f"Pipe_Tube_Server: {data}")
                            Pipe_Tube.pipewrite(data)
        except Exception as e:
            print(f"Pipe_Tube_Server: {e}")

async def Pipe_Tube_Client():
    while True:
        try:
            with PipetubePath.pipe() as pipe:
                while True:
                    data = PipetubePath.piperead()
                    if data:
                        print(f"Pipe_Tube_Client: {data}")
                        pipe.write(data)
        except Exception as e:
            print(f"Pipe_Tube_Client: {e}")