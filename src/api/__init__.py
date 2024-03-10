import sys
import logging
import os
import toml
# Path: src/api/__init__.py
"""Initializes logging for the module.

Creates a logger named after the module, sets the log level, adds handlers for 
console and file output, and propagates logs to the parent logger if defined.

Logging will be initialized only once, subsequent calls will just retrieve the
existing initialized logger.
"""
from pathlib import Path
import logging

ml = None
ml = logging.getLogger(__name__)
log_level = os.getenv('API_LOG_LEVEL', 'INFO')  # Get from environment or default to INFO
ml.setLevel(log_level)
if ml is None:
    ml = logging.getLogger(__name__)
    ml.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s]%(asctime)s||%(name)s: %(message)s', datefmt='%Y-%m-%d~%H:%M:%S%z')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    ml.addHandler(console_handler)
    logs_dir = Path(__file__).resolve().parent / 'logs'
    logs_dir.mkdir(exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(logs_dir / 'app.log', maxBytes=10485760, backupCount=10)
    file_handler.setFormatter(formatter)
    ml.addHandler(file_handler)
    ml.propagate = False
    ml.setLevel(logging.INFO)
    ml.info('Logging initialized src: %s', __file__)
else:
    ml.setLevel(logging.INFO)
    ml.info('Logging already initialized')

if ml.__dict__.get('parent') is None or ml.__dict__.get('parent') != 'cognos':
    ml.__dict__['parent'] = Path(__file__).resolve().parent

'ml' in globals() or globals().__setitem__('ml', ml)
