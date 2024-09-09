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
    # Validate scan path
    if not os.path.exists(scan_path):
        raise FileNotFoundError(f"Scan path '{scan_path}' does not exist.")
    
    try:
        # Run Bandit and capture output
        bandit_cmd = ['bandit', '-r', scan_path, '-f', 'json']
        
        process = subprocess.run(bandit_cmd, capture_output=True, text=True)
        bandit_results = json.loads(process.stdout)
        
        # Return Bandit results (parsed JSON)
        return bandit_results

    except subprocess.CalledProcessError as e:
        logger.error(f"Bandit scan failed with error: {e.stderr}")
        return {"error": "Bandit scan failed", "details": e.stderr}

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {"error": "Unexpected error", "details": str(e)}
