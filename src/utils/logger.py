"""
Logger Configuration Module
Sets up application-wide logging.
"""

import sys
from pathlib import Path
from typing import Optional
from loguru import logger
from datetime import datetime


def setup_logger(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    rotation: str = "10 MB",
    retention: str = "7 days"
) -> None:
    """
    Configure application-wide logger.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for log output
        rotation: Log rotation size
        retention: Log retention period
    """
    # Remove default handler
    logger.remove()
    
    # Console handler with colored output
    logger.add(
        sys.stderr,
        level=log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True
    )
    
    # File handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.add(
            log_file,
            level=log_level,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{name}:{function}:{line} | "
                "{message}"
            ),
            rotation=rotation,
            retention=retention,
            compression="zip"
        )
    
    logger.info(f"Logger initialized with level: {log_level}")


def get_logger(name: str = "career_architect"):
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name for context
        
    Returns:
        Logger instance
    """
    return logger.bind(name=name)


class LogContext:
    """Context manager for structured logging."""
    
    def __init__(self, operation: str, **kwargs):
        self.operation = operation
        self.context = kwargs
        self.start_time = None
        self.logger = get_logger()
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(
            f"Starting {self.operation}",
            **self.context
        )
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is not None:
            self.logger.error(
                f"Failed {self.operation} after {duration:.2f}s: {exc_val}",
                **self.context
            )
            return False
        
        self.logger.info(
            f"Completed {self.operation} in {duration:.2f}s",
            **self.context
        )
        return True


def log_function_call(func):
    """Decorator to log function calls."""
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.debug(f"Calling {func_name}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Completed {func_name}")
            return result
        except Exception as e:
            logger.error(f"Error in {func_name}: {e}")
            raise
    
    return wrapper
