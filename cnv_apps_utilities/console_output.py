from typing import Any

def print_in_color(message: Any, color: str = "white") -> None:
    """
    Prints the given message in the specified color.
    Args:
        message (str): The message to be printed.
        color (str, optional): The color in which the message should be printed. Defaults to "white".
            Available colors: "white", "green", "red", "blue", "yellow", "magenta", "cyan".
    Raises:
        ValueError: If an invalid color is provided.
    Returns:
        None
    """    
    available_colors: dict[str, str] = {
        "white": "\033[97m",
        "green": "\033[92m",
        "red":"\033[91m",
        "blue": "\033[94m",
        "yellow": "\033[93m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
    }
    end_of_colored_part: str = "\033[00m"
    if color not in list(available_colors.keys()):
        raise ValueError(f"Invalid color: {color}. Available colors: {available_colors}")
    
    print(f"{available_colors[color]}{message}{end_of_colored_part}")
    
    return None