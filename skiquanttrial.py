#!/usr/bin/env python3
"""
Quantum Morphological Information Processing System

This module integrates quantum state processing, SKI combinators, 
Maxwell's Demon sorting, and morphological tree structures with 
advanced hashing and transformation capabilities.

Key Concepts:
- Quantum superposition and state collapse
- SKI combinator information processing
- Energy-based sorting (Maxwell's Demon)
- Morphological transformations
- Merkle-like data structures
"""

import hashlib
import math
import os
import random
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import (
    Any, Callable, Generic, List, Optional, Protocol, 
    TypeVar, Union
)

# Type Variables for Generic Programming
T = TypeVar('T')
S = TypeVar('S')

# Utility Functions for Hashing and Color Generation
def hash_data(data: Union[str, bytes]) -> str:
    """Generate a SHA-256 hash of the given data."""
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()

def generate_color_from_hash(hash_str: str) -> str:
    """Generate an ANSI color code based on the hash string."""
    color_value = int(hash_str[:6], 16)
    r = (color_value >> 16) % 256
    g = (color_value >> 8) % 256
    b = color_value % 256
    return f"\033[38;2;{r};{g};{b}m"

# Quantum State Processing
@dataclass
class QuantumState(Generic[T]):
    """Represents a quantum superposition of states."""
    possibilities: list[T]
    amplitudes: list[float]

    def __init__(self, possibilities: list[T]):
        n = len(possibilities)
        self.possibilities = possibilities
        self.amplitudes = [1 / math.sqrt(n)] * n

    def collapse(self) -> T:
        """Collapses the wave function to a single state."""
        return random.choices(self.possibilities, weights=self.amplitudes)[0]

# SKI Combinator for Functional Transformations
class SKICombinator:
    """Implementation of SKI combinators for information processing."""
    @staticmethod
    def S(f: Callable, g: Callable, x: Any) -> Any:
        """
        S combinator: S f g x = f x (g x)
        Ensure all arguments are callable
        """
        return f(x)(g(x))

    @staticmethod
    def K(x: T, y: Any) -> T:
        """K combinator returns the first argument"""
        return x

    @staticmethod
    def I(x: T) -> T:
        """Identity combinator"""
        return x

# Maxwell's Demon for Energy-Based Sorting
class MaxwellDemon:
    """Information sorter based on Maxwell's Demon concept."""
    def __init__(self, energy_threshold: float = 0.5):
        self.energy_threshold = energy_threshold
        self.high_energy = deque()
        self.low_energy = deque()

    def sort(self, particle: Any, energy: float) -> None:
        if energy > self.energy_threshold:
            self.high_energy.append(particle)
        else:
            self.low_energy.append(particle)

    def get_sorted(self) -> tuple[deque, deque]:
        return self.high_energy, self.low_energy

# Quantum Processor for Complex Information Processing
class QuantumProcessor:
    """Main quantum information processing system."""
    def __init__(self):
        self.ski = SKICombinator()
        self.demon = MaxwellDemon()
        self._collapsed = False

    def apply_ski(self, data: T, transform: Callable[[T], S]) -> S:
        """Apply SKI combinator transformation."""
        def transformed_func(x):
            transformed = transform(x)
            return lambda _: transformed

        # Use S combinator with the transformed function
        return self.ski.S(
            transformed_func,  # First function
            self.ski.I,        # Second function (identity)
            data               # Input data
        )

    def measure(self, quantum_state: QuantumState) -> T:
        """Collapse the quantum state to a single outcome."""
        return quantum_state.collapse()

    def process(self, data: list[T]) -> QuantumState:
        """Convert data into a quantum superposition."""
        return QuantumState(data)

# Morphological Node for State Reflection
class MorphType(Protocol):
    def morph(self) -> None:
        """Dynamically adapt or evolve"""

@dataclass
class MorphologicalNode:
    """A node capable of self-reflection and transformation."""
    data: str
    hash: str = field(init=False)
    morph_operations: List[Callable[[str], str]] = field(default_factory=list)

    def __post_init__(self):
        """Initialize the node by calculating its initial hash and applying morphs."""
        self.hash = self.calculate_hash(self.data)
        self.reflect_and_morph()

    def calculate_hash(self, input_data: str) -> str:
        """Calculate hash of data, reflects state."""
        return hash_data(input_data)

    def morph(self) -> None:
        """Simulate adapting to its environment via self-reflection."""
        for operation in self.morph_operations:
            self.data = operation(self.data)

    def reflect_and_morph(self) -> None:
        """Run self-modifications and update hash."""
        if self.morph_operations:
            self.morph()
            self.hash = self.calculate_hash(self.data)

