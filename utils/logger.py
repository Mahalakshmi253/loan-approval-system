"""Logging utilities for the application."""
import logging
import sys
from typing import Optional
from config.settings import settings


def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Setup logger with consistent formatting."""
    log_level = level or settings.LOG_LEVEL
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        if settings.LOG_FILE:
            file_handler = logging.FileHandler(settings.LOG_FILE)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
