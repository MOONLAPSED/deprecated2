import abc
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional, Union
import json
import inspect
import asyncio


# Abstract Base Class
class AtomicModel(abc.ABC):
    """
    Abstract base class to define a nominative reflective architecture
    for self-validating atomic elements.
    """
    @abc.abstractmethod
    def validate(self) -> bool:
        """Validate the model's data."""
        pass

    @abc.abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the model into a dictionary."""
        pass


# Concrete Implementation
@dataclass(frozen=True, slots=True)
class AtomicTheory(AtomicModel):
    """
    Represents an atomic element of the system.
    Designed to be immutable and efficient using frozen=True and slots=True.
    """
    name: str
    value: Union[int, float, str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    post_init_validated: bool = field(init=False, default=False)

    def __post_init__(self):
        # Perform validation after initialization
        object.__setattr__(self, "post_init_validated", self.validate())

    def validate(self) -> bool:
        """Validate the AtomicTheory instance."""
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("Invalid name: must be a non-empty string.")
        if not isinstance(self.value, (int, float, str)):
            raise ValueError("Invalid value: must be int, float, or str.")
        if not isinstance(self.metadata, dict):
            raise ValueError("Invalid metadata: must be a dictionary.")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the model into a dictionary."""
        return asdict(self)


# Utility Function for Reflection
def reflect_atomic_model(obj: AtomicModel) -> str:
    """
    Reflects the details of the given AtomicModel instance.
    """
    if not isinstance(obj, AtomicModel):
        raise TypeError("Object must be an instance of AtomicModel.")
    return json.dumps(obj.to_dict(), indent=4)


# Asynchronous Execution Example
async def process_atomic_elements(elements: List[AtomicTheory]):
    """
    Asynchronously processes a list of AtomicTheory instances.
    """
    for element in elements:
        await asyncio.sleep(0.01)
        print(f"Processed: {reflect_atomic_model(element)}")


# Main Application Logic
def main():
    try:
        # Create instances of AtomicTheory
        element1 = AtomicTheory(name="Element1", value=42, metadata={"type": "integer"})
        element2 = AtomicTheory(name="Element2", value="Hello", metadata={"type": "string"})

        # Reflect atomic elements
        print("Reflection of Atomic Elements:")
        print(reflect_atomic_model(element1))
        print(reflect_atomic_model(element2))

        # Asynchronous processing
        elements = [element1, element2]
        asyncio.run(process_atomic_elements(elements))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
