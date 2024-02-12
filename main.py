#! /usr/bin/env python3
# main.py
import os
import sys
from logging import config as logging
from src.lager import *


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

        return 0

if __name__ == "__main__":
    try:
        logging.config.dictConfig(LOGGING_CONFIG)
        logger = logging.getLogger('applog')
        logger.info("main.py is running")
    except ImportError:
        print("src not found, try reinstalling the package")
    finally:
        main()
