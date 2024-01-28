#! /usr/bin/env python3
# main.py
import src.lager

root_logger, branch_logger = src.lager.init_logging()

from src.ufx import SerializationInterface

def main():
    class UnixFilesystem(SerializationInterface):
        pass

if __name__ == '__main__':
    main()