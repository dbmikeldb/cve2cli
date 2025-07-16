# app/core/logging.py

import logging
import logging.handlers
import os

from logging.handlers import RotatingFileHandler


def create_log_handler(log_file, log_level=logging.DEBUG):
    """
    This is a helper function to create a RotatingFileHandler with standard formats.
    
    """

    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024, #1MB
        backupCount=5
    )

    log_handler.setLevel(log_level)
    log_handler.setFormatter(logging.Formatter('[%(asctime)s]---[%(levelname)s]---[%(message)s]'))
    
    return log_handler


def setup_logger(name, log_file, log_level=logging.DEBUG, to_console=True):
    """
    This function is used to create the logger per service, calling the helper function create_log_handler.

    Args:
        name(str): The name of the logger.
        log_file(str): The file path to the log file.
        log_level(str): The logging level.

    Returns:
        logger(***TBC***): The logger  

    """

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logging.handlers:
        logger.addHandler(create_log_handler(log_file, log_level))


    if to_console:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(logging.Formatter(('[%(asctime)s]---[%(levelname)s]---[%(message)s]')))
        logger.addHandler(stream_handler)
    
    return logger


app_logger = setup_logger('app', '../logging/app.log', logging.DEBUG)
auth_logger = setup_logger('auth', '../logging/auth.log', logging.DEBUG)
