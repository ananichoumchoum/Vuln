"""
This module contains functions to run Checkov on a given file or directory
and return the scan output along with any errors encountered
"""
import subprocess
import logging
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)

# Initialize logger
logger = logging.getLogger(__name__)


def run_checkov(scan_path):
    """
    Runs Checkov on the specified scan_path and returns the output.

    Args:
        scan_path (str): The directory path to scan with Checkov.

    Returns:
        dict: A dictionary containing the output of the scan or error message.
    """
    print(Fore.YELLOW + "Tool: Checkov" + Style.RESET_ALL)

    try:
        # Command to run Checkov
        venv_dir = os.path.dirname(sys.executable)
        checkov_bat = os.path.join(venv_dir, 'checkov.cmd')
        checkov_cmd = [checkov_bat, '--directory', scan_path]
        process = subprocess.run(
            checkov_cmd, capture_output=True, text=True, check=False)

        # Check if Checkov returned any issues
        if process.returncode == 0:
            logger.info("Checkov scan completed with no issues\n")
        else:
            logger.warning("Checkov found potential security misconfig\n")

        return {
            "output": process.stdout or "No output",
            "error": process.stderr or "No error"
        }

    except subprocess.CalledProcessError as e:
        error_msg = f"Checkov execution failed: {e}\n"
        logger.error(error_msg)
        return {"error": error_msg}
