import hashlib
import multiprocessing
import ctypes
import struct
from dataclasses import dataclass, field
from typing import Optional, List, Union, Callable, Any
from concurrent.futures import ProcessPoolExecutor, as_completed


# SIMD-inspired Utility Functions and Classes
class SIMDVector:
    """A SIMD-like vector implementation for parallel processing."""
    
    @staticmethod
    def create_lanes(data: List[Any], lane_type=ctypes.c_uint32):
        """
        Create a SIMD-like lane structure from input data.
        Pads or truncates data to fit exact lane width.
        """
        # Determine lane width based on the ctypes type
        lane_width = ctypes.sizeof(lane_type)
        
        # Create a ctypes array with appropriate type and size
        ArrayType = lane_type * len(data)
        
        # Convert data to the specified lane type
        lanes = ArrayType(*[lane_type(item) for item in data])
        
        return lanes
    
    @staticmethod
    def parallel_reduce(data: List[Any], 
                        reduce_func: Callable, 
                        num_processes: Optional[int] = None):
        """
        Perform a parallel reduction operation across data lanes.
        
        :param data: List of input data
        :param reduce_func: Function to apply to each chunk of data
        :param num_processes: Number of processes to use (defaults to CPU count)
        :return: Reduced result
        """
        if num_processes is None:
            num_processes = multiprocessing.cpu_count()
        
        # Split data into chunks for parallel processing
        chunk_size = max(1, len(data) // num_processes)
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        results = []
        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            future_to_chunk = {
                executor.submit(reduce_func, chunk): chunk 
                for chunk in chunks
            }
            
            for future in as_completed(future_to_chunk):
                results.append(future.result())
        
        # Final reduction of results
        return reduce(reduce_func, results)


def generate_color_from_hash(hash_str: str, dark_mode: bool = True) -> str:
    """
    Generate an ANSI escape color code based on the first 6 characters of a hash.
    Supports both dark and light mode color generation.
    """
    color_value = int(hash_str[:6], 16)  # Convert the first 6 chars to an integer
    r = (color_value >> 16) % 256
    g = (color_value >> 8) % 256
    b = color_value % 256
    
    if dark_mode:
        # Darken colors for CLI readability
        r = r // 2
        g = g // 2
        b = b // 2
    
    return f"\033[38;2;{r};{g};{b}m"


def hash_data(data: Union[str, bytes], algorithm: str = 'sha256') -> str:
    """
    Enhanced hashing function supporting multiple algorithms and input types.
    
    :param data: Input data to hash
    :param algorithm: Hashing algorithm to use
    :return: Hex digest of the hash
    """
    if isinstance(data, str):
        data = data.encode()
    
    if algorithm == 'sha256':
        return hashlib.sha256(data).hexdigest()
    elif algorithm == 'sha3_256':
        return hashlib.sha3_256(data).hexdigest()
    else:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")


class SIMDMerkleNode:
    """
    Enhanced Merkle tree node with SIMD-like properties and color representation.
    """
    def __init__(self, 
                 data: Union[str, bytes, List[Any]], 
                 node_type: str = 'leaf', 
                 hash_algo: str = 'sha256'):
        """
        Initialize a Merkle tree node with SIMD-inspired features.
        
        :param data: Input data for the node
        :param node_type: Type of node (leaf or internal)
        :param hash_algo: Hashing algorithm to use
        """
        self.node_type = node_type
        self.hash_algo = hash_algo
        
        # Handle different input types
        if isinstance(data, list):
            # SIMD-like lane processing for list inputs
            self.lanes = SIMDVector.create_lanes(data)
            self.data = data
            self.hash = self._compute_lane_hash()
        else:
            self.lanes = None
            self.data = data
            self.hash = hash_data(data, hash_algo)
        
        # Generate short hash and color
        self.short_hash = self.hash[:6]
        self.color = generate_color_from_hash(self.hash)
    
    def _compute_lane_hash(self) -> str:
        """
        Compute hash for SIMD-like lane data.
        """
        if self.lanes is None:
            return hash_data(self.data, self.hash_algo)
        
        # Convert lanes to bytes for hashing
        lane_bytes = bytes(self.lanes)
        return hash_data(lane_bytes, self.hash_algo)
    
    def __repr__(self):
        """
        Colorful representation of the node.
        """
        data_repr = str(self.data)[:20]  # Truncate long data
        return f"{self.color}[{self.node_type.capitalize()}:{data_repr}][{self.short_hash}]\033[0m"
    
    def lane_xor(self, other: 'SIMDMerkleNode') -> str:
        """
        Perform lane-wise XOR between two nodes.
        """
        if self.lanes is None or other.lanes is None:
            return hash_data(self.hash + other.hash)
        
        # Perform lane-wise XOR
        xor_lanes = [a ^ b for a, b in zip(self.lanes, other.lanes)]
        xor_bytes = bytes(xor_lanes)
        return hash_data(xor_bytes)


class SIMDMerkleTree:
    """
    Advanced Merkle tree with SIMD-like processing capabilities.
    """
    def __init__(self, 
                 data_chunks: List[Union[str, bytes, List[Any]]], 
                 hash_algo: str = 'sha256', 
                 max_workers: Optional[int] = None):
        """
        Initialize a Merkle tree with parallel processing.
        
        :param data_chunks: Input data chunks
        :param hash_algo: Hashing algorithm to use
        :param max_workers: Maximum number of worker processes
        """
        self.hash_algo = hash_algo
        self.max_workers = max_workers or multiprocessing.cpu_count()
        
        # Parallel node creation
        self.leaves = self._create_leaves(data_chunks)
        self.root = self._build_tree()
    
    def _create_leaves(self, data_chunks: List[Union[str, bytes, List[Any]]]) -> List[SIMDMerkleNode]:
        """
        Create leaf nodes in parallel.
        """
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            leaves = list(executor.map(
                lambda d: SIMDMerkleNode(d, node_type='leaf', hash_algo=self.hash_algo), 
                data_chunks
            ))
        return leaves
    
    def _build_tree(self) -> SIMDMerkleNode:
        """
        Build the Merkle tree using parallel processing.
        """
        nodes = self.leaves.copy()
        
        while len(nodes) > 1:
            new_level = []
            
            # Process nodes in pairs
            for i in range(0, len(nodes), 2):
                if i + 1 < len(nodes):
                    # Create internal node from two children
                    internal_data = nodes[i].hash + nodes[i+1].hash
                    internal_node = SIMDMerkleNode(
                        internal_data, 
                        node_type='internal', 
                        hash_algo=self.hash_algo
                    )
                    new_level.append(internal_node)
                else:
                    # Duplicate last node if odd number of nodes
                    new_level.append(nodes[i])
            
            nodes = new_level
        
        return nodes[0]
    
    def verify_integrity(self, original_data: List[Union[str, bytes, List[Any]]]) -> bool:
        """
        Verify the integrity of the Merkle tree against original data.
        """
        # Recreate the tree and compare root hashes
        new_tree = SIMDMerkleTree(original_data, hash_algo=self.hash_algo)
        return self.root.hash == new_tree.root.hash
    
    def visualize(self, max_depth: int = 3):
        """
        Colorful visualization of the Merkle tree structure.
        
        :param max_depth: Maximum depth to visualize
        """
        def _traverse(node: SIMDMerkleNode, depth: int = 0):
            if depth > max_depth:
                return
            
            print(f"{'  ' * depth}{node}")
            
            if node.node_type == 'internal':
                # Recursively visualize children (this is a placeholder)
                # In a full implementation, you'd track child nodes
                pass
        
        print(f"{self.root.color}Merkle Tree Visualization:\033[0m")
        _traverse(self.root)


# Example Usage
def main():
    # Demonstrate SIMD-like Merkle Tree with various data types
    data_chunks = [
        "apple", 
        "banana", 
        [1, 2, 3],  # SIMD-like lane processing
        b"cherry",
        [4.5, 6.7, 8.9]
    ]
    
    # Create Merkle tree with parallel processing
    merkle_tree = SIMDMerkleTree(data_chunks)
    
    # Visualize the tree
    merkle_tree.visualize()
    
    # Demonstrate integrity verification
    print("\nIntegrity Check:", merkle_tree.verify_integrity(data_chunks))
    
    # Lane-wise XOR demonstration
    leaf1, leaf2 = merkle_tree.leaves[:2]
    xor_result = leaf1.lane_xor(leaf2)
    print(f"\nLane-wise XOR Result: {xor_result}")


if __name__ == "__main__":
    main()