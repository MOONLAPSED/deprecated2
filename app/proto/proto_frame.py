import sys
import os

"""
Defines the bytes object frame 'protocol' for IPC
"""

class Frame:
    """
    This class manages the serialization and deserialization of frames.
    """
    # Use bytes literals (prefixed with b) since they will be used in binary framing
    HEADER_REQUEST = b'01'
    HEADER_RESPONSE = b'02'
    TYPES = (HEADER_REQUEST, HEADER_RESPONSE)
    HeaderType = bytes
    print(HEADER_REQUEST)
    assert len(HEADER_REQUEST) == 1

    def __init__(self, header: HeaderType, payload: bytes):
        self.header = header
        self.payload = payload

    def serialize(self) -> bytes:
        """
        Serialize the Frame object into bytes.

        Returns:
            bytes: Serialized representation of the Frame.
        """
        return self.header + self.payload

    @classmethod
    def deserialize(cls, frame_bytes: bytes) -> 'Frame':
        """
        Deserialize bytes into a Frame object.

        Args:
            frame_bytes (bytes): Bytes representing a Frame.

        Returns:
            Frame: Deserialized Frame object.
        """
        header = frame_bytes[:1]
        payload = frame_bytes[1:]
        return cls(header, payload)

# Usage example:
if __name__ == "__main__":
    # Create a Frame object
    frame = Frame(Frame.HEADER_REQUEST, b'This is a payload')

    # Serialize the Frame
    serialized_frame = frame.serialize()
    print("Serialized Frame:", serialized_frame.hex())

    # Deserialize the Frame
    deserialized_frame = Frame.deserialize(serialized_frame)
    print("Deserialized Frame - Header:", deserialized_frame.header)
    print("Deserialized Frame - Payload:", deserialized_frame.payload)