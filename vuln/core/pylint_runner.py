"""
This module contains functions to run Pylint with Dlint on a given file/dir
and return the scan output along with any errors encountered.
"""
import subprocess
import logging
import os
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)
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


def run_subprocess(command):
    """Run a subprocess and return the output."""
    return subprocess.run(command, capture_output=True, text=True, check=False)


def process_module_output(lines, trim_path):
    """Process and normalize the output, organizing by module."""
    module_output = {}
    current_module = None
    for line in lines:
        if line.startswith("************* Module"):
            current_module = line.split()[-1].replace(".", os.sep) + ".py"
            current_module = trim_path(current_module)
            module_output[current_module] = [line]
        elif current_module:
            module_output[current_module].append(line)
    return module_output


def process_flake8_output(lines, module_output, trim_path):
    """Process Flake8 output and merge with Pylint output."""
    for line in lines:
        if ':' in line:
            file_path = os.path.normpath(
                line.split(":")[0] if line.startswith("..")
                else line.split(":")[1])
            file_path = trim_path(file_path)
            if file_path in module_output:
                module_output[file_path].insert(1, f"Flake8: {line}")
            else:
                module_output[file_path] = [f"Flake8: {line}"]
    return module_output


def run_pylint(scan_path):
    """Run Pylint and Flake8, combine their outputs, and return results"""
    print(Fore.YELLOW + "Tool: Pylint with Flake8(Dlint)" + Style.RESET_ALL)
    try:
        # Run Pylint
        pylint_output = run_subprocess(['pylint', scan_path])
        pylint_output_lines = pylint_output.stdout.splitlines()

        # Run Flake8
        flake8_output = run_subprocess(['flake8', scan_path])
        flake8_output_lines = flake8_output.stdout.splitlines()

        # Process the outputs
        module_output = process_module_output(pylint_output_lines, trim_path)
        module_output = process_flake8_output(
            flake8_output_lines, module_output, trim_path)

        # Combine the output
        combined_output_str = "\n".join(
            "\n".join(output_lines) for output_lines in module_output.values())

        # Return the combined output
        return {
            "output": combined_output_str,
            "error": pylint_output.stderr if pylint_output.returncode != 0
            else None,
        }

    except subprocess.CalledProcessError as e:
        logger.error("Execution failed: %s", e)
        return {"error": "Execution failed", "details": str(e)}
