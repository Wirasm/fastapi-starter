"""Module for setting up and configuring logging for the application.

This module provides functionality to set up logging with both console
and file handlers, allowing for comprehensive logging throughout the application.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    """Set up and configure logging for the application.

    This function creates a root logger with both console and file handlers.
    The file handler uses a RotatingFileHandler to manage log file sizes.

    Returns:
        logging.Logger: The configured root logger.
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Set up root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)

    # File handler
    file_handler = RotatingFileHandler(
        filename=log_dir / "app.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)

    # Add handlers to root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Create a logger instance
logger = setup_logging()
