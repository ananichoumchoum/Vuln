"""
This module provides utility functions for validating file paths,
fetching tools based on categories, and handling user input for scanning.
Ensures valid directories/files are provided. Prompts user for correct inputs.
It also handles graceful program exit on Ctrl+C.
"""

import os
import re
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)
# Dictionary to store the category mappings and their tools
TOOL_CATEGORIES = {
    "Python Test": {
        "Security": ["bandit", "checkov", "safety", "trufflehog"],
        "Linting": ["flake8", "pylint", "mypy", "radon"]
    }
}


def ask_for_requirements_file(scan_path, default_file):
    """
    Prompt user to either use default requirements.txt or provide custom one.
    Re-prompts the user until a valid file is provided.

    Args:
        scan_path (str): The scan path where the requirements file is located.
        default_file (str): The default file path for requirements.txt.

    Returns:
        str: The valid path to the requirements file.
    """
    while True:
        custom_file = input(Fore.GREEN + f"Press Enter to use the default file"
                            f" ({os.path.join(scan_path, default_file)}), "
                            f"or type a custom file path: " + Style.RESET_ALL)

        # If the user presses Enter, use the default path
        if not custom_file.strip():
            requirements_file_path = os.path.join(scan_path, default_file)
        else:
            requirements_file_path = custom_file.strip()

        # Validate the provided requirements file
        try:
            # Validate the file using the is_valid_requirements_file() function
            is_valid_requirements_file(requirements_file_path)
            return requirements_file_path
        except ValueError as e:
            print(f"Error: {str(e)}. Please try again.")


def is_valid_directory(path):
    """Check if the provided path is a valid directory."""
    # Normalize the path early
    path = os.path.abspath(path)

    # Check if the path contains any potentially malicious characters
    if re.search(r'[\*\?\<\>\|]', path):
        raise ValueError("Invalid characters in path.")

    # Check if the directory exists
    if not os.path.exists(path):
        raise ValueError(f"Path {path} does not exist.")

    # Check if it's a directory
    if not os.path.isdir(path):
        raise ValueError(f"Path {path} is not a directory.")

    return path


def is_valid_requirements_file(path):
    """Check if the provided file exists and is a valid .txt file."""
    # Normalize the path early
    path = os.path.abspath(path)

    # Check if the path contains any potentially malicious characters
    if re.search(r'[\*\?\<\>\|]', path):
        raise ValueError("Invalid characters in path.")

    # Check if the file exists
    if not os.path.exists(path):
        raise ValueError(f"File {path} does not exist.")

    # Check if it's a file and has a .txt extension
    if not os.path.isfile(path) or not path.endswith('.txt'):
        raise ValueError(f"File {path} is not a valid .txt file.")

    return path


def get_tools_for_category(category):
    """
    Fetch the tools for a given category.

    Args:
        category (str): The category name (e.g., "Security", "Linting").

    Returns:
        list: A list of tools for the specified category.
    """
    return TOOL_CATEGORIES.get("Python Test", {}).get(category, [])
