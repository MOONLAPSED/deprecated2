import subprocess
import os
import fcntl
import sys
import json


class Pipetube:
    def __init__(self, path: str):
        self.path = path
    
    def write(self, data: bytes):
        subprocess.run(f'echo {data.decode("utf-8")} | {self.path}', shell=True)
    
    def read(self) -> bytes:
        return subprocess.check_output(f'{self.path} | cat', shell=True)

    def __enter__(self):
        return self

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
    
    def close(self):
        self.close()

    def __del__(self):
        os.remove(self.path)


class PipetubeServer:

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

  def __exit__(self, exc_type, exc_value, traceback):
    self.close()


while True:  # per no_state_pipe.sh

  # Read input (JSON string)
  input = sys.stdin.readline()
  
  try:
    # Parse JSON
    data = json.loads(input)  
  except:
    # Handle non-JSON input
    data = input

  # Process data (input-specific logic)

  # Generate output
  output = {"response": "ok"} 
  
  print(json.dumps(output))