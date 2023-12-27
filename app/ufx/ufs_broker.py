import os
import requests
import signal
import select
import os

# Create a pipe 
read_fd, write_fd = os.pipe() 

# Write data to the pipe
os.write(write_fd, b"Hello, world!")

# Write the pipe data to a file
with open("file.txt", "wb") as f:
    os.lseek(read_fd, 0, os.SEEK_SET)
    f.write(os.read(read_fd, 1024))

"""
In this example, os.write() is used to write the string "Hello, world!" to the write end of the pipe. The b prefix before the string indicates that it should be treated as a bytes object. The os.lseek() method is used to move the read pointer to the beginning of the pipe, and os.read() is used to read the data from the pipe. The data is then written to a file using the write() method of a file object.
To write the write_fd memory to a REST API function, you can use the requests module in Python. Here is an example of how to use it:
"""

# Send the pipe data to a REST API endpoint
url = "https://example.com/api/data"
headers = {"Content-Type": "application/octet-stream"}
data = os.read(read_fd, 1024)
response = requests.post(url, headers=headers, data=data)

""""
In this example, os.read() is used to read the data from the pipe, and the data is then sent to a REST API endpoint using the requests.post() method. The Content-Type header is set to application/octet-stream to indicate that the data being sent is binary data.
"""




# Create a pipe 
read_fd, write_fd = os.pipe() 

""" ## Create a pipe
    read_fd, write_fd = os.pipe(): This line creates a unidirectional pipe, which is a communication channel between two processes. The pipe has two file descriptors:
        read_fd: Used for reading data from the pipe.
        write_fd: Used for writing data to the pipe.
"""

# Set a 2 second alarm
signal.alarm(2)

print("Waiting for data on pipe...")

# Monitor pipe for data
result = select.select([read_fd], [], [], 0) 

""" ## Monitor read_fd pipe for data
    result = select.select([read_fd], [], [], 0): This line monitors the read_fd for incoming data. The select.select() function waits for activity on one or more file descriptors:
    [read_fd]: Specifies that we're only interested in events on the read_fd.
    []: Indicates that we're not monitoring any file descriptors for writing.
    []: Specifies that we're not monitoring any file descriptors for exceptional conditions.
    0: Timeout value, set to 0 in this case, meaning it will return immediately with available events.
    select ensures the read will not block if no data is available.
"""


if result[0]:
  # Pipe is ready to read
  data = os.read(read_fd, 1024)
  print("Read", len(data), "bytes from pipe")
else: 
  print("No data after 2 seconds")

""" ## Check for data on the pipe:
    if result[0]: If the result list is not empty, it means there's data available to be read from the pipe.
    data = os.read(read_fd, 1024): Reads up to 1024 bytes of data from the read_fd and stores it in the data variable.
    print("Read", len(data), "bytes from pipe"): Prints the number of bytes read from the pipe.
    else:: If no data is available after 2 seconds, this block executes.
    print("No data after 2 seconds"): Prints a message indicating that no data was received within the timeout period.
"""


# Send data to pipe
os.write(write_fd, b"Hello World")

"""  ## Write data to the write_fd pipe
    os.write(write_fd, b"Hello World"): Writes the string "Hello World" (in bytes) to the write_fd of the pipe.
"""


print("Done")