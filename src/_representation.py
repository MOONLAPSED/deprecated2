import hashlib
from dataclasses import dataclass, field
from typing import Optional, List, Union


# --- Utility Functions ---

def generate_color_from_hash(hash_str: str) -> str:
    """Generate an ANSI escape color code based on the first 6 characters of a hash."""
    color_value = int(hash_str[:6], 16)  # Convert the first 6 chars to an integer
    r = (color_value >> 16) % 256
    g = (color_value >> 8) % 256
    b = color_value % 256
    return f"\033[38;2;{r};{g};{b}m"  # ANSI color escape sequence


def hash_data(data: str) -> str:
    """Hashes the input data using SHA-256 and returns the hex digest."""
    return hashlib.sha256(data.encode()).hexdigest()


def short_hash(hash_str: str) -> str:
    """Returns the first 6 characters of the hash as a short identifier."""
    return hash_str[:6]


# --- Node Definitions ---

@dataclass
class Node:
    """Base class for a node in the Merkle tree."""
    hash: str = field(init=False)
    short_hash: str = field(init=False)

    def __post_init__(self):
        raise NotImplementedError("Subclasses must implement __post_init__")

    def __repr__(self):
        color = generate_color_from_hash(self.hash)
        return f"{color}[{self.short_hash}]\033[0m"


@dataclass
class LeafNode(Node):
    """Leaf node representing the original data in the Merkle tree."""
    data: str

    def __post_init__(self):
        self.hash = hash_data(self.data)
        self.short_hash = short_hash(self.hash)

    def __repr__(self):
        color = generate_color_from_hash(self.hash)
        return f"{color}Leaf({self.data[:10]})[{self.short_hash}]\033[0m"


@dataclass
class InternalNode(Node):
    """Internal node combining two child nodes to form a parent."""
    left: Node
    right: Optional[Node] = None

    def __post_init__(self):
        combined_hash = self.left.hash + (self.right.hash if self.right else self.left.hash)
        self.hash = hash_data(combined_hash)
        self.short_hash = short_hash(self.hash)

    def __repr__(self):
        color = generate_color_from_hash(self.hash)
        right_repr = f", {self.right}" if self.right else ""
        return f"{color}Internal({self.left}{right_repr})[{self.short_hash}]\033[0m"


# --- Merkle Tree ---

class MerkleTree:
    """Class representing a complete Merkle tree."""
    def __init__(self, data_chunks: List[str]):
        self.leaves = [LeafNode(data) for data in data_chunks]
        self.root = self.build_tree(self.leaves)

    def build_tree(self, nodes: List[Node]) -> Node:
        """Recursively build the tree and return the root node."""
        while len(nodes) > 1:
            new_level = []
            for i in range(0, len(nodes), 2):
                if i + 1 < len(nodes):
                    new_level.append(InternalNode(left=nodes[i], right=nodes[i + 1]))
                else:
                    new_level.append(InternalNode(left=nodes[i]))
            nodes = new_level
        return nodes[0]

    @property
    def root_hash(self) -> str:
        """Return the hash of the root node of the tree."""
        return self.root.hash

    def visualize(self):
        """Recursively visualizes the tree structure."""
        def traverse(node: Node, depth: int = 0):
            print(f"{'  ' * depth}{node}")
            if isinstance(node, InternalNode):
                traverse(node.left, depth + 1)
                if node.right:
                    traverse(node.right, depth + 1)

        print("Merkle Tree Visualization:")
        traverse(self.root)


# --- Example Usage and Debugging ---

if __name__ == "__main__":
    print("Building Merkle Tree...")
    data_chunks = ["apple", "banana", "cherry", "date", "elderberry"]
    merkle_tree = MerkleTree(data_chunks)

    print("\nTree Visualization:")
    merkle_tree.visualize()

    print(f"\nRoot Hash: {merkle_tree.root_hash}")

    # Color demonstration
    print("\nColored Nibbles (Short Hashes):")
    for leaf in merkle_tree.leaves:
        print(leaf)
