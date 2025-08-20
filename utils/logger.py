import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(log_path: str = 'InfoSnare.log'):
    os.makedirs(os.path.dirname(log_path) or '.', exist_ok=True)
    handler = RotatingFileHandler(log_path, maxBytes=1024*1024, backupCount=3)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s',
        handlers=[handler, logging.StreamHandler()]
    ) 