import argparse
import os
from cli.interface import (
    display_logo, show_main_menu, show_python_menu, ask_for_scan_path
)
from utils.validation import (
    is_valid_requirements_file, get_tools_for_category, ask_for_requirements_file
)
from vuln.core.tool_runner import format_results, TOOLS, run_tool


def run_selected_tools(tools_to_run, scan_path):
    """
    Runs the selected tools with the provided scan path.
    """
    for tool in tools_to_run:
        try:
            if tool == 'safety':
                requirements_file_path = ask_for_requirements_file(
                    scan_path, 'requirements.txt')

                if not os.path.exists(requirements_file_path):
                    print(f"Warning: Requirements file "
                          f"'{requirements_file_path}' does not exist."
                          f"Skipping Safety scan.")
                    continue

                # Run the tool with the correct requirements file path
                results = run_tool(tool, requirements_file_path)
            else:
                # Run the other tools with the user-provided scan path
                results = run_tool(tool, scan_path)

            format_results(tool, results)

        except FileNotFoundError as fnf_error:
            print(f"File not found: {fnf_error}")
        except PermissionError as perm_error:
            print(f"Permission denied: {perm_error}")
        except OSError as os_error:
            print(f"OS error: {os_error}")


def main():
    parser = argparse.ArgumentParser(
        description="Vuln: Security scanner for multiple tools")

    # Accept the path to scan as an argument
    parser.add_argument('--scan-path', type=is_valid_directory, required=True,
                        help="Path to the directory or file to scan")

    # Accept the requirements.txt path for Safety
    parser.add_argument('--requirements-file',
                        type=is_valid_requirements_file,
                        default='requirements.txt',
                        help="Path to the requirements file. "
                             "Default: ./requirements.txt")

    # Accept a list of tools to run, default is all tools if not specified
    parser.add_argument('--tools', type=str, nargs='+',
                        help="List of tools to run "
                        "(e.g., bandit, safety, pylint, trufflehog, checkov)")

    args = parser.parse_args()

    # If no specific tools are provided, default to running all tools
    tools_to_run = args.tools if args.tools else list(TOOLS.keys())

    # Run each specified tool
    for tool in tools_to_run:
        try:
            if tool == 'safety':
                # Ensure the requirements file path is constructed correctly
                requirements_file_path = args.requirements_file
                # If the requirements file is not in the scan path
                # use the default 'requirements.txt' from the scan path
                if not os.path.isabs(requirements_file_path):
                    requirements_file_path = os.path.join(
                        args.scan_path, requirements_file_path)

                # Check if the requirements file exists in the constructed path
                if not os.path.exists(requirements_file_path):
                    print(f"Warning: Requirements file"
                          f"'{requirements_file_path}'"
                          f" does not exist. Skipping Safety scan.")
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

            # Run the selected tools
            run_selected_tools(tools_to_run, scan_path)

        elif main_choice == "Exit":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
