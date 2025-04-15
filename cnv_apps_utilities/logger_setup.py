import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(log_directory: Path, log_file_name: str):
    """
    Configure and return a logger with file rotation and console output.

    This function sets up a logger that writes logs to a file with rotation 
    capabilities and also prints errors to the console. It's useful for scenarios 
    where you want to keep detailed logs in files for debugging or auditing purposes 
    while also having immediate visibility of errors during runtime.

    Args:
        log_directory (Path): The directory where log files will be stored.
        log_file_name (str): The name of the log file to be created.

    Returns:
        logging.Logger: A configured logger instance.

    The logger configuration includes:
    - **File Handler**: 
        - Uses `RotatingFileHandler` for log file management.
        - Logs at INFO level or above.
        - Log files rotate when they reach 1 MB (1,000,000 bytes), with up to 3 backups.
    - **Console Handler**: 
        - Only logs ERROR messages and above to the console.
    - **Formatter**: 
        - Uses a consistent format for timestamps, logger name, log level, and message.

    Note:
        - The `Path` type hint ensures that `log_directory` is a path-like object for 
          safe file operations.
        - If the `log_directory` does not exist, this function will raise an exception 
          when attempting to write logs.
    """
    logger = logging.getLogger(name=__name__)
    logger.setLevel(level=logging.INFO)

    file_handler = RotatingFileHandler(filename=log_directory/log_file_name, 
                                       maxBytes=1000000, 
                                       backupCount=3)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(fmt=formatter)
    console_handler.setFormatter(fmt=formatter)

    logger.addHandler(hdlr=file_handler)
    logger.addHandler(hdlr=console_handler)

    return logger

def log_error(logger: logging.Logger, message: str) -> None:
    """
    Log an error message using Python's built-in logging system.

    This function acts as a wrapper around the `logging.error` method to provide 
    a consistent way to log errors throughout the application. It ensures that 
    all error messages are formatted and handled in the same manner, enhancing 
    maintainability and debugging.

    Args:
        message (str): The error message to be logged.

    Returns:
        None

    Note:
        - This method does not handle exceptions; it merely logs them.
        - The actual logging behavior depends on the configuration of the logging module.
    """
    logger.error(msg=message)

def log_warning(logger: logging.Logger, message: str) -> None:
    """
    Log an warning message using Python's built-in logging system.

    This function acts as a wrapper around the `logging.warning` method to provide 
    a consistent way to log warning throughout the application. It ensures that 
    all warning messages are formatted and handled in the same manner, enhancing 
    maintainability and debugging.

    Args:
        message (str): The warning message to be logged.

    Returns:
        None

    Note:
        - This method does not handle exceptions; it merely logs them.
        - The actual logging behavior depends on the configuration of the logging module.
    """
    logger.warning(msg=message)