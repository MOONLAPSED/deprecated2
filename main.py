#! /usr/bin/env python3
# main.py

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'))

import src.lager


if __name__ == "__main__":
    src.lager.main()
    src.lager.sub()
    leaf = src.lager.logger_factory('leaf')
    leaf.info(f"leaf set to {leaf.level}")
