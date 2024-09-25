"""
This module contains functions to run MyPy on a given file or directory
and return the type checking output along with any errors encountered.
"""
import subprocess
import logging
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

# Initialize logger
logger = logging.getLogger(__name__)


def run_mypy(scan_path):
    """
    Runs MyPy on the specified scan_path and returns the output.

    Args:
        scan_path (str): The file or directory path to scan with MyPy.

    Returns:
        dict: A dictionary containing the output of the scan or error message.
    """
    print(Fore.YELLOW + "Tool: Mypy" + Style.RESET_ALL)

    try:
        # Command to run MyPy
        mypy_cmd = ['mypy', scan_path]
        process = subprocess.run(
            mypy_cmd, capture_output=True, text=True, check=False)

        # Check if MyPy returned any issues
        if process.returncode == 0:
            logger.info("MyPy scan completed with no issues\n")
        else:
            logger.warning("MyPy found type-checking issues\n")

        return {
            "output": process.stdout or "No output",
            "error": None if process.returncode == 0 else process.stderr
        }

    except subprocess.CalledProcessError as e:
        error_msg = f"MyPy execution failed: {e}\n"
        logger.error(error_msg)
        return {"error": error_msg}
