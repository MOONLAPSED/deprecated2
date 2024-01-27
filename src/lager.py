import logging
from logging.config import dictConfig
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,   
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%z-%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': logging.INFO,
            'class': 'logging.StreamHandler',
            'formatter': 'default' 
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
    import sys
    import os
    from logging.handlers import RotatingFileHandler 
    from dataclasses import dataclass
    from abc import ABC, abstractmethod
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

    
    logging.config.dictConfig(LOGGING_CONFIG)  

    root_logger = logging.getLogger()   
    sub_logger = logging.getLogger('sub')

    root_logger.info("Root logger")  
    sub_logger.info("Sub logger")


    @dataclass(frozen=True)
    class LogBase(ABC):
        name: str = None
        propagate: bool = True
        
        logger: logging.Logger = None

        def should_propagate(self, level):
            return self.propagate and level >= self.level
    return root_logger, sub_logger

# root, sub = init_logging()