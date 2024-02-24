#! /usr/bin/env python3  # setup.py
import sys
import logging
import argparse
from pathlib import Path
from setuptools import setup, find_packages
import subprocess
import os
import shutil
import time
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig


def main():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # is there adequate permission to expand the path?
    except Exception as e:
        print(e)
    finally:
        sys.path.extend([
            os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
            os.path.abspath(os.path.dirname(__file__))
        ])
    logger = setup_logger(n_parent_dirs=2)  # Example: Check 2 parent directories
    logger.info("main.py's __main__ is running")
    return 0
def setup_logger(n_parent_dirs=1):
    """
    Sets up a logger and searches for an existing 'logs' directory within the specified
    number of parent directories.

    Args:
        n_parent_dirs (int): The number of parent directories to search for an existing 'logs' directory.
                             Default is 1 (check the immediate parent).
    """

    current_dir = Path(os.path.dirname(__file__))

    # Check for 'logs' in the current directory and up to n_parent_dirs
    for _ in range(n_parent_dirs + 1):
        logs_dir = current_dir / 'logs'
        if logs_dir.exists():
            break  # Found an existing 'logs' directory
        current_dir = current_dir.parent
    else:  # No 'logs' directory found in the search path
        logs_dir = current_dir / 'logs'
        logs_dir.mkdir(exist_ok=True)

    # Determine log file path 
    log_file_path = logs_dir / 'setup.log' 

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a file handler and set its level to DEBUG
    file_handler = RotatingFileHandler('setup.log', maxBytes=1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler and set its level to INFO
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    setattr(logger, 'parent', Path(os.path.dirname(__file__)))

    return logger

def execute_command(command):
    try:
        logging.info(f'Executing command: {command}')
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.debug(result.stdout.decode('utf-8'))
    except subprocess.CalledProcessError as exc:
        error_message = exc.stderr.decode('utf-8')
        logging.error(f'Command failed with error: {error_message}')
    except Exception as e:
        error_message = str(e)
        logging.error(f'Unhandled exception: {error_message}')

def run_setup(install_commands):
    for command in install_commands:
        execute_command(command)

    execute_command('python main.py')

if __name__ == "__main__":
    try:
        i = setup_logger()
        i.parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger('applog')
        logger.info("main.py is running")
    except ImportError:
        print("src not found, try reinstalling the package")
    finally:
        main()
