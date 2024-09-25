"""
This module serves as entry point for running security tools on specified paths
"""

import argparse
import os
from cli.interface import (
    display_logo, show_main_menu, show_python_menu, ask_for_scan_path
)
from utils.validation import (
    is_valid_requirements_file, get_tools_for_category,
    ask_for_requirements_file
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
    """
    Main function that parses CLI arguments and runs the specified tools.
    """
    parser = argparse.ArgumentParser(
        description="Vuln: Security scanner for multiple tools")

    # Accept the requirements.txt path for Safety
    parser.add_argument('--requirements-file',
                        type=is_valid_requirements_file,
                        default='requirements.txt',
                        help="Path to the requirements file.")

    # Display the logo and main menu
    display_logo()

    while True:
        main_choice = show_main_menu()

        if main_choice == "Start Test":
            python_choice = show_python_menu()

            # Map the user input to lowercase tool names in TOOLS dictionary
            tool_key = python_choice.lower()

            if python_choice == "Run All Tests":
                tools_to_run = list(TOOLS.keys())

            elif python_choice == "Security":
                tools_to_run = get_tools_for_category("Security")

            elif python_choice == "Linting":
                tools_to_run = get_tools_for_category("Linting")

            # If a specific tool is selected (like "Bandit", "Safety", etc.)
            elif tool_key in TOOLS:
                tools_to_run = [tool_key]

            elif python_choice == "Exit":
                print("Exiting...")
                break

            else:
                print(f"Unknown selection: {python_choice}")
                continue

            # Ask the user for the scan path (file or directory) to scan
            scan_path = ask_for_scan_path()

            # Run the selected tools
            run_selected_tools(tools_to_run, scan_path)

        elif main_choice == "Exit":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
