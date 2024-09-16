"""
This module serves as the entry point for running security tools on specified paths.
"""

import argparse
import os
from vuln.core.tool_runner import run_tool, format_results, TOOLS

def main():
    """
    Main function that parses command-line arguments and runs the specified security tools.
    """
    parser = argparse.ArgumentParser(description="Vuln: Security scanner for multiple tools")

    # Accept the path to scan as an argument
    parser.add_argument('--scan-path', type=str, required=True,
                        help="Path to the directory or file to scan")

    # Accept the requirements.txt path for Safety
    parser.add_argument('--requirements-file', type=str, default='requirements.txt',
                        help="Path to the requirements file (for Safety)")

    # Accept a list of tools to run, default is all tools if not specified
    parser.add_argument('--tools', type=str, nargs='+',
                        help="List of tools to run (e.g., bandit, safety, pylint, trufflehog)")

    args = parser.parse_args()

    # If no specific tools are provided, default to running all tools
    tools_to_run = args.tools if args.tools else list(TOOLS.keys())

    # Run each specified tool
    for tool in tools_to_run:
        try:
            if tool == 'safety':
                # Ensure the requirements file path is properly formed
                requirements_file_path = os.path.join(args.scan_path, args.requirements_file)
                results = run_tool(tool, requirements_file_path)
            else:
                # Run Bandit or other tools that use the scan path directly
                results = run_tool(tool, args.scan_path)

            format_results(tool, results)
        except Exception as ex:  # Catching any unexpected errors
            print(f"Unexpected error occurred while running {tool}: {ex}")

if __name__ == "__main__":
    main()
