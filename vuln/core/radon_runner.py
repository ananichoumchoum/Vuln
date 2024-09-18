"""
This module contains functions to run Radon on a given file or directory
and return the complexity analysis output along with any errors encountered
"""
import subprocess
import logging

# Initialize logger
logger = logging.getLogger(__name__)


def run_radon(scan_path):
    """
    Runs Radon Cyclomatic Complexity on scan_path and formats the output

    Args:
        scan_path (str): The file or directory path to scan with Radon

    Returns:
        dict: A dictionary containing the output of the scan or error message
    """
    print("Tool: Radon")
    try:
        # Command to run Radon
        radon_cmd = ['radon', 'cc', scan_path, '-s']
        process = subprocess.run(
            radon_cmd, capture_output=True, text=True, check=False)

        # Capture the raw output and split by lines
        output_lines = process.stdout.splitlines()

        # Skip A and B grades and format the output for C or higher
        format_output = []
        high_complexity_found = False
        current_file = None

        for line in output_lines:
            # If the line contains a file path
            if not line.startswith((' ', 'F', 'M', 'C')):
                current_file = line
                continue

            parts = line.split()
            if len(parts) < 4:
                continue

            complexity_grade = parts[4]
            if complexity_grade in ['A', 'B']:
                continue  # Skip low complexity entries

            high_complexity_found = True
            func_type = "Function" if parts[0] == 'F' else "Method"
            line_number = parts[1].split(":")[0]
            func_name = parts[2]
            complexity_desc = {
                'C': 'Moderate Complexity',
                'D': 'High Complexity',
                'E': 'Very High Complexity',
                'F': 'Unmaintainable Complexity'
            }.get(complexity_grade, 'Unknown Complexity')

            # Append the formatted string
            format_output.append(
                f"{current_file}:\n"
                f"  {func_type}: {func_name}\n"
                f"    Line: {line_number}\n"
                f"    Complexity: {complexity_grade} ({complexity_desc})\n"
            )

        # If no high complexity functions were found, add a message
        if not high_complexity_found:
            format_output.append("All functions have low complexity(A or B)")

        # Return the final formatted output
        return {
            "output": "\n".join(format_output),
            "error": process.stderr if process.returncode != 0 else None
        }

    except subprocess.CalledProcessError as e:
        logger.error("Radon scan failed with Process error: %s", e.stderr)
        return {"error": "Radon scan failed", "details": e.stderr}
