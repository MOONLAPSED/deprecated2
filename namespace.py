import sys
import importlib
import types

"""Morphological source code requires a morphological compiler - python run time is that compiler, and compilation is asynchonous at runtime."""

# rt_module = types.ModuleType('cognos')
rt_mod_name = 'cognos'
# rt_mod_path = sys.modules['__main__'].__file__
rt_mod_path = "/workspaces/cognos/src/launch.py"

rt_mod = types.ModuleType(rt_mod_name)
rt_mod.__file__ = rt_mod_path  # for importlib.util.spec_from_file_location
sys.modules[rt_mod_name] = rt_mod  # rt in globals() or globals().__setitem__(rt_mod_name, rt_mod)

with open(rt_mod_path, 'r') as f:  # open [[source code|rt_src]]
    rt_mod_src = f.read()

code = compile(rt_mod_src, rt_mod_path, 'exec')

exec(code, rt_mod.__dict__)  # exec [[source code|rt_src]] in rt_mod.__dict__ --> inject frontmatter into obsidian architecture