import ast
import inspect
import json
from typing import Any, Dict, List, Type, Union, Optional
from types import MethodType, MethodWrapperType

class LogicalMRO:
    def __init__(self):
        self.mro_structure = {
            "class_hierarchy": {},
            "method_resolution": {},
            "super_calls": {}
        }

    def encode_class(self, cls: Type) -> Dict[str, Any]:
        """Encodes details of a class, its methods, and super calls."""
        return {
            "name": cls.__name__,
            "mro": [c.__name__ for c in cls.__mro__],
            "methods": {
                name: {
                    "defined_in": cls.__name__,
                    "super_calls": self._analyze_super_calls(getattr(cls, name)),
                    "overrides": self._find_method_override(name, cls),
                    "signature": str(inspect.signature(getattr(cls, name))) if callable(getattr(cls, name)) else ""
                }
                for name, method in cls.__dict__.items()
                if isinstance(method, (MethodType, MethodWrapperType)) or callable(method)
            }
        }

    def _analyze_super_calls(self, method) -> List[Dict[str, Union[str, int]]]:
        """Analyzes super() calls within a method to capture explicit or implicit inheritance."""
        try:
            source = inspect.getsource(method)
            tree = ast.parse(source)
            super_calls = []
            
            class SuperVisitor(ast.NodeVisitor):
                def visit_Call(self, node):
                    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Call):
                        if isinstance(node.func.value.func, ast.Name) and node.func.value.func.id == 'super':
                            super_calls.append({
                                "line": node.lineno,
                                "method": node.func.attr,
                                "type": "explicit" if node.func.value.args else "implicit"
                            })
                    elif isinstance(node.func, ast.Name) and node.func.id == 'super':
                        super_calls.append({
                            "line": node.lineno,
                            "type": "explicit" if node.args else "implicit"
                        })
                    self.generic_visit(node)

            SuperVisitor().visit(tree)
            return super_calls
        except Exception:
            return []

    def _find_method_override(self, method_name: str, cls: Type) -> Optional[str]:
        """Identifies if the method overrides a method in a superclass."""
        for base in cls.__mro__[1:]:
            if method_name in base.__dict__:
                return base.__name__
        return None

    def create_logical_mro(self, *classes: Type) -> Dict[str, Any]:
        """Constructs the logical MRO structure, storing data about class methods and resolution order."""
        mro_logic = {
            "classes": {},
            "resolution_order": {},
            "method_dispatch": {}
        }

        for cls in classes:
            class_info = self.encode_class(cls)
            mro_logic["classes"][cls.__name__] = class_info
            
            for method_name, method_info in class_info["methods"].items():
                mro_logic["method_dispatch"][f"{cls.__name__}.{method_name}"] = {
                    "resolution_path": [
                        base.__name__ for base in cls.__mro__
                        if hasattr(base, method_name)
                    ],
                    "super_calls": method_info["super_calls"],
                    "overrides": method_info["overrides"]
                }

        return mro_logic

    def __repr__(self):
        def class_to_s_expr(cls_name: str) -> str:
            cls_info = self.mro_structure["classes"][cls_name]
            methods = [f"(method {name} (defined_in {info['defined_in']}) "
                       f"{' '.join([f'(super {call["method"]})' for call in info['super_calls']])})"
                       for name, info in cls_info["methods"].items()]
            return f"(class {cls_name} (mro {' '.join(cls_info['mro'])}) {' '.join(methods)})"

        s_expressions = [class_to_s_expr(cls) for cls in self.mro_structure["classes"]]
        return "\n".join(s_expressions)

    def to_json(self) -> str:
        """Returns a JSON representation of the logical MRO structure."""
        return json.dumps(self.mro_structure, indent=2)

    def to_graph(self) -> str:
        """Returns a simple graph representation of class hierarchies and method calls."""
        graph = []
        for cls_name, cls_info in self.mro_structure["classes"].items():
            graph.append(f"{cls_name} -> {' -> '.join(cls_info['mro'])}")
            for method_name, method_info in cls_info["methods"].items():
                if method_info["super_calls"]:
                    graph.append(f"  {method_name} -> {', '.join(call['method'] for call in method_info['super_calls'])}")
        return "\n".join(graph)


class LogicalMROExample:
    def __init__(self):
        self.mro_analyzer = LogicalMRO()

    def analyze_classes(self, *classes: Type):
        """Analyzes the given classes for MRO, returning structured, human-readable representations."""
        class_structure = self.mro_analyzer.create_logical_mro(*classes)
        self.mro_analyzer.mro_structure = class_structure
        return {
            "logical_structure": class_structure,
            "s_expressions": str(self.mro_analyzer),
            "json_structure": self.mro_analyzer.to_json(),
            "graph_structure": self.mro_analyzer.to_graph(),
            "method_resolution": class_structure["method_dispatch"]
        }

# Example classes
class A:
    def a(self):
        print("a")
    def b(self):
        print("a.b method")
        super().b()

class C:
    def b(self):
        print("c.b method")
    def c(self):
        print("c")

class B(A, C):
    def __init__(self):
        super().__init__()
    def b(self):
        print("b.b method")
        super().b()
        self.c()
    def a(self):
        print("override")

def demonstrate():
    analyzer = LogicalMROExample()
    result = analyzer.analyze_classes(A, B, C)
    
    print("S-expression representation:\n")
    print(result["s_expressions"])
    print("\nDetailed JSON structure:\n")
    print(result["json_structure"])
    print("\nGraph structure:\n")
    print(result["graph_structure"])
    
    # Test MRO behavior
    print("\nActual method resolution in class B:")
    b = B()
    b.b()

if __name__ == "__main__":
    demonstrate()