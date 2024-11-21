import os
import fcntl
import errno
import time
import signal

def run_command(command, timeout=None, env=None, encoding='utf-8'):
    """
    Executes a command, capturing stdout and stderr with optional timeout.

    Args:
        command (list): Command and arguments as a list, e.g., ['ls', '-l']
        timeout (float): Timeout in seconds for the command to execute.
        env (dict): Environment variables to set for the command.
        encoding (str): Encoding for decoding output streams (default: 'utf-8').

    Returns:
        tuple: stdout (str), stderr (str), exit_status (int)
    """
    r_stdout, w_stdout = os.pipe()  # Pipes for capturing stdout
    r_stderr, w_stderr = os.pipe()  # Pipes for capturing stderr
    pid = os.fork()  # Fork the process

    if pid == 0:  # Child process
        os.close(r_stdout)
        os.close(r_stderr)
        os.dup2(w_stdout, 1)  # Redirect stdout to pipe
        os.dup2(w_stderr, 2)  # Redirect stderr to pipe
        os.close(w_stdout)
        os.close(w_stderr)

        try:
            # Execute the command
            if env:
                os.execvpe(command[0], command, env)
            else:
                os.execvp(command[0], command)
        except Exception as e:
            print(f"Execution failed: {e}", file=os.fdopen(2, 'w'))
            os._exit(1)  # Exit with error code 1

    else:  # Parent process
        os.close(w_stdout)
        os.close(w_stderr)
        fcntl.fcntl(r_stdout, fcntl.F_SETFL, fcntl.fcntl(r_stdout, fcntl.F_GETFL) | os.O_NONBLOCK)
        fcntl.fcntl(r_stderr, fcntl.F_SETFL, fcntl.fcntl(r_stderr, fcntl.F_GETFL) | os.O_NONBLOCK)

        stdout_output = []
        stderr_output = []
        start_time = time.time()
        status = None

        try:
            while True:
                # Handle timeout
                if timeout and (time.time() - start_time) > timeout:
                    os.kill(pid, signal.SIGTERM)  # Attempt graceful termination
                    time.sleep(0.1)
                    os.kill(pid, signal.SIGKILL)  # Force kill if still running
                    raise TimeoutError(f"Command '{' '.join(command)}' timed out after {timeout} seconds")

                # Read from stdout
                try:
                    stdout_chunk = os.read(r_stdout, 4096)
                    if stdout_chunk:
                        stdout_output.append(stdout_chunk.decode(encoding))
                except OSError as e:
                    if e.errno != errno.EAGAIN:
                        raise

                # Read from stderr
                try:
                    stderr_chunk = os.read(r_stderr, 4096)
                    if stderr_chunk:
                        stderr_output.append(stderr_chunk.decode(encoding))
                except OSError as e:
                    if e.errno != errno.EAGAIN:
                        raise

                # Check child process status
                pid_exit, status = os.waitpid(pid, os.WNOHANG)
                if pid_exit == pid:
                    break

                time.sleep(0.01)  # Prevent busy-waiting

        finally:
            # Ensure pipes are closed
            os.close(r_stdout)
            os.close(r_stderr)

            # Handle orphaned child process (if any)
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass

        # Convert output lists to strings
        stdout = ''.join(stdout_output)
        stderr = ''.join(stderr_output)

        return stdout, stderr, os.WEXITSTATUS(status) if status is not None else -1


# Example Usage
if __name__ == "__main__":
    try:
        stdout, stderr, status = run_command(['ls', '-l'], timeout=5)
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        print("STATUS:", status)
    except TimeoutError as e:
        print(e)
