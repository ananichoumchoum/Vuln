"""
This module contains functions to run Pylint with Dlint on a given file or directory
and return the scan output along with any errors encountered.
"""
import subprocess
import logging
import os

# Initialize logger
logger = logging.getLogger(__name__)

def trim_path(file_path):
    """
    Trims the path to keep only the last folder and file name.
    """
    # Get the last directory and the file name
    folder = os.path.basename(os.path.dirname(file_path))
    file = os.path.basename(file_path)
    # Combine the folder and file name
    return os.path.join(folder, file)

def run_pylint(scan_path):
    """
    Runs both Pylint and Flake8 on the specified scan_path, combines their outputs,
    and returns the output grouped by file/module.
    
    Args:
        scan_path (str): The file or directory path to scan.
        
    Returns:
        dict: A dictionary containing the combined output and any errors.
    """
    print("Tool: Pylint (with Flake8 for Dlint)")
    try:
        # Run Pylint and capture the output and errors
        pylint_cmd = ['pylint', scan_path]
        process_pylint = subprocess.run(pylint_cmd, capture_output=True, text=True, check=False)
        pylint_output_lines = process_pylint.stdout.splitlines()

        # Run Flake8 and capture the output and errors
        flake8_cmd = ['flake8', scan_path]
        process_flake8 = subprocess.run(flake8_cmd, capture_output=True, text=True, check=False)
        flake8_output_lines = process_flake8.stdout.splitlines()

        # Store output by file/module
        combined_output = []
        module_output = {}  # Dictionary to track output per module
        current_module = None

        # Process Pylint output and normalize paths
        for line in pylint_output_lines:
            if line.startswith("************* Module"):
                # Normalize Pylint module path by converting it to a relative file path
                current_module = line.split()[-1].replace(".", os.sep) + ".py"
                current_module = trim_path(current_module)  # Apply the trimming to Pylint paths
                module_output[current_module] = [line]  # Initialize with the module line
            elif current_module:
                module_output[current_module].append(line)

        # Process Flake8 output and normalize paths
        for line in flake8_output_lines:
            if line.startswith(".."):
                file_path = os.path.normpath(line.split(":")[0])
            else:
                file_path = os.path.normpath(line.split(":")[1])

            file_path = trim_path(file_path)
            if file_path in module_output:
                # Prepend Flake8 output to the beginning of the existing module output
                module_output[file_path].insert(1, f"Flake8: {line}")
            else:
                # If the module doesn't exist in Pylint output, create a new entry
                module_output[file_path] = [f"Flake8: {line}"]

        # Join the combined output into a single string
        combined_output_str = "\n".join(
            "\n".join(output_lines) for output_lines in module_output.values())

        # Return the combined output
        return {
            "output": combined_output_str,
            "error": process_pylint.stderr if process_pylint.returncode != 0 else None,
        }

    except subprocess.CalledProcessError as e:
        # Log any subprocess errors
        logger.error("Execution failed: %s", e)
        return {"error": "Execution failed", "details": str(e)}
    