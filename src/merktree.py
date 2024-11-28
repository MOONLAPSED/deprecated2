import hashlib
import os
from dataclasses import dataclass, field
from typing import List, Optional, Protocol, Callable
import itertools

def hash_data(data: str) -> str:
    """Generate a SHA-256 hash of the given data."""
    return hashlib.sha256(data.encode()).hexdigest()

def generate_color_from_hash(hash_str: str) -> str:
    """Generate an ANSI color code based on the hash string.
    
    This function creates a color based on the first 6 characters of the hash,
    providing a unique color representation for each hash.
    """
    color_value = int(hash_str[:6], 16)
    r = (color_value >> 16) % 256
    g = (color_value >> 8) % 256
    b = color_value % 256
    return f"\033[38;2;{r};{g};{b}m"

# Type Definition: State Reflection
class MorphType(Protocol):
    def morph(self) -> None:
        """Dynamically adapt or evolve"""

# Value Node with Dynamic Capabilities
@dataclass
class MorphologicalNode:
    data: str
    hash: str = field(init=False)
    morph_operations: List[Callable[[str], str]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize the node by calculating its initial hash and applying morphs."""
        self.hash = self.calculate_hash(self.data)
        self.reflect_and_morph()

    def calculate_hash(self, input_data: str) -> str:
        """Calculate hash of data, reflects state."""
        return hashlib.sha256(input_data.encode()).hexdigest()

    def morph(self) -> None:
        """Simulate adapting to its environment via self-reflection."""
        for operation in self.morph_operations:
            self.data = operation(self.data)

    def reflect_and_morph(self) -> None:
        """Run self-modifications and update hash."""
        if self.morph_operations:
            self.morph()
            self.hash = self.calculate_hash(self.data)

@dataclass
class InternalNode:
    left: MorphologicalNode
    right: Optional[MorphologicalNode] = None
    hash: str = field(init=False)

    def __post_init__(self):
        """Calculate hash by combining left and right node hashes."""
        combined = self.left.hash + (self.right.hash if self.right else '')
        self.hash = hashlib.sha256(combined.encode()).hexdigest()

# Energy-like State Evolution in the Tree Process
class MorphologicalTree:
    def __init__(self, data_chunks: List[str], transformations: List[Callable[[str], str]]):
        """
        Initialize a MorphologicalTree with data chunks and transformation operations.
        
        :param data_chunks: List of initial data to create leaf nodes
        :param transformations: List of transformation functions to apply to nodes
        """
        self.leaves = [MorphologicalNode(data, morph_operations=transformations) for data in data_chunks]
        self.root = self.build_tree(self.leaves)

    def build_tree(self, nodes: List[MorphologicalNode]) -> InternalNode:
        """
        Recursively build a binary tree from the input nodes.
        
        :param nodes: List of nodes to be organized into a tree
        :return: Root node of the constructed tree
        """
        if not nodes:
            raise ValueError("Cannot build tree with empty nodes list")
        
        while len(nodes) > 1:
            new_level = []
            for i in range(0, len(nodes), 2):
                if i + 1 < len(nodes):
                    new_node = InternalNode(left=nodes[i], right=nodes[i+1])
                else:
                    new_node = InternalNode(left=nodes[i])
                new_level.append(new_node)
            nodes = new_level
        return nodes[0]

    def print_node_info(self, node, prefix=""):
        """
        Recursively print information about nodes in the tree.
        
        :param node: Current node to print information for
        :param prefix: Prefix for indentation and tree structure visualization
        """
        if isinstance(node, InternalNode):
            print(f"{prefix}Internal Node [Hash: {generate_color_from_hash(node.hash)}{node.hash[:8]}...\033[0m]")
            print(f"{prefix}├── Left:")
            self.print_node_info(node.left, prefix + "│   ")
            if node.right:
                print(f"{prefix}└── Right:")
                self.print_node_info(node.right, prefix + "    ")
        else:  # MorphologicalNode
            print(f"{prefix}Leaf Node:")
            print(f"{prefix}├── Data: {node.data}")
            print(f"{prefix}└── Hash: {generate_color_from_hash(node.hash)}{node.hash[:8]}...\033[0m")

    def visualize(self):
        """Print a visual representation of the tree."""
        print("\nTree Structure:")
        print("==============")
        self.print_node_info(self.root)

@dataclass
class MerkleRingNode:
    """Represents a node in the Merkle Ring."""
    data: str
    hash: str = field(init=False)
    next_hash: Optional[str] = None

    def __post_init__(self):
        """Initialize the hash of the node's data."""
        self.hash = hash_data(self.data)

    def __repr__(self):
        """Colorized representation of the node."""
        color = generate_color_from_hash(self.hash)
        return f"{color}Node(Data: {self.data[:10]}, Hash: {self.hash[:6]}, Next Hash: {self.next_hash[:6]})\033[0m"

class MerkleRing:
    def __init__(self, data_series: List[str]):
        """
        Initialize the Merkle Ring with a series of data.
        
        :param data_series: List of data strings to create nodes
        """
        self.nodes = [MerkleRingNode(data) for data in data_series]
        self.link_nodes()

    def link_nodes(self):
        """Link each node to the next in the series, forming a ring."""
        for i, node in enumerate(self.nodes):
            next_node = self.nodes[(i + 1) % len(self.nodes)]
            node.next_hash = next_node.hash

    def to_toml(self, filepath: str):
        """
        Persist the Merkle Ring to a TOML file.
        
        :param filepath: Path to save the TOML file
        """
        try:
            with open(filepath, 'wb') as f:
                # Create a TOML string representation of the data
                toml_string = "[nodes]\n"
                for node in self.nodes:
                    toml_string += f"[[nodes]]\n"
                    toml_string += f'data = "{node.data}"\n'
                    toml_string += f'hash = "{node.hash}"\n'
                    toml_string += f'next_hash = "{node.next_hash}"\n'
                f.write(toml_string.encode('utf-8'))
        except IOError as e:
            print(f"Error writing to TOML file: {e}")

    @staticmethod
    def from_toml(filepath: str) -> 'MerkleRing':
        """
        Load a Merkle Ring from a TOML file.
        
        :param filepath: Path to the TOML file
        :return: Reconstructed MerkleRing
        """
        try:
            with open(filepath, 'rb') as f:
                content = f.read().decode('utf-8')
                data_series = []
                lines = content.splitlines()
                for i in range(len(lines)):
                    if lines[i].startswith("data ="):
                        # Extract the data value
                        data_series.append(lines[i].split(" = ")[1].strip().strip('"'))
                return MerkleRing(data_series)
        except IOError as e:
            print(f"Error reading TOML file: {e}")
            return MerkleRing([])

    def visualize(self):
        """Display the structure of the Merkle Ring."""
        for node in self.nodes:
            print(node)

def demo_transformations(input_data: str, transformations: List[Callable[[str], str]]) -> None:
    """
    Demonstrate the effect of each transformation on input data.
    
    :param input_data: Initial data to transform
    :param transformations: List of transformation functions
    """
    print(f"\nDemonstrating transformations on input: '{input_data}'")
    current_data = input_data
    for i, transform in enumerate(transformations, 1):
        current_data = transform(current_data)
        print(f"After transformation {i}: '{current_data}'")

def main():
    """
    Comprehensive demonstration of MorphologicalTree and MerkleRing functionality.
    """
    # ANSI color codes for styling
    HEADER_COLOR = "\033[95m"  # Magenta
    TRANSFORMATION_COLOR = "\033[94m"  # Blue
    FINAL_STATE_COLOR = "\033[92m"  # Green
    ERROR_COLOR = "\033[91m"  # Red
    RESET_COLOR = "\033[0m"  # Reset to default

    print(f"{HEADER_COLOR}=== Advanced Data Structures Demonstration ==={RESET_COLOR}\n")
    
    # Define transformations with descriptive names
    transformations = [
        lambda s: s.upper(),                    # Transform 1: Convert to uppercase
        lambda s: s[::-1],                      # Transform 2: Reverse the string
        lambda s: ''.join(sorted(s)),           # Transform 3: Sort characters
        lambda s: s.replace('e', '@'),          # Transform 4: Replace 'e' with '@'
    ]

    # Demo data
    input_data = ["hello", "world", "morphological", "tree"]
    
    # 1. Demonstrate individual transformations
    print(f"{HEADER_COLOR}1. Transformation Process Example{RESET_COLOR}")
    print("-" * 40)
    for data in input_data:
        demo_transformations(data, transformations)
    
    # 2. Create and visualize Morphological Tree
    print(f"\n{HEADER_COLOR}2. Morphological Tree Construction and Visualization{RESET_COLOR}")
    print("-" * 40)
    try:
        tree = MorphologicalTree(input_data, transformations)
        tree.visualize()
    except Exception as e:
        print(f"{ERROR_COLOR}Error during tree visualization: {e}{RESET_COLOR}")
    
    # 3. Show final states of leaf nodes
    print(f"\n{HEADER_COLOR}3. Final Leaf Node States{RESET_COLOR}")
    print("-" * 40)
    for i, leaf in enumerate(tree.leaves, 1):
        print(f"\n{FINAL_STATE_COLOR}Leaf {i}:{RESET_COLOR}")
        print(f"  Original: {input_data[i-1]}")
        print(f"  Transformed: {leaf.data}")
        print(f"  Hash: {leaf.hash[:8]}...")
    
    # 4. Demonstrate Merkle Ring
    print(f"\n{HEADER_COLOR}4. Merkle Ring Demonstration{RESET_COLOR}")
    print("-" * 40)
    data_series = ["state1", "state2", "state3", "state4"]
    
    # Create Merkle Ring
    merkle_ring = MerkleRing(data_series)
    print("Original Merkle Ring:")
    merkle_ring.visualize()
    
    # 5. File Persistence Demonstration
    print(f"\n{HEADER_COLOR}5. TOML File Persistence{RESET_COLOR}")
    print("-" * 40)
    
    # Ensure the directory exists
    os.makedirs('output', exist_ok=True)
    toml_path = 'output/merkle_ring.toml'
    
    # Persist to a TOML file
    merkle_ring.to_toml(toml_path)
    print(f"Merkle Ring saved to {toml_path}")
    
    # Load from the TOML file
    loaded_ring = MerkleRing.from_toml(toml_path)
    print("\nLoaded Merkle Ring:")
    loaded_ring.visualize()

if __name__ == "__main__":
    main()