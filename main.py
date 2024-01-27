# main.py

import os
import sys

from src.lager import init_logging

print("The current working directory is: " + os.getcwd())

root_logger, sub_logger = init_logging()

root_logger.info("Log message from main.py")
sub_logger.info("Another log message from main.py")

from dev.testfiledir import main2
main2()
