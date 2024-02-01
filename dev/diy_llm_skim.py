import os
import sys
from dataclasses import dataclass, field


@dataclass
class filehandler():
    file_attr: str = field(default_factory=str)
    file_prop: str = "diyllmdump.txt"
    
    @property
    def file(self):
        return self.file_prop
    
    @file.setter
    def file(self, value):
        self.file_prop = value
    
    def __post_init__(self):
        if os.path.exists(self.file_prop):
            with open(self.file_prop, "r") as f:
                self.text = f.read()
        else:
            self.text = """this is plain text which will be copy pasted from the clipboard which has undesirable formatting"""
    
    def __str__(self):
        return self.text

def remove(text):
    find = {"Copy code", "avatar", "Type your message", "Send"}
    find2 = '''Chat
|
GitHub
|
Status
avatar
'''
    find3 = {"""
        python
        Copy code
    """}

    find4 = {"""
        avatar
        Type your message
        Send
"""}
    if text.startswith(find2):
        text = text[len(find2):]
    for f in find:
        text = text.replace(f, "")
    for f in find3:
        text = text.replace(f, "")
    for f in find4:
        text = text.replace(f, "")
    
    return text

def main():
    try:
        text = filehandler().__str__()
        cleaned_text = remove(text)

        # Write the cleaned text to a Markdown file
        output_file = "output.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_text)

        print(f"Processed text saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pass

if __name__ == "__main__":
    main()
