"""
This module contains functions to run and format results from various security tools.
"""
from tabulate import tabulate  # Third-party library
from vuln.core.bandit_runner import run_bandit  # First-party import

# TODO: Add other tools to the Tool Registry, such as Safety, in future versions
TOOLS = {
    'bandit': run_bandit,
    # Add future tools like 'safety': run_safety
}

def run_tool(tool_name, scan_path):
    """
    Runs the specified tool and returns the results.
    Parameters:
    - tool_name: The name of the tool (e.g., 'bandit').
    - scan_path: The path to scan.
    
    Returns:
    - dict: The results from the tool, typically parsed JSON.
    """
    if tool_name in TOOLS:
        tool_function = TOOLS[tool_name]
        return tool_function(scan_path)
    raise ValueError(f"Tool '{tool_name}' not found.")

def format_results(tool_name, results):
    """
    Formats and prints the results for a given tool.
    - tool_name: The name of the tool (e.g., 'bandit').
    - results: The results from the tool.
    """
    if 'results' in results and results['results']:
        print(f"Tool: {tool_name.capitalize()}")
        print(f"Issue Count: {len(results['results'])}")

        table_data = []
        more_info = []
        for issue in results['results']:
            more_info.append(issue['more_info'])
            table_data.append([
                issue['filename'],
                issue['line_number'],
                issue['issue_text'],
                issue['issue_severity'],
                issue['issue_confidence'],
            ])

        headers = ["File", "Line", "Description", "Severity", "Confidence"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))
        print("More Info about these issues:")
        for info in more_info:
            print(info)

    elif 'error' in results:
        print(f"Error: {results['error']}\nDetails: {results['details']}")
    else:
        print(f"No issues found by {tool_name}.")
