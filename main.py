#! /usr/bin/env python3
# main.py
import os
import src.lager

root_logger, branch_logger = src.lager.init_logging()
def main():
    root_logger.info("")
    branch_logger.info("")


main()
