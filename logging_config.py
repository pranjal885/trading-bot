import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Sets up the centralized logging system.
    Logs are written to logs/trading.log with rotation (5MB per file, max 3 files).
    """
    # Find project root directory to ensure logs folder is at the root
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logs_dir = os.path.join(project_root, 'logs')
    
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        
    log_file_path = os.path.join(logs_dir, 'trading.log')
    
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.INFO)
    
    # Add handler if logger does not already have handlers to prevent duplicate logs
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding='utf-8'
        )
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
