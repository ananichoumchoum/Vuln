import subprocess
import re
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def run_pylint(scan_path):
    try:
        # Run Pylint on the scan path (file or directory)
        pylint_cmd = ['pylint', scan_path]
        process = subprocess.run(pylint_cmd, capture_output=True, text=True, check=False)
        print(f"Raw Pylint output: {process.stdout}")
        # Extract Pylint score from the output
        pylint_output = process.stdout
        score_match = re.search(r'Your code has been rated at ([\d\.]+)/10', pylint_output)
        score = score_match.group(1) if score_match else "N/A"

        # Check the return code and log based on the result
        if process.returncode == 0:
            print(f"Pylint scan completed with no issues. Score: {score}/10")
        elif process.returncode == 1:
            logger.warning(f"Pylint scan found linting issues. Score: {score}/10")
        elif process.returncode == 32:
            logger.error("Pylint usage error.")
        elif process.returncode == 2:
            logger.error("Pylint fatal error or parse error.")
        else:
            logger.error("Pylint scan failed with exit code %d", process.returncode)

        # Always return both stdout, stderr, and the score
        return {
            "pylint_output": pylint_output,
            "error": process.stderr if process.returncode != 0 else None,
            "score": score
        }
    except subprocess.CalledProcessError as e:
        # Log error if subprocess fails
        logger.error(f"Pylint execution failed: {e}")
        return {"error": "Pylint execution failed", "details": str(e)}
