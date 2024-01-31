#! /usr/bin/env python3
# main.py

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'))

import src.lager

def main():
    logger, _ = src.lager.init_logging()
    try:
        logger.info("Application initialized.")
    except NameError:
        print("Logger not defined")
    finally:
        # print(f"finishing main with logger {logger}")
        pass
    return logger, _

def sub():
    _, sub_logger = src.lager.init_logging()
    try:
        sub_logger.info("Application in-progress.")
    except NameError:
        print("Logger not defined")
    finally:
        # print(f"finishing sub with logger {sub_logger}")
        pass
    return _, sub_logger

if __name__ == "__main__":
    main()
    sub()
    leaf = src.lager.logger_factory('leaf')
    leaf.info("Application conclueded.")