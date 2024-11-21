import subprocess
import time
import os
import signal
from threading import Thread
from queue import Queue, Empty


def read_stream(stream, queue):
    """Reads lines from a stream and pushes them to a queue."""
    for line in iter(stream.readline, b""):
        queue.put(line.decode(errors="replace"))  # Decode with error handling for robustness
    stream.close()


def run(command, timeout=None, env=None):
    """
    Executes a command, capturing stdout and stderr with optional timeout.

    Args:
        command (list): Command and arguments, e.g., ['cmd', '/c', 'dir']
        timeout (float): Timeout in seconds for the command to execute
        env (dict): Environment variables for the subprocess

    Returns:
        tuple: stdout (str), stderr (str), exit_status (int)
    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=False,  # Binary streams
        env=env,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    )

    # Queues for inter-thread communication
    stdout_queue = Queue()
    stderr_queue = Queue()

    # Threads to read stdout and stderr
    stdout_thread = Thread(target=read_stream, args=(process.stdout, stdout_queue), daemon=True)
    stderr_thread = Thread(target=read_stream, args=(process.stderr, stderr_queue), daemon=True)
    stdout_thread.start()
    stderr_thread.start()

    start_time = time.time()

    try:
        while True:
            # Check if timeout has been exceeded
            if timeout and (time.time() - start_time) > timeout:
                if os.name == "nt":
                    process.send_signal(signal.CTRL_BREAK_EVENT)
                else:
                    process.terminate()  # UNIX fallback
                raise TimeoutError(f"Command '{' '.join(command)}' timed out after {timeout} seconds")

            # Check if process has completed
            ret_code = process.poll()
            if ret_code is not None:
                break

            time.sleep(0.05)  # Small sleep to prevent busy-waiting

    finally:
        # Ensure threads finish
        stdout_thread.join(timeout=1)
        stderr_thread.join(timeout=1)

        # Ensure process streams are closed
        process.stdout.close()
        process.stderr.close()

    # Collect output from queues
    stdout = ''.join(iter(lambda: stdout_queue.get_nowait() if not stdout_queue.empty() else '', ''))
    stderr = ''.join(iter(lambda: stderr_queue.get_nowait() if not stderr_queue.empty() else '', ''))

    return stdout, stderr, process.returncode


def call(command, timeout=None, env=None):
    """
    Executes a command synchronously and returns the exit status.

    Args:
        command (list): Command and arguments, e.g., ['cmd', '/c', 'dir']
        timeout (float): Timeout in seconds for the command to execute
        env (dict): Environment variables for the subprocess

    Returns:
        int: Exit status of the command.
    """
    _, _, exit_status = run(command, timeout=timeout, env=env)
    return exit_status


def copy(command, timeout=None, env=None, file_path=None):
    """
    Executes a command and optionally writes stdout to a file.

    Args:
        command (list): Command and arguments, e.g., ['cmd', '/c', 'dir']
        timeout (float): Timeout in seconds for the command to execute
        env (dict): Environment variables for the subprocess
        file_path (str): Path to a file where stdout will be copied.

    Returns:
        str: The captured stdout.
    """
    stdout, stderr, exit_status = run(command, timeout=timeout, env=env)

    # Write to file if a file path is provided
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(stdout)

    return stdout


# Example usage
if __name__ == "__main__":
    # Example 1: Using `run` to capture output
    try:
        stdout, stderr, status = run(["cmd", "/c", "dir"], timeout=5)
        print("RUN - STDOUT:\n", stdout)
        print("RUN - STDERR:\n", stderr)
        print("RUN - STATUS CODE:", status)
    except TimeoutError as e:
        print(e)

    # Example 2: Using `call` for synchronous execution
    status = call(["cmd", "/c", "dir"], timeout=5)
    print("CALL - STATUS CODE:", status)

    # Example 3: Using `copy` to capture output and save to a file
    stdout = copy(["cmd", "/c", "dir"], timeout=5, file_path="output.txt")
    print("COPY - STDOUT (Saved to file):\n", stdout)