# Morphological Tree for Complex Data Structures
class MorphologicalTree:
    def __init__(self, data_chunks: List[str], transformations: List[Callable[[str], str]]):
        """
        Initialize a MorphologicalTree with data chunks and transformation operations.
        
        :param data_chunks: List of initial data to create leaf nodes
        :param transformations: List of transformation functions to apply to nodes
        """
        self.leaves = [MorphologicalNode(data, morph_operations=transformations) for data in data_chunks]
        self.root = self.build_tree(self.leaves)

    def build_tree(self, nodes: List[MorphologicalNode]):
        """
        Recursively build a binary tree from the input nodes.
        
        :param nodes: List of nodes to be organized into a tree
        :return: Root node of the constructed tree
        """
        @dataclass
        class InternalNode:
            left: MorphologicalNode
            right: Optional[MorphologicalNode] = None
            hash: str = field(init=False)

            def __post_init__(self):
                """Calculate hash by combining left and right node hashes."""
                combined = self.left.hash + (self.right.hash if self.right else '')
                self.hash = hash_data(combined)

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
        if hasattr(node, 'right'):  # Internal node
            print(f"{prefix}Internal Node [Hash: {generate_color_from_hash(node.hash)}{node.hash[:8]}...\033[0m]")
            print(f"{prefix}├── Left:")
            self.print_node_info(node.left, prefix + "│   ")
            if node.right:
                print(f"{prefix}└── Right:")
                self.print_node_info(node.right, prefix + "    ")
        else:  # Leaf node (MorphologicalNode)
            print(f"{prefix}Leaf Node:")
            print(f"{prefix}├── Data: {node.data}")
            print(f"{prefix}└── Hash: {generate_color_from_hash(node.hash)}{node.hash[:8]}...\033[0m")

    def visualize(self):
        """Print a visual representation of the tree."""
        print("\nTree Structure:")
        print("==============")
        self.print_node_info(self.root)

# Quantum Morph for State Manipulation
class Morph:
    """Represents a morphable quantum state."""
    def __init__(self, state: QuantumState, processor: QuantumProcessor):
        self.state = state
        self.processor = processor
        self.history = []

    def transition(self, transform: Callable[[T], S]) -> None:
        """Transition the state using a transformation function."""
        self.state = QuantumState([
            self.processor.apply_ski(possibility, transform)
            for possibility in self.state.possibilities
        ])

    def measure(self) -> T:
        """Collapse the state to a single outcome."""
        result = self.processor.measure(self.state)
        self.history.append(result)
        return result

# Pipeline Functions for Complex Data Processing
def transducer_pipeline(data: list[T], energy_function: Callable[[T], float], processor: QuantumProcessor) -> tuple[list[S], tuple[deque, deque]]:
    """Pipeline to process, transform, and sort data."""
    # Process data into quantum superposition
    quantum_state = processor.process(data)

    # Measure state
    measured = processor.measure(quantum_state)

    # Apply transformation
    transformed = processor.apply_ski(measured, lambda x: x * 2 if isinstance(x, (int, float)) else x)

    # Sort using Maxwell's Demon
    for item in data:
        energy = energy_function(item)
        processor.demon.sort(item, energy)

    return transformed, processor.demon.get_sorted()

def omega_pipeline(omega: list[T], transform: Callable[[T], S], energy_function: Callable[[T], float]) -> tuple[list[S], tuple[deque, deque]]:
    """Processes omega algebra with transformations and sorting."""
    processor = QuantumProcessor()
    morph = Morph(QuantumState(omega), processor)

    # Transform Morph using SKI
    morph.transition(transform)

    # Measure final state
    final_state = morph.measure()

    # Use transducer pipeline for sorting
    _, sorted_states = transducer_pipeline(omega, energy_function, processor)

    return final_state, sorted_states

# Demonstration and Main Execution
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

def omega_demo():
    """Demonstrate quantum processing and morphological transformations."""
    # Quantum Omega Pipeline Demo
    omega = [1, 2, 3, 4, 5]

    # Define transformation and energy functions
    transform = lambda x: x * 3
    energy_function = lambda x: abs(math.cos(x))

    # Run the pipeline
    final_state, (high, low) = omega_pipeline(omega, transform, energy_function)

    print(f"Final measured state: {final_state}")
    print(f"High energy states: {list(high)}")
    print(f"Low energy states: {list(low)}")

def main():
    """
    Comprehensive demonstration of advanced data processing capabilities.
    """
    # ANSI color codes for styling
    HEADER_COLOR = "\033[95m"  # Magenta
    RESET_COLOR = "\033[0m"  # Reset to default

    print(f"{HEADER_COLOR}=== Quantum Morphological Information Processing Demonstration ==={RESET_COLOR}\n")
    
    # Quantum Omega Demo
    print(f"{HEADER_COLOR}1. Quantum Omega Pipeline{RESET_COLOR}")
    omega_demo()

    # Define transformations
    transformations = [
        lambda s: s.upper(),                    # Transform 1: Convert to uppercase
        lambda s: s[::-1],                      # Transform 2: Reverse the string
        lambda s: ''.join(sorted(s)),           # Transform 3: Sort characters
        lambda s: s.replace('e', '@'),          # Transform 4: Replace 'e' with '@'
    ]

    # Morphological Tree Demo
    input_data = ["hello", "world", "morphological", "tree"]
    
    print(f"\n{HEADER_COLOR}2. Morphological Tree Demonstration{RESET_COLOR}")
    tree = MorphologicalTree(input_data, transformations)
    tree.visualize()

    # Transformation Demonstrations
    print(f"\n{HEADER_COLOR}3. Individual Transformations{RESET_COLOR}")
    for data in input_data:
        demo_transformations(data, transformations)

if __name__ == "__main__":
    main()