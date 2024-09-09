import argparse
from vuln.core.tool_runner import run_tool, format_results, TOOLS

def main():
    parser = argparse.ArgumentParser(description="Vuln: Security scanner for multiple tools")
    
    # Accept the path to scan as an argument
    parser.add_argument('--scan-path', type=str, required=True, help="Path to the directory or file to scan")
    
    # Accept a list of tools to run, default is all tools if not specified
    parser.add_argument('--tools', type=str, nargs='+', help="List of tools to run (e.g., bandit, safety)")

    args = parser.parse_args()

    # If no specific tools are provided, default to running all tools
    tools_to_run = args.tools if args.tools else list(TOOLS.keys())

    # Run each specified tool
    for tool in tools_to_run:
        try:
            results = run_tool(tool, args.scan_path)
            format_results(tool, results)
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as ex:
            print(f"Unexpected error occurred while running {tool}: {ex}")

if __name__ == "__main__":
    main()
