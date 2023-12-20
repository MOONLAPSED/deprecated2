import re

def process_custom_syntax(input_text, context={}):
    # Split input into tokens
    tokens = input_text.split()

    # Initialize output
    output = ""

    # Loop through tokens
    for token in tokens:
        # Check if token is a placeholder
        if token.startswith("{{") and token.endswith("}}"):
            key = token[2:-2]
            if key in context:
                output += context[key]
            else:
                output += token
        # Check if token contains a placeholder in the middle
        elif "{{" in token and "}}" in token:
            start = token.index("{{")
            end = token.index("}}") + 2
            key = token[start+2:end-2]
            if key in context:
                output += token[:start] + context[key] + token[end:]
            else:
                output += token
        else:
            output += token

        # Add space after token
        output += " "

    # Remove trailing space
    return output.strip()

# Example usage
custom_syntax = "This is a {{key1}} example {{key2}} with some {{key3}}."
context = {
  "key1": "custom",
  "key2": "text", 
  "key3": "placeholders"
}

result = process_custom_syntax(custom_syntax, context)
print(f"{result}")

  # Outputs: This is a custom example text with some placeholders.

class CustomSyntax:
    def __init__(self):
        self.var_regex = re.compile(r"\{\{([\w]+)\}\}")

    def process(self, text, context):
        def var_replace(match):
            var_name = match.group(1)
            if var_name in context:
                return context[var_name]
            return match.group(0)
        
        return self.var_regex.sub(var_replace, text)

processor = CustomSyntax()

text = "This has a {{var1}} and a {{var2}} variable."
context = {"var1": "first", "var2": "second"}

result = processor.process(text, context)
print(result)

# Outputs: This has a first and a second variable.