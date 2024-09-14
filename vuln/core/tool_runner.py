"""
This module contains functions to run and format results from various security tools.
"""

import textwrap
from tabulate import tabulate
from vuln.core.bandit_runner import run_bandit
from vuln.core.safety_runner import run_safety
from vuln.core.pylint_runner import run_pylint

TOOLS = {
    'bandit': run_bandit,
    'safety': run_safety,
    'pylint': run_pylint,
}

def run_tool(tool_name, scan_path):
    """
    Runs the specified tool and returns the results.
    Parameters:
    - tool_name: The name of the tool (e.g., 'bandit', 'safety').
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
    - tool_name: The name of the tool (e.g., 'bandit', 'safety').
    - results: The results from the tool.
    """
    if tool_name == 'bandit':
        # Handling Bandit results
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

    if tool_name == 'safety' and 'vulnerabilities' in results:
        print(f"Tool: {tool_name.capitalize()}")
        print(f"Issue Count: {len(results['vulnerabilities'])}")

        # Prepare table data for vulnerabilities in Safety's results
        table_data = []
        safety_more_info = []
        for vulnerability in results['vulnerabilities']:
            # Wrapping the advisory to fit the table's width
            advisory_wrapped = textwrap.wrap(vulnerability['advisory'], width=70)
            first_line_advisory = advisory_wrapped[0] if advisory_wrapped else ''
            remaining_advisory = "\n".join(
                advisory_wrapped[1:]) if len(advisory_wrapped) > 1 else ''

            safety_more_info.append(vulnerability['more_info_url'])

            # First row: Package, Installed Version, Vulnerable Spec, first part of Description
            table_data.append([
                vulnerability['package_name'],
                vulnerability['analyzed_version'],
                vulnerability['vulnerable_spec'][0],
                first_line_advisory,  # Only the first line of the advisory here
            ])

            # Second row: Empty fields for Package, Version, etc., and rest of Description
            if remaining_advisory:
                table_data.append([
                    '',  # Empty package name
                    '',  # Empty version
                    '',  # Empty vulnerable spec
                    remaining_advisory,  # Rest of the advisory here
                ])

        headers = ["Package", "Installed Version", "Vulnerable Spec", "Description"]
        print(tabulate(table_data, headers=headers, tablefmt="pretty"))

        print("More Info about these issues:")
        for info in safety_more_info:
            print(info)
        
    elif tool_name == 'pylint':
        # Handling Pylint results
        if results.get('pylint_output'):
            print(results['pylint_output'])

        # Print the score if present
        if tool_name == 'pylint' and 'score' in results:
            print(f"Pylint score: {results['score']}/10")
        
        # Print error if it's present
        if results.get('error'):
            print(f"Error: {results['error']}")
