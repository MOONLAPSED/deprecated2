import asyncio
import dataclasses
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Union
import inspect
import ast

# A base class for self-validating objects
@dataclass(frozen=True, slots=True)
class AtomicModel:
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        object.__setattr__(self, "properties", self.validate_properties(self.properties))

    @staticmethod
    def validate_properties(properties: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(properties, dict):
            raise TypeError("Properties must be a dictionary.")
        return properties

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

# A decorator for defining formal theories
def FormalTheory(atom_cls: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        obj = atom_cls(*args, **kwargs)
        if not hasattr(obj, "validate_properties"):
            raise TypeError("Class must implement 'validate_properties' method.")
        obj.validate_properties(obj.properties)
        return obj
    return wrapper

# A runtime manager
class RuntimeManager:
    def __init__(self):
        self.registry = {}

    def register(self, name: str, atomic_instance: AtomicModel):
        if name in self.registry:
            raise ValueError(f"An instance with name {name} is already registered.")
        self.registry[name] = atomic_instance

    def get_instance(self, name: str) -> AtomicModel:
        return self.registry.get(name)

    def run_tasks(self):
        async def task_runner():
            for name, instance in self.registry.items():
                print(f"Running task for: {name}")
                await asyncio.sleep(0.1)  # Simulate some async operation
        asyncio.run(task_runner())

# An example concrete atomic model
@FormalTheory
class MyAtomicModel(AtomicModel):
    pass

# AST parsing utility
def parse_code_to_ast(code: str) -> ast.AST:
    try:
        return ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}")

# Main application logic
if __name__ == "__main__":
    # Create instances
    instance1 = MyAtomicModel(name="atom1", properties={"mass": 1.0, "charge": -1.0})
    instance2 = MyAtomicModel(name="atom2", properties={"mass": 1.2, "charge": 1.0})

    # Initialize runtime manager
    manager = RuntimeManager()

    # Register instances
    manager.register("atom1", instance1)
    manager.register("atom2", instance2)

    # Print instances as dictionaries
    print(instance1.to_dict())
    print(instance2.to_dict())

    # Run tasks in the runtime manager
    manager.run_tasks()

    # AST example
    code_snippet = """
def example_function(x):
    return x * 2
"""
    parsed_ast = parse_code_to_ast(code_snippet)
    print(ast.dump(parsed_ast, indent=4))
