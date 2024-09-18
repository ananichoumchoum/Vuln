import argparse
import os
from vuln.core.tool_runner import run_tool, format_results, TOOLS

def is_valid_directory(path):
    """Check if the provided path is a valid directory."""
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"Path {path} does not exist.")
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Path {path} is not a directory.")
    return os.path.abspath(path)

def is_valid_requirements_file(path):
    """Check if the provided file exists."""
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"File {path} does not exist.")
    if not os.path.isfile(path) or not path.endswith('.txt'):
        raise argparse.ArgumentTypeError(f"File {path} is not a valid .txt file.")
    return os.path.abspath(path)

def main():
    parser = argparse.ArgumentParser(description="Vuln: Security scanner for multiple tools")

    # Accept the path to scan as an argument
    parser.add_argument('--scan-path', type=is_valid_directory, required=True,
                        help="Path to the directory or file to scan")

    # Accept the requirements.txt path for Safety, default to requirements.txt in the current working directory
    parser.add_argument('--requirements-file', type=str, default='requirements.txt',
                        help="Path to the requirements file (for Safety). Default: ./requirements.txt")

    # Accept a list of tools to run, default is all tools if not specified
    parser.add_argument('--tools', type=str, nargs='+',
                        help="List of tools to run (e.g., bandit, safety, pylint, trufflehog, checkov)")

    args = parser.parse_args()

    # If no specific tools are provided, default to running all tools
    tools_to_run = args.tools if args.tools else list(TOOLS.keys())

    # Run each specified tool
    for tool in tools_to_run:
        try:
            if tool == 'safety':
                # Ensure the requirements file path is constructed correctly
                requirements_file_path = args.requirements_file
                # If the requirements file is not in the scan path, use the default 'requirements.txt' from the scan path
                if not os.path.isabs(requirements_file_path):
                    requirements_file_path = os.path.join(args.scan_path, requirements_file_path)

                # Check if the requirements file exists in the constructed path
                if not os.path.exists(requirements_file_path):
                    print(f"Warning: Requirements file '{requirements_file_path}' does not exist. Skipping Safety scan.")
                    continue

                results = run_tool(tool, requirements_file_path)
            else:
                # Run Bandit or other tools that use the scan path directly
                results = run_tool(tool, args.scan_path)

            format_results(tool, results)
        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
        except PermissionError as perm_error:
            print(f"Permission denied: {perm_error}")
        except Exception as ex:
            print(f"Unexpected error occurred while running {tool}: {ex}")

if __name__ == "__main__":
    main()
