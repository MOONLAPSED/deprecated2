import sys
import importlib
from types import SimpleNamespace, ModuleType
"""This provides a way to dynamically generate modules and inject code into them at runtime. This is useful for creating a module from a source code string or AST (or cognos tree), and then executing the module in the runtime.
Runtime module (main) is the module that the source code is injected into | t_module is a tree of modules dynamically pulled from SimpleNamespace + dataclasses"""
t_module = ModuleType('cognos')
rt_mod_path = sys.modules['__main__'].__file__
sys.modules['cognos'] = t_module
# This means now Python will recognize 'cognos' as a valid module that can be imported even though it was created dynamically.

tmod=SimpleNamespace()
tmod.__name__ = 'cognos'
tmod.__file__ = rt_mod_path
tmod.__package__ = 'cognos'
tmod.__path__ = None
tmod.__doc__ = None
# advanced funcs tbd like __loaders__ (if needed)
t_module.__dict__.update(tmod.__dict__)
