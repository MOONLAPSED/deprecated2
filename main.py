# main.py

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from src.lager import init_logging

root_logger, sub_logger = init_logging()

root_logger.info("Log message from main.py")
sub_logger.info("Another log message from main.py")
