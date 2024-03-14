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
    """
    Configures logging for the app.

    Args:
        None

    Returns:
        logging.Logger: The logger for the module.
    """
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
    

if __name__ == '__main__':
    ml = main()
    runtime = logging.getLogger('runtime')
    runtime.info(f'||{__file__}_runtime()||')

    # importlib.import_module(rt_mod_name)
    for mod in SimpleNamespace(
        globals=globals(),
        locals=locals(),
        sys_modules=sys.modules
    ).sys_modules:
        if isinstance(mod, str):
            runtime.info(f'||{mod}_runtime()||')
            import_module(mod)

    sys.exit(0)
