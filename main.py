import sys
import logging
from pathlib import Path
from logging.config import dictConfig
import argparse
import importlib
import types
from importlib import import_module
from importlib.util import spec_from_file_location, module_from_spec
from types import SimpleNamespace

def main() -> logging.Logger:
    # logging for the dir the script is invoked from - global scope but not in the global namespace (logs... /x/logs.. /y/logs...)
    logs_dir = Path(__file__).resolve().parent / 'logs'
    logs_dir.mkdir(exist_ok=True)
    # explicit path for non .py-files (python does this for .py source files automatically)
    sys.path.append((Path(__file__).resolve().parent / '.').resolve())
    sys.path.append((Path(__file__).resolve().parent / 'src').resolve())
    current_dir = Path(__file__).resolve().parent
    # check for logging in parent dirs to the current dir
    while not (current_dir / 'logs').exists():
        # ascend to the highest logs dir
        current_dir = current_dir.parent
        if current_dir == Path('/'):
            break
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
                'datefmt': '%Y-%m-%d~%H:%M:%S%z'
            },
        },
        'handlers': {
            'console': {
                'level': None,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': None,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': logs_dir / 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 10
            }
        },
        'root': {
            'level': logging.INFO,
            'handlers': ['console', 'file']
        }
    }

    dictConfig(logging_config)

    logger = logging.getLogger(__name__)
    logger.info(f'Logging_dir {logs_dir}|'
                f'\nSource_file: {__file__}|'
                f'\nInvocation_dir: {Path(__file__).resolve().parent}|'
                f'\nWorking_dir: {current_dir}||')
    
    return logger

if __name__ == '__main__':
    ml = main()
    runtime = logging.getLogger('runtime')
    try:

        """Morphological source code requires a morphological compiler - python run time is that compiler, and compilation is asynchonous at runtime.
        So the source code is injected into the runtime as a module, and the module is executed in the runtime.
        """
        rt_module = types.ModuleType('cognos')
        rt_mod_name = 'cognos'
        rt_mod_path = sys.modules['__main__'].__file__
        # rt_mod_path = "/workspaces/cognos/src/launch.py"

        rt_mod = types.ModuleType(rt_mod_name)
        rt_mod.__file__ = rt_mod_path  # for importlib.util.spec_from_file_location
        sys.modules[rt_mod_name] = rt_mod  # rt in globals() or globals().__setitem__(rt_mod_name, rt_mod)

        with open(rt_mod_path, 'r') as f:  # open [[source code|rt_src]]
            rt_mod_src = f.read()

        code = compile(rt_mod_src, rt_mod_path, 'exec')

        # exec(code, rt_mod.__dict__)  # exec [[source code|rt_src]] in rt_mod.__dict__ --> inject frontmatter into obsidian architecture
    except Exception as e:
        runtime.error(f'||Error: {e}||')
        raise e
    finally:
        runtime.info(f'||runtime|{__file__}|| invoked from {Path(__file__).resolve().parent}||')


    # importlib.import_module(rt_mod_name)
    for mod in SimpleNamespace(
        globals=globals(),
        locals=locals(),
        sys_modules=sys.modules
    ).sys_modules:
        if isinstance(mod, str):
            runtime.info(f'||{mod}||')

    ml.info(f'||{rt_mod_name}|| concluded...')