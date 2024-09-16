"""
This module contains functions to run Pylint on a given file or directory
and return the linting output along with any errors encountered.
"""
import subprocess
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def run_pylint(scan_path):
    """
    Runs the Pylint command on the specified scan_path and returns the output
    and error messages (if any).

    Args:
        scan_path (str): The file or directory path to scan with Pylint.

    Returns:
        dict: A dictionary containing the Pylint output and any errors.
    """
    try:
        # Command to run Pylint
        pylint_cmd = ['pylint', scan_path]

        # Run Pylint and capture the output and errors
        process = subprocess.run(pylint_cmd, capture_output=True, text=True, check=False)
        pylint_output = process.stdout

        # Determine the exit code and log the appropriate message
        if process.returncode == 0:
            print("Pylint scan completed with no issues.")
        elif process.returncode in {1, 20}:
            logger.warning("Pylint scan found linting issues.")
        elif process.returncode == 32:
            logger.error("Pylint usage error.")
        elif process.returncode == 2:
            logger.error("Pylint fatal error or parse error.")
        else:
            logger.error("Pylint scan failed with exit code %d", process.returncode)

        # Return the output and any error messages
        return {
            "pylint_output": pylint_output,
            "error": process.stderr if process.returncode != 0 else None,
        }

    except subprocess.CalledProcessError as e:
        # Log any subprocess errors
        logger.error("Pylint execution failed: %s", e)
        return {"error": "Pylint execution failed", "details": str(e)}
