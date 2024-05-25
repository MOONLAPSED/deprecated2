from typing import Optional

# Define a simple linked list node for the scratch arena
class Node:
    def __init__(self, size: int):
        self.data = bytearray(size)
        self.next: Optional['Node'] = None
        self.size = size
        self.used = 0

class ScratchArena:
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size
        self.head = Node(chunk_size)
        self.current = self.head

    def allocate(self, size: int) -> memoryview:
        if size > self.chunk_size:
            raise ValueError("Allocation size exceeds chunk size")

        # If there's not enough space in the current chunk, create a new one
        if self.current.used + size > self.current.size:
            new_node = Node(self.chunk_size)
            self.current.next = new_node
            self.current = new_node

        # Allocate memory from the current chunk
        start = self.current.used
        self.current.used += size
        return memoryview(self.current.data)[start:start + size]

    def reset(self):
        # Reset all chunks for reuse
        node = self.head
        while node:
            node.used = 0
            node = node.next
        self.current = self.head

# Example usage
arena = ScratchArena(chunk_size=1024)  # Create a scratch arena with chunks of 1024 bytes

# Allocate some memory
data1 = arena.allocate(100)
data2 = arena.allocate(200)

# Fill allocated memory with some data
data1[:] = b'a' * 100
data2[:] = b'b' * 200

print(bytes(data1))
print(bytes(data2))

# Reset the arena for reuse
arena.reset()
