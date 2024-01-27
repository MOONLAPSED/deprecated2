#! /usr/bin/env python3
import logging

# only root/base logger has properties, all submodules strip their submodule logger of values - they retain only their own level and propagate value to root logger if necessary (if they are not disabled) by default.

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s')
sublogger = logging.getLogger(__name__)


def main():
    sublogger.info("Hello, world!")