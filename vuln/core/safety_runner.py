"""
This module runs the Safety tool to check known vulnerabilities in dependencies
"""

import subprocess
import json
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_safety(requirements_file):
    """
    Runs the Safety security tool to check for vulnerabilities in dependencies

    Parameters:
    - requirements_file (str): The path to the requirements.txt file

    Returns:
    - dict: JSON-parsed result of the Safety scan or error details
    """
    print("Tool: Safety")

    # Validate the requirements file path
    if not os.path.exists(requirements_file):
        print("[Error] Requirements file not found.")
        print("The requirements file is missing from the path you specified.")
        print(
            "If your file has a different name or is located elsewhere,"
            " please use:"
        )
        print("--requirements-file <file_path/name_file> --tools safety\n")
        return {"error": "Requirements file not found"}
    try:
        # Run Safety and capture output
        safety_cmd = ['safety', 'check', '--file', requirements_file, '--json']
        process = subprocess.run(
            safety_cmd, capture_output=True, text=True, check=False)

        # Check if process failed and log an error
        if process.returncode == 0:
            print("Safety scan completed with no issues.")
        elif process.returncode == 64:
            logger.warning("Safety scan found issues.")
        else:
            logger.error(
                "Safety scan failed with exit code %d", process.returncode)

        # Parse the JSON output, if valid
        if process.stdout.strip():
            try:
                safety_results = json.loads(process.stdout)
                return safety_results
            except json.JSONDecodeError as e:
                logger.error("Failed to parse Safety output as JSON: %s \n", e)
                return {"error": "Invalid JSON output from Safety",
                        "details": process.stdout}
        else:
            logger.error("Safety scan produced no output.")
            return {"error": "No output from Safety",
                    "details": "Empty stdout \n"}

    except subprocess.CalledProcessError as e:
        logger.error("Safety scan failed with error: %s \n", e.stderr)
        return {"error": "Safety scan failed", "details": e.stderr}

    except OSError as e:
        logger.error("An unexpected OS error occurred: %s \n", e)
        return {"error": "Unexpected OS error", "details": str(e)}
