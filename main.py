import os
from dotenv import load_dotenv

def load_env_file():
    try:
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
            return True, "Loaded .env file successfully"
        else:
            # If .env file is not found in the current directory, search in the subdirectories
            for root, dirs, files in os.walk(os.path.dirname(__file__)):
                for file in files:
                    if file == '.env':
                        load_dotenv(os.path.join(root, file))
                        return True, "Loaded .env file successfully"
            return False, "Failed to find .env file"   
    except Exception as e:
        return False, f"Loading .env failed with error: {e}"

result, message = load_env_file()
if result:
    print("Successfully")
    print(message)
else:
    print(message)