import subprocess
import os


class VirtualShell:
    """
    A foundational abstract class representing a virtual Unix shell within a Python runtime environment.

    The VirtualShell class acts as an abstraction layer, facilitating interactions with the Unix file system
    by providing methods to execute commands, manage the current working directory, and handle errors
    encountered during system operations. Its inheritors can extend functionality specific to certain tasks,
    interpreting Unix file system operations within a controlled, virtualized runtime environment.

    Attributes:
        cwd (str): Represents the current working directory within the virtual environment.

    Methods:
        execute_command(command: str) -> Tuple[str, str]: Executes a command within the virtual shell
            and returns the standard output and standard error of the executed command.
        change_directory(new_directory: str) -> Tuple[bool, str]: Changes the current working directory
            within the virtual environment and returns a success flag along with any encountered errors.
    """
    def __init__(self):
        self.cwd = os.getcwd()  # Get current working directory

    def execute_command(self, command):
        try:
            # Execute the command using subprocess
            result = subprocess.run(command, shell=True, cwd=self.cwd, capture_output=True, text=True)
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            return None, f"Error: {e}"

    def change_directory(self, new_directory):
        try:
            os.chdir(new_directory)  # Change current working directory
            self.cwd = os.getcwd()  # Update the stored current working directory
            return True, None
        except FileNotFoundError:
            return False, f"Directory '{new_directory}' not found"
        except PermissionError:
            return False, "Permission denied"

def main():
    shell = VirtualShell()
    while True:
        command = input(f"{shell.cwd} $ ")
        if command == "exit":
            break
        """
            Each command input by the user is executed within the virtual shell using shell.execute_command(), and 
                the output (standard output and standard error) is printed to the console.
        """
        output, error = shell.execute_command(command)
        print("Output:", output)
        print("Error:", error)

        # Example usage within the shell
        if command.startswith("ls"):  # Example: ls -l
            output, error = shell.execute_command(command)
            print("Output:", output)
            print("Error:", error)
        elif command.startswith("cd"):  # Example: cd /path/to/new/directory
            _, change_error = shell.change_directory(command.split(" ")[1])
            if change_error:
                print("Error:", change_error)
            else:
                print("Directory changed successfully")
        else:
            print("Command not recognized")

if __name__ == "__main__":
    main()
