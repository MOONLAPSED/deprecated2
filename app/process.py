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
