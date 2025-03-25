# mmorpdnd_tools.py
# This file contains common methods and utility functions for the MMORPDND project.
# Purpose: To centralize reusable code for tasks like text output, file processing, 
# and other tools, improving modularity and maintainability across the project.

def output_text(text, option="text"):
    """
    Print text to the console in a specified color using ANSI escape codes.

    Args:
        text (str): The text to be printed.
        option (str, optional): The color option for the text. Valid options are "text" (default, no color), 
            "warning" (yellow), "error" (red), "note" (blue), "success" (green), "command" (cyan), 
            and "test" (magenta). Defaults to "text". Invalid options result in uncolored text.

    Returns:
        None

    Note:
        This function uses ANSI escape codes for color formatting. Colors may not display correctly 
        in all environments (e.g., some IDEs or Windows terminals without ANSI support).
    """
    color_codes = {
        "text": "\033[0m",      # Reset color
        "warning": "\033[93m",  # Yellow - Warning text
        "error": "\033[91m",    # Red - Error text
        "note": "\033[94m",     # Blue - Notes or program information
        "success": "\033[92m",  # Green - Success text
        "command": "\033[36m",  # Cyan - Command output text
        "test": "\033[35m"      # Magenta - Testing
    }

    text = str(text)  # Ensure text is a string
    if option in color_codes:
        color_code = color_codes[option]
        reset_code = color_codes["text"]
        print(f"{color_code}{text}{reset_code}")
    else:
        print(text)
        
        
def is_image_file(file_name):
    """
    Checks if a file name is an image file based on its extension.

    Args:
        file_name (str): The name of the file to check.

    Returns:
        bool: True if the file name has an image extension, False otherwise.

    Example:
        >>> is_image_file('myphoto.jpg')
        True
        >>> is_image_file('document.pdf')
        False
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    for ext in image_extensions:
        if file_name.lower().endswith(ext):
            return True
    return False
