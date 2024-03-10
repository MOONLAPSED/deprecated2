import sys
import logging
from pathlib import Path
from logging import StreamHandler
from logging.config import dictConfig

def main(n_parent_dirs: int = 0):
    logs_dir = Path(__file__).resolve().parent / 'logs'
    
    sys.path.append((Path(__file__).resolve().parent / '..').resolve())
    sys.path.append((Path(__file__).resolve().parent / 'src').resolve())
    current_dir = Path(__file__).resolve().parent

    for _ in range(n_parent_dirs + 1):
        logs_dir = current_dir / 'logs'
        if logs_dir.exists():
            break  
        current_dir = current_dir.parent

    logs_dir.mkdir(exist_ok=True)
    
    logging_config = {
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
                'level': None,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': None,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': logs_dir / 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 10
            }
        },
        'root': {
            'level': logging.INFO,
            'handlers': ['console', 'file']
        }
    }

    dictConfig(logging_config)

    logger = logging.getLogger(__name__)

    return logger
        
if __name__ == '__main__':
    logger = main()
    main().info('Hello World!')