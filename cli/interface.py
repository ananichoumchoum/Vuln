"""
Display the CLI menu
"""
import os
from InquirerPy import prompt
from colorama import Fore, Style, init
from utils.validation import is_valid_directory, is_valid_requirements_file

# Initialize colorama for cross-platform support
init(autoreset=True)


def display_logo():
    """
    Display the refined VULN CLI logo
    """
    logo = """
+================================================================+
|| ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ||
||                                                               ||
||   ██████                                             ██████   ||
||   █    █                                             █    █   ||
||   █ ██ █                                             █ ██ █   ||
||   █    █                                             █    █   ||
||   ██████                                             ██████   ||
||                                                               ||
||          ██        ██  ██    ██ ██      ███    ██             ||
||           ██      ██   ██    ██ ██      ████   ██             ||
||            ██    ██    ██    ██ ██      ██ ██  ██             ||
||             ██  ██     ██    ██ ██      ██  ██ ██             ||
||              ████      ████████ ███████ ██   ████             ||
||                                                               ||
||   ██████                                             ██████   ||
||   █    █                                             █    █   ||
||   █ ██ █                                             █ ██ █   ||
||   █    █           Static Code Scanner 2.0           █    █   ||
||   ██████                                             ██████   ||
||                                                               ||
|| ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ ||
+================================================================+

"""
    print(logo)
    print(
        Fore.GREEN + "\nWelcome to the " + Style.BRIGHT +
        "VULN CLI!" + Style.RESET_ALL
    )
    print(
        "Your one-stop shop for scanning, and eliminating bad practices."
    )
    print(
        "We’re here to save you from your bad security practices..."
        " or at least point them out.\n"
    )
    print(
        "Whether it's linting your code or making sure"
        " you didn't hardcode your API keys,"
    )
    print("we're here to catch your mistakes before your boss does. 😎\n")
    print("Remember, security isn't a product, it's a process.")
    print("...and if that process involves pushing sensitive data to GitHub,")
    print("well, TruffleHog is here to keep your secrets secret. 🔐\n")

    print(
        Fore.MAGENTA + "Pro tip:" + Fore.RESET + " If you see a security "
        "warning and think, 'that’s future me’s problem,'"
    )
    print(
        "Just remember... future you is terrible at solving present"
        " you's problems. 😬\n"
    )

    print(
        "Let’s dive in and clean up your code before the real hackers do! 🚀\n"
    )


def show_main_menu():
    """
    Display the main menu for the VULN CLI.
    """
    menu_questions = [
        {
            "type": "list",
            "message": "Select an option:",
            "choices": ["Start Test", "Exit"],
            "name": "main_menu_choice"
        }
    ]
    answer = prompt(menu_questions)
    return answer['main_menu_choice']


def show_python_menu():
    """
    Display the Python test menu for the VULN CLI.
    """
    python_menu_questions = [
        {
            "type": "list",
            "message": "Python Tests:",
            "choices": [
                "Run All Tests", "Security", "Linting", "Safety", "Bandit",
                "Checkov", "trufflehog", "Flake8", "Pylint", "Mypy", "Radon",
                "Exit"
            ],
            "name": "python_menu_choice"
        }
    ]
    answer = prompt(python_menu_questions)
    return answer['python_menu_choice']


def ask_for_scan_path():
    """
    Prompt the user to enter the scan path (file or directory) to scan.
    Validates the input before returning the path.

    Returns:
        str: The path to the file or directory to scan.
    """
    while True:
        scan_path_question = [
            {
                "type": "input",
                "message": "Enter the path to the file or directory to scan:",
                "name": "scan_path"
            }
        ]
        answer = prompt(scan_path_question)
        scan_path = answer['scan_path']

        # Validate the directory or file
        try:
            # The user can input either a directory or file, we validate both
            if os.path.isdir(scan_path):
                is_valid_directory(scan_path)
                return os.path.abspath(scan_path)
            if os.path.isfile(scan_path):
                is_valid_requirements_file(scan_path)
                return os.path.abspath(scan_path)
            print(f"Error: '{scan_path}' is neither a valid file nor"
                  f" directory. Please try again.")
        except ValueError as e:
            print(str(e))
