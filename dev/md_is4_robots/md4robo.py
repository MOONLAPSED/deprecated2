init_string = str({"schema": "The provided logic is a description of a custom syntax or markup language that defines how to generate content based on various rules, conditions, and functions. This description outlines the syntax and semantics for defining these rules and conditions."})
"""
// Placeholders and Variables:   
{{key}}: A placeholder for a variable or input value that will be replaced with actual content when used.
${{key}}: A variable or input value that is instantiated or declared and is only required once per variable. It is not replaced with content but serves to declare variables.

// Modifiers:
~{{key}}: Indicates an approximate value or range for the specified key. 
+{{key}}: Appends or concatenates the value of key with another element.
={{key}}: Specifies that the generated content should have an exact match or value equal to key.
!{{key}}: Negates or excludes the value of key from the generated content.  
-{{key}}: Removes or subtracts the value of key from the generated content.
*{{key}}: Specifies that the generated content should repeat the specified property or attribute key times.  
>{{key}}, <{{key}}, <={{key}}, >={{key}}: Define length comparisons for generated content.

// Conditional Expressions:
?{{key1}}:{{key2}}: Used for conditional expressions, where if the condition specified by key1 is met, the generated content will include key2.

// Keywords:   
ANY, ALWAYS, NEVER, WITH, AND, ONLY, NOT, UNIQUE: Keywords that modify or constrain the generated content based on specific conditions.

// Functions:
between({{key1}}, {{key2}}): Specifies a range for a certain attribute or property in the generated content.  
random({{key1}}, {{key2}}, ...): Specifies that the generated content should include one of the provided keys at random.
mixed({{key1}}, {{key2}}, ...): Specifies that the generated content should include a combination of the provided keys.
contains({{key}}): Indicates that the generated content must contain the specified key.
optimize({{key}}): Suggests that the generated content should optimize for a certain aspect represented by the key.
limit({{key}}, {{value}}): Sets a limit on the number of times the specified key can appear in the generated content.

// Function Arguments:
fn(-{{key}}): Represents a function fn that takes the value of key as an input and removes or subtracts it from the generated content. 
fn(*{{key}}): Represents a function fn that takes the value of key as an input and repeats a specific property or attribute key times.
fn(?{{key1}}:{{key2}}): Represents a function fn that takes the values of key1 and key2 as inputs and includes key2 in the generated content if the condition specified by key1 is met.
"""
import json
import re
from typing import List, Optional

# Define a function to process the custom syntax
def process_custom_syntax(input_text, context={}):
    # Split the input text into tokens using space as a delimiter
    tokens = input_text.split()

    # Initialize an output string
    output = ""

    # Loop through the tokens
    for token in tokens:
        # Check if the token is a placeholder {{key}}
        if token.startswith("{{") and token.endswith("}}"):
            key = token[2:-2]  # Extract the key
            if key in context:
                # Replace the placeholder with the corresponding value from the context
                output += context[key]
            else:
                # If the key is not in the context, leave it as is
                output += token
        else:
            # If the token is not a placeholder, add it to the output
            output += token

        # Add a space after each token
        output += " "

    # Remove trailing space and return the processed text
    return output.strip()

# Example usage:
custom_syntax = "This is a {{key1}} example {{key2}} with some {{key3}}."
context = {
    "key1": "custom",
    "key2": "text",
    "key3": "placeholders"
}

result = process_custom_syntax(custom_syntax, context)
print(result)

def process_text(input_text):
    # Split the input text into chunks based on a specific delimiter or pattern
    chunks = re.split(r'\n\n|\n\n\n', input_text)

    # Initialize a list to store the processed chunks
    processed_chunks = []

    # Loop through each chunk
    for chunk in chunks:
        # Process each chunk of text using the provided custom syntax logic
        processed_chunk = process_custom_syntax(chunk)
        processed_chunks.append(processed_chunk)

    # Jsonify or stringify the processed text
    processed_text = json.dumps(processed_chunks)

    return processed_text

# Example usage:
input_text = """
This is the first chunk of text.

This is the second chunk of text.

This is the third chunk of text.
"""

processed_text = process_text(input_text)
display(processed_text)

class PreProcessor:
    def __init__(self):
        pass
    
    def filter_explicit(self, input_text):
        # Implement the logic to filter out explicit content
        filtered_text = input_text.replace("explicit", "")
        return filtered_text

# Example usage:
preprocessor = PreProcessor()
filtered_text = preprocessor.filter_explicit(input_text)
display(filtered_text)

def chunk_text(input_text: str, chunk_size: int = 4096) -> List[str]:
    chunks = []
    chunk = ""
    for i in range(0, len(input_text), chunk_size):
        chunk = input_text[i:i+chunk_size]
        if len(chunk) < chunk_size:
            chunk += "0" * (chunk_size - len(chunk))
        chunks.append(chunk)
    return chunks

def process_chunked_text(input_text: str, chunk_size: int = 4096, add_params: Optional[List[str]] = None) -> str:
    chunks = chunk_text(input_text, chunk_size)
    processed_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            processed_chunk = "<im_start> " + chunk
        else:
            processed_chunk = "<contd> " + chunk
        processed_chunks.append(processed_chunk)
    if add_params:
        processed_chunks.append("<|new file, or next/last chunk in current file|>")
        processed_chunks.extend(add_params)
    processed_text = json.dumps(processed_chunks)
    return processed_text