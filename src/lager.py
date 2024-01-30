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
# Note: The msg is the message format string, and the args are the arguments which are merged into msg using the string formatting operator. (Note that this means that you can use keywords in the format string, together with a single dictionary argument.) No % formatting operation is performed on msg when no args are supplied.
def init_logging():
    
    logging.config.dictConfig(LOGGING_CONFIG)  

    root_logger = logging.getLogger()   
    sub_logger = logging.getLogger('branch')

    return root_logger, sub_logger
# if propagate is True: Messages are passed directly to the ancestor loggers’ handlers - neither the level nor filters of the ancestor loggers in question are considered.
# The term ‘delegation to the parent’ means that if a logger has a level of NOTSET, its chain of ancestor loggers is traversed until either an ancestor with a level other than NOTSET is found, or the root is reached.
# The logger’s name will be resolved against the appropriate hierarchy of loggers, so that a logger named foo.bar will be affected by level settings on both foo and foo.bar, whereas a logger named foo will only be affected by settings on foo.
# If an ancestor is found with a level other than NOTSET, then that ancestor’s level is treated as the effective level of the logger where the ancestor search began, and is used to determine how a logging event is handled.
# If no ancestor is found for a logger, the root logger is used as the ancestor.
# If the root logger has a level of NOTSET, it will be treated as level WARNING.
# If the root is reached, and it has a level of NOTSET, then all messages will be processed. Otherwise, the root’s level will be used as the effective level.
# root, sub = init_logging()