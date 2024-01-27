#! /usr/bin/env python3
import logging, logging.config
import sys

def main():
    # Define the logging configuration
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

    # Apply the logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)

    # Create a sub-logger for your module
    # This sub-logger will be 'naked' and propagate to the root logger
    sublogger = logging.getLogger(__name__)

    # Now you can use the sublogger to log messages
    sublogger.info('This is an info message from the sublogger.')

if __name__ == "__main__":
    main()

    # Custom application log levels 001-199
    for i in range(1, 200):
        logging.addLevelName(i, f"LEVEL{str(i).zfill(3)}")


    # Extend the Logger class to support custom application-specific logging methods
    class AppLogger(logging.Logger):
        def __init__(self, name, level=logging.NOTSET):
            super().__init__(name, level)
            # Dynamically add custom level methods to the logger
            for i in range(1, 200):
                def _log_at_level(self, message, *args, level=i, **kwargs):
                    if self.isEnabledFor(level):
                        self.log(level, message, *args, **kwargs)
                setattr(self, f"custom_{i}", _log_at_level)

    # Set our custom logger as the default for our application
    logging.setLoggerClass(AppLogger)

    # Configure the logging system
    # You can add file handlers, formatters or other configurations as needed
    logging.basicConfig(level=1)  # Set the lowest custom level for the root logger

    # Example usage of the custom AppLogger
    logger = logging.getLogger('my_app_logger')

    # Log a message using one of the custom logging methods
    logger.custom_1('This message is logged with a custom level of 1.')
    logger.custom_42('This message corresponds to a domain-specific event with level 42.')