from typing import Any, Callable, Dict, List, Tuple
from functools import wraps
from dataclasses import dataclass, field, asdict
from collections.abc import Hashable
import inspect
import ast

# === Utility Functions ===

def validate_instance(obj: Any, expected_type: Any) -> None:
    """Ensures the object is of the expected type."""
    if not isinstance(obj, expected_type):
        raise TypeError(f"Expected type {expected_type}, got {type(obj)} instead.")

def singleton(cls: Callable) -> Callable:
    """Ensures a class is a singleton."""
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

def debug_log(func: Callable) -> Callable:
    """Decorator to log the function call and its return value."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = ", ".join([repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()])
        print(f"Calling {func.__name__}({arg_str})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result
    return wrapper

# === Core Data Classes ===

@dataclass(frozen=True, slots=True)
class AtomicModel:
    """A base immutable model with slots for runtime efficiency."""
    name: str
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the AtomicModel to a dictionary."""
        return asdict(self)

    def __post_init__(self):
        """Validate attributes for immutability and hashability."""
        for key, value in self.attributes.items():
            if not isinstance(key, Hashable):
                raise ValueError(f"Attribute key {key} is not hashable.")
            if isinstance(value, (list, dict, set)):
                raise ValueError(f"Attribute value for {key} must be immutable, got {type(value)}.")

@dataclass
class AtomicTheory:
    """Represents an advanced atomic structure."""
    model: AtomicModel
    annotations: Dict[str, Any] = field(default_factory=dict)

    @debug_log
    def validate(self) -> bool:
        """Validate the AtomicTheory based on annotations."""
        for key, annotation in self.annotations.items():
            if key not in self.model.attributes:
                raise KeyError(f"Missing key {key} in model attributes.")
            if not isinstance(self.model.attributes[key], annotation):
                raise TypeError(f"Key {key} should be {annotation}, got {type(self.model.attributes[key])}.")
        return True

# === Tokenization and I/O ===

@debug_log
def tokenize_string(data: str) -> List[str]:
    """Simple tokenizer that splits a string into words."""
    return data.split()

@debug_log
def process_io(data: str) -> List[str]:
    """Processes input and outputs a tokenized version."""
    return tokenize_string(data)

# === Reflection and AST ===

@dataclass
class ReflectiveModel:
    """Model to support reflective capabilities."""
    source: str = field(default_factory=str)

    @debug_log
    def parse_ast(self) -> ast.AST:
        """Parse the source code into an AST."""
        return ast.parse(self.source)

    @debug_log
    def modify_ast(self) -> str:
        """Modifies and compiles AST."""
        tree = self.parse_ast()
        # Example: Add a dummy node
        tree.body.insert(0, ast.Pass())
        return compile(tree, filename="<ast>", mode="exec")

# === Example Usage ===

if __name__ == "__main__":
    # Create a model and theory
    atomic_model = AtomicModel(name="Sample", attributes={"mass": 1.0, "charge": -1.0})
    atomic_theory = AtomicTheory(model=atomic_model, annotations={"mass": float, "charge": float})

    # Validate the theory
    try:
        if atomic_theory.validate():
            print("AtomicTheory is valid.")
    except Exception as e:
        print(f"Validation failed: {e}")

    # Tokenize a string
    example_string = "The quick brown fox jumps over the lazy dog."
    tokens = process_io(example_string)
    print(f"Tokens: {tokens}")

    # Reflection
    reflective_model = ReflectiveModel(source="print('Hello, world!')")
    reflective_model.modify_ast()
