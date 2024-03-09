import sys
import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig

def setup_logger(n_parent_dirs=1, logging_config=None):
    current_dir = Path(__file__).resolve().parent

    # Check for 'logs' in the current directory and up to n_parent_dirs
    for _ in range(n_parent_dirs + 1):
        logs_dir = current_dir / 'logs'
        if logs_dir.exists():
            break  # Found an existing 'logs' directory
        current_dir = current_dir.parent
    else:  # No 'logs' directory found in the search path
        logs_dir = current_dir / 'logs'
        logs_dir.mkdir(exist_ok=True)

    log_file_path = logs_dir / 'setup.log'

    if logging_config is None:
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
                    'level': logging.INFO,
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'stream': 'ext://sys.stdout'
                },
                'file': {
                    'level': logging.INFO,
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

    logger = logging.getLogger()
    setattr(logger, 'parent', Path(__file__).resolve().parent)

    return logger

def main():
    try:
        sys.path.append((Path(__file__).resolve().parent / '..').resolve())  # is there adequate permission to expand the path?
    except Exception as e:
        print(e)
    finally:
        sys.path.extend([
            (Path(__file__).resolve().parent / 'src').resolve(),
            (Path(__file__).resolve().parent).resolve(),
        ])
    logger = setup_logger(n_parent_dirs=2)  # Example: Check 2 parent directories
    logger.info("main.py's __main__ is running")
    return 0

if __name__ == "__main__":
    main()
