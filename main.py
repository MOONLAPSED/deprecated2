#! /usr/bin/env python3
# main.py
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'))

import src.lager

def main():
    logger, sub_logger = src.lager.init_logging()
    return logger, sub_logger

def sub():
    logger, sub_logger = main()
    try:
        sub_logger.warning("This is a warning message")
    except NameError:
        print("Logger not defined")
    finally:
        print("Exiting sub")

if __name__ == '__main__':
    logger, sub_logger = main()
    try:
        logger.warning("This is a warning message")
    except NameError:
        print("Logger not defined")
    finally:
        print("Exiting main")
    sub()