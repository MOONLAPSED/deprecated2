import logging
from logging.config import dictConfig
import sys
import os
from logging.handlers import RotatingFileHandler 
from dataclasses import dataclass
from abc import ABC, abstractmethod
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,   
    'formatters': {
        'default': {
            'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
            'datefmt': '%Y-%m-%d~%H:%M:%S%z'
        },
    },
    'handlers': {
        'console': {
            'level': logging.INFO,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': logging.INFO,
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10485760,
            'backupCount': 10
        }
    },
    'root': {  
        'level': logging.INFO,
        'propagate': True,
        'handlers': ['console', 'file']
    }
}
def init_logging():
    
    logging.config.dictConfig(LOGGING_CONFIG)  

    root_logger = logging.getLogger()   
    sub_logger = logging.getLogger('branch')

    return root_logger, sub_logger

def logger_factory(logger_name: str = '{__name__}'):
    return logging.getLogger(logger_name)

def main():
    logger, _ = init_logging()
    try:
        logger.info("Application initialized.")
    except NameError:
        print("Logger not defined")
    finally:
        # print(f"finishing main with logger {logger}")
        pass
    return logger, _

def sub():
    _, sub_logger = init_logging()
    try:
        sub_logger.info("Application in-progress.")
    except NameError:
        print("Logger not defined")
    finally:
        # print(f"finishing sub with logger {sub_logger}")
        pass
    return _, sub_logger

