#! /usr/bin/env python3
# main.py
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'))

import src.lager

root_logger, branch_logger = src.lager.init_logging()

def init_logging():
        print("The root logger is set to {}.".format(root_logger.level))
        print("The branch logger is set to {}.".format(branch_logger.level))
        return root_logger, branch_logger

def loglevel(level):
    root_logger.setLevel(level)
    branch_logger.setLevel(level)
    print("The root logger is set to {}.".format(root_logger.level))
    print("The branch logger is set to {}.".format(branch_logger.level))

def main():
    init_logging()
    branch_logger.warning("This is a warning message.")
    branch_logger.error("This is an error message.")
    branch_logger.critical("This is a critical message.")
    branch_logger.info("This is an info message.")
    branch_logger.debug("This is a debug message.")
    loglevel(30)
    branch_logger.warning("This is a warning message.")
    branch_logger.error("This is an error message.")
    branch_logger.critical("This is a critical message.")
    branch_logger.info("This is an info message.")
    branch_logger.debug("This is a debug message.")

if __name__ == '__main__':
    main()
