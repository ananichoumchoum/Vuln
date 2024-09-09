from vuln.core.bandit_runner import run_bandit
from tabulate import tabulate
import textwrap

# TODO Tool Registry
TOOLS = {
    'bandit': run_bandit,
    # Add future tools like 'safety': run_safety
}

def run_tool(tool_name, scan_path):
    """
    Runs the specified tool and returns the results.
    - tool_name: The name of the tool (e.g., 'bandit').
    - scan_path: The path to scan.
    """
    if tool_name in TOOLS:
        tool_function = TOOLS[tool_name]
        return tool_function(scan_path)
    else:
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
