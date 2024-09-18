"""
This module runs the Bandit security scanner on a given path and parses results
Captures the output in JSON format and handles potential errors during the scan
"""
import subprocess
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_bandit(scan_path):
    """
    Runs Bandit security scanner on the provided path.

    Parameters:
    - scan_path (str): The directory or file to scan.

    Returns:
    - dict: JSON-parsed result of the Bandit scan.
    """
    print("Tool: Bandit")

    # Validate scan path
    if not os.path.exists(scan_path):
        raise FileNotFoundError(f"Scan path '{scan_path}' does not exist.")

    try:
        # Run Bandit and capture output
        bandit_cmd = ['bandit', '-r', scan_path, '-f', 'json']
        process = subprocess.run(
            bandit_cmd, capture_output=True, text=True, check=False)

        if process.returncode == 0:
            print("Bandit scan completed with no issues.")
        elif process.returncode == 1:
            logger.warning("Bandit scan found issues.")
        else:
            logger.error(
                "Bandit scan failed with exit code %d", process.returncode)

        # Parse and return Bandit results (JSON)
        bandit_results = json.loads(process.stdout)
        return bandit_results

    except subprocess.CalledProcessError as e:
        logger.error("Bandit scan failed with Process error: %s", e.stderr)
        return {"error": "Bandit scan failed", "details": e.stderr}

    except OSError as e:
        logger.error("An unexpected OS error occurred: %s", str(e))
        return {"error": "Unexpected OS error", "details": str(e)}
