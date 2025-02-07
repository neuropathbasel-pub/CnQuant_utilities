import os
import orjson
from pathlib import Path
from .logger_setup import log_error

def load_analysis_status(status_json_path: str | Path, dictionary_status_entry_name: str) -> bool:
    """
    Load and check the status from a JSON file.

    This function attempts to read a JSON file from the given path, looking for a specific 
    status entry by name. If the entry exists and is truthy, it returns `True`. Otherwise, 
    it returns `False` or upon encountering any errors during file operations or JSON parsing.

    Parameters:
    - status_json_path (str | Path): The path to the JSON file, which can be provided as a string or Path object.
    - dictionary_status_entry_name (str): The key name within the JSON to check for the status.

    Returns:
    - bool: 
      - `True` if the status entry exists and is truthy.
      - `False` if:
        - The file does not exist.
        - The JSON could not be decoded.
        - An IO error occurred while reading the file.
        - The specified status entry is missing or falsy.
        - Any other unexpected error occurred.

    Raises:
    - No exceptions are raised; errors are logged instead using `log_error`.

    Notes:
    - The function uses `orjson` for JSON parsing for better performance.
    - Errors are logged but not raised, ensuring the function always returns a boolean.
    """
    path = Path(status_json_path) if isinstance(status_json_path, str) else status_json_path

    if not os.path.exists(path=path):
        return False
    try:
        with open(file=path, mode='rb') as file:
            return orjson.loads(file.read()).get(dictionary_status_entry_name, False)
    except orjson.JSONDecodeError:
        log_error(message=f"Error decoding JSON from file: {path}")
    except IOError as e:
        log_error(message=f"IOError occurred when reading file {path}: {e}")
    except Exception as e:
        log_error(message=f"Unexpected error when processing {path}: {e}")
    return False