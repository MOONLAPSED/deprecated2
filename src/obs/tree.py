from collections import deque
import os
import sys
import pathlib
"""
Creates heriarchial tree representation of a network.
The tree representation is created by traversing the network and creating a tree of the layers.
The tree has a syntax similar to the bracket notation used in linguistics to represent the structure of sentences for use by LLMs.
All tree methods must break the network into a tree of layers, and then create a string representation of the tree such that it can be conveyed in markdown-formatted text.
Tree to Tree operations are 'interpreted' at runtime - via NLP and agentic, out of scope, operations. Trees must maintain internal-consistency and be able to be 'interpreted' by the network.
"""

# conforms with MyST notebook format and obsidian markdown(function calling, etc.) - see https://myst-parser.readthedocs.io/en/latest/

def _insert_header(incomings, outgoings):
    """Insert the header (first two lines) in the representation."""
    headers = []
    separators = []

    if incomings:
        headers.append('In')
        separators.append('---')  # Markdown requires at least three dashes for separators.

    headers.append('Layer')
    separators.append('-----')

    if outgoings:
        headers.append('Out')
        separators.append('---')

    headers.append('Description')
    separators.append('-----------')

    # Construct Markdown table header strings
    header_line = '| ' + ' | '.join(headers) + ' |'
    separator_line = '| ' + ' | '.join(separators) + ' |'

    # Return as list for ease of further appending or processing.
    return [header_line, separator_line]

# Use the function like this:
network_str = []
network_str.extend(_insert_header(incomings=True, outgoings=True))
# ... rest of your serialization process.

class Tree(object):
    """Represents a Tree Node"""

    def __init__(self, name, *children):
        self.name = name
        self.children = list(children)

    def bracket(self):
        """Show tree using brackets notation"""
        result = str(self.name)
        for child in self.children:
            result += child.bracket()
        return "{{{}}}".format(result)

    def __repr__(self):
        return self.bracket()

    @classmethod
    def from_text(cls, text):
        """Create tree from bracket notation

        Bracket notation encodes the trees with nested parentheses, for example,
        in tree {A{B{X}{Y}{F}}{C}} the root node has label A and two children
        with labels B and C. Node with label B has three children with labels
        X, Y, F.
        """
        tree_stack = []
        stack = []
        for letter in text:
            if letter == "{":
                stack.append("")
            elif letter == "}":
                text = stack.pop()
                children = deque()
                while tree_stack and tree_stack[-1][1] > len(stack):
                    child, _ = tree_stack.pop()
                    children.appendleft(child)

                tree_stack.append((cls(text, *children), len(stack)))
            else:
                stack[-1] += letter
        return tree_stack[0][0]

def _check_for_obst(self, steps, vector_mag, clear_x, clear_y):
        """
        Look for obstacles in the path 'steps'
        and stop short if they are there.
        clear_x and clear_y start out as the agent's current pos,
        which must, of course, be clear for this agent to occupy!
        If there happens to be an obstacle less than tolerance - 1
        from the agent's initial square, well, we just stay put.
        """
        lag = self.tolerance - 1
        lookahead = deque(maxlen=lag + 1)
        for (x, y) in steps:
            lookahead.append((x, y))
            if not self.env.is_cell_empty(x, y):
                return (clear_x, clear_y)
            elif lag > 0:
                lag -= 1
            else:
                (clear_x, clear_y) = lookahead.popleft()
        return (clear_x, clear_y)
