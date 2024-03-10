import sys
import logging
from pathlib import Path
from logging.config import dictConfig
import time

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

class ProgressBarLogger:
    def __init__(self, total=100):
        self.total = total
        self.count = 0
        
    def update(self, increment=1):
      
        self.count += increment
        percent_complete = self.count / self.total * 100
        
        # Log progress bar at info level
        logger.info(f"[{'='*int(percent_complete/10)}:<10] {percent_complete:.0f}%")
        # Pause for each 25% section
        if percent_complete <= 25:
            time.sleep(0.1)
        elif percent_complete <= 50: 
            time.sleep(0.2)
        elif percent_complete <= 75:
            time.sleep(0.3)
        else:
            time.sleep(0.4)

        sys.stdout.write('\r')
        sys.stdout.flush()

        if percent_complete == 100:
            sys.stdout.write('\n')
            sys.stdout.flush()
            time.sleep(0.1)
            return True
        return False
        
    def reset(self):
            self.count = 0

    def set_total(self, total):
        self.total = total
        self.count = 0

    def get_count(self):
        return self.count
    
    def get_total(self):
        return self.total
        
    def get_percent_complete(self):
            return self.count / self.total * 100
    
    def get_progress_bar(self):
        percent_complete = self.count / self.total * 100
        return f"[{'='*int(percent_complete/10)}:<10] {percent_complete:.0f}%"
    

if __name__ == '__main__':
    logger = main()
    main().info('Loading... 1/2...')
    bar = ProgressBarLogger()
    for i in range(100):
        bar.update()
    
    bar.reset()
    main().info('Loading... 2/2...')
    bar.set_total(100)
    for i in range(100):
        bar.update()
    bar.reset()
