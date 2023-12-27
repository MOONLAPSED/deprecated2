# =================xGLOBAL_IMPORTS
import sys
import os
import json
import datetime
import re
import logging
import typing
import typing_extensions
import subprocess
import fcntl
import select
# ==================xSUBMODULE_IMPORTS

class TextStats:

    def __init__(self):
        self.states = {}
        self.delimiters = ['\n\n', '```']
        self.current_block = ""
        self.inside_code_block = False

    def process_character(self, char):
        if self.inside_code_block:
            if char == '`' and self.current_block.endswith('```'):
                self.inside_code_block = False
                self.current_block += char
                self.process_block()
            else:
                self.current_block += char
        else:
            if char in ['\n', '`']:
                self.process_block()
                if char == '`' and self.current_block.endswith('```'):
                    self.inside_code_block = False
                    self.current_block += char
                else:
                    self.inside_code_block = True
                    self.current_block += char
            else:
                self.current_block += char

    def process_block(self):
        state = self.get_state(self.current_block)
        if state in self.states:
            self.states[state] += 1
        else:
            self.states[state] = 1
        self.current_block = ""

    def get_state(self, block):
        if block.startswith('#'):
            return "header"
        elif block.startswith('```'):
            return "code"

        len_chars = len(block)
        len_words = len(block.split())

        if len_chars < 50:
            return "short"
        elif len_words < 5:
            return "minimal"
        elif block.strip() == '':
            return "empty"
        else:
            return "non_empty_non_standard"

    @property
    def quantities(self):
        return self.states

# Example usage:
stats = TextStats()
text = "Your long string of .md files..."  # Stream of ASCII characters
for char in text:
    stats.process_character(char)
print(stats.quantities)
