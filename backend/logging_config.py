import logging
import logging.handlers
from pathlib import Path
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging(name: str) -> logging.Logger:
    """
    Setup logging configuration for the application.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / "app.log",
        maxBytes=10485760,
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatter
    formatter = logging.Formatter(
        '[%(asctime)s] %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
