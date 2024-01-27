#! /usr/bin/env python3
import logging
import logging.config
import sys

def main():
    """
    Main function that configures logging and demonstrates custom application-specific logging methods.

    This function sets up the logging configuration, creates a logger, and extends the logger class
    to support custom application-specific logging methods. It then demonstrates the usage of these
    custom methods by logging an error and a critical message.

    """
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'datefmt': '%z- %Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'level': logging.INFO,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': sys.stdout
            },
        },
        'file': {
            'level': logging.getLevelName('default'),
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'app.log',
            'maxBytes': 10485760,
            'backupCount': 10
        },
        'root': {
            'handlers': ['console'],
            'level': logging.INFO,
            'propagate': True
        },
        'ERROR': {
            'handlers': ['console', 'file'],
            'level': logging.ERROR,
            'propagate': False
        },
        'CRITICAL': {
            'handlers': ['console', 'file'],
            'level': logging.CRITICAL,
            'propagate': False
        },
        'LEVEL001': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
            'propagate': False
        },
        'LEVEL200': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
            'propagate': False
        },
        'LEVELXYZ': {
            'handlers': ['console', 'file'],
            'level': logging.DEBUG,
            'propagate': False
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)  # Mutate the basicConfig
    
    # Create a logger
    logger = logging.getLogger(__name__)

    # Extend the Logger class to support custom application-specific logging methods
    class AppLogger(logger.__class__):
        # Custom application log levels 001-199
        for i in range(1, 200):
            logging.addLevelName(i, f"LEVEL{str(i).zfill(3)}")
        
        def __init__(self, name, level=logging.NOTSET):
            super().__init__(name, level)
            # Dynamically add custom level methods to the logger
            for i in range(1, 200):
                def _log_at_level(self, message, *args, level=i, **kwargs):
                    if self.isEnabledFor(level):
                        self.log(level, message, *args, **kwargs)
                setattr(self, f"custom_{i}", _log_at_level)

        def custom_error(self, message, *args, **kwargs):
            self.error(message, *args, **kwargs)

        def custom_critical(self, message, *args, **kwargs):
            self.critical(message, *args, **kwargs)

    # Replace the logger with the new class
    logger.__class__ = AppLogger

    # Create a logger
    logger = logging.getLogger(__name__)

    logger.custom_error("This is an error message")
    logger.custom_critical("This is a critical message")

    # logging.handlers.TimedRotatingFileHandler.level = 100

    def print_logging_levels():
        for level in range(0, 200):
            for e in ['CRITICAL', 'ERROR']:
                if e in logging.getLevelName(level):
                    print(f"Level {level} is {logging.getLevelName(level)}")

    print_logging_levels()

if __name__ == "__main__":
    main()

