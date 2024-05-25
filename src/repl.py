import ast
import signal
import sys

class REPLEnvironment:
    def __init__(self):
        self.namespace = {}

    def handle_signal(self, signum, frame):
        print("Received unexpected signal: ", signum)
        print("Continuing execution...")

    def run(self):
        signal.signal(signal.SIGINT, self.handle_signal)  # Handle keyboard interrupts

        while True:
            try:
                user_input = input(">>> ")
                if user_input.strip() == "exit":
                    break

                try:
                    node = ast.parse(user_input, mode="eval")
                    result = eval(compile(node, filename="<input>", mode="eval"), self.namespace)
                    print(result)
                except SyntaxError:
                    try:
                        exec(user_input, self.namespace)
                    except Exception as e:
                        print(f"Error: {e}")

            except Exception as e:
                print(f"Unexpected error: {e}")

if __name__ == "__main__":
    repl = REPLEnvironment()
    repl.run()
    """
    def repl():
        while True:
            try:
                input_value = input("> ")
                if input_value.lower() == "exit":
                    break
                result = eval(input_value)
                print(result)
            except Exception as e:
                print(f"Error: {e}")

    print("Welcome to the REPL!")
    print("Type 'exit' to quit.")
    repl()
    """