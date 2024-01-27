#! /usr/bin/env python3
import logging, logging.config
import sys

def main():  # Define the logging configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
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
        'root': {
            'handlers': ['console'],
            'level': logging.INFO,
            'propagate': True
        }
    }

    # Mutate the basicConfig
    logging.config.dictConfig(LOGGING_CONFIG)
    
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

if __name__ == "__main__":
    main()
