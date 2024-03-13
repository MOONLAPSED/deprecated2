import json
from types import SimpleNamespace

with open("path/to/your/file.json", "r") as your_file:

    your_dict = json.load(your_file)
    your_file.seek(0)
    # so you can reload the JSON data a second time but in a different way
    your_root = json.load(your_file, object_hook= lambda x:
                                        SimpleNamespace(**x))
    # Lambda function taking an argument 'x':
        # For each JSON object encountered, it creates a SimpleNamespace object and passes 'x' (the original JSON object) as its initialization data.
    # The **x syntax is equivalent to passing each key-value pair of the JSON object as a keyword argument to the SimpleNamespace constructor.