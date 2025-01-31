import os
import sys
from pathlib import Path
from typing import Optional
from .get_variables_from_path import log_error

def get_path_from_env(value: str) -> Path:
    """
    Retrieve a file system path from an environment variable.

    This function looks up an environment variable by name, checks if it's set,
    verifies if the path exists, and returns it as a `Path` object. If the 
    environment variable is not set or the path does not exist, it raises 
    a `ValueError` with an informative message. Errors are both printed to 
    stdout and logged.

    Args:
        value (str): The name of the environment variable to look up.

    Returns:
        Path: A `Path` object representing the file system path from the 
              environment variable.

    Raises:
        ValueError: 
            - If the environment variable is not set.
            - If the path specified by the environment variable does not exist.

    Note:
        - This function assumes the existence of a `log_error` function to 
          log error messages. Ensure this function is defined or imported.
        - It checks for path existence at the time of function call; the path 
          must exist before this function can return successfully.
    """

    env_value = os.getenv(value)

    if env_value is None: 
        error_message = f"Error: {value} environment variable not set!"
        print(error_message, file=sys.stdout)
        log_error(error_message)
        raise ValueError(error_message)
    
    path = Path(env_value)
    if not os.path.exists(env_value):
        error_message = f"Path set in .env file {env_value} does not exist."
        print(error_message, file=sys.stdout)
        log_error(message=error_message)
        raise ValueError(error_message)
    
    return path

def get_integer_from_env(value: str, default_value: int = 300) -> int:
    """
    Retrieve an integer from an environment variable, with a fallback to a default value.

    This function attempts to fetch and convert an environment variable's value 
    to an integer. If the conversion fails due to the variable not being set or 
    containing non-integer data, it logs an error and returns the provided default 
    value.

    Args:
        value (str): The name of the environment variable to look up.
        default_value (int, optional): The value to return if the environment 
                                       variable's value cannot be converted 
                                       to an integer. Defaults to 300.

    Returns:
        int: The integer value from the environment variable if conversion is 
             successful, otherwise the default_value.

    Note:
        - If the environment variable does not exist (i.e., `env_value` is `None`), 
          or if it cannot be converted to an integer, an error is logged but 
          no exception is raised; the default value is returned instead.
        - Errors are logged using a `log_error` function which should be defined 
          or imported elsewhere in your code.
    """
    env_value: Optional[str] = os.getenv(value)
   
    try:
        return int(env_value)
    except ValueError:
        error_message = f"Error: {value} environment variable '{env_value}' is not a valid integer. Defaulting to {default_value}."
        log_error(message=error_message)
        return default_value
    
def get_string_from_env(value: str) -> str:
    """
    Retrieve a string value from an environment variable.

    This function fetches the value of a specified environment variable and 
    returns it as a string. If the environment variable is not set, it raises 
    a `ValueError` with an informative message, logs the error, and prints it 
    to stdout.

    Args:
        value (str): The name of the environment variable to look up.

    Returns:
        str: The string value from the environment variable.

    Raises:
        ValueError: If the environment variable is not set.

    Note:
        - This function assumes the existence of a `log_error` function for 
          logging error messages. Ensure this function is defined or imported.
        - The error message is both printed to stdout and logged for better 
          visibility and debugging.
    """

    env_value = os.getenv(value)

    if env_value is None: 
        error_message = f"Error: {value} environment variable not set!"
        log_error(message=error_message)
        print(error_message, file=sys.stdout)
        raise ValueError(error_message)
    
    return env_value