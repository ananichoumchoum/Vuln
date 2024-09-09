# Vuln: Python Security Scanner Tool

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
   1. [Sample Output](#sample-output)
5. [Running Tests](#running-tests)
6. [Branching Strategy](#branching-strategy)
7. [Contributing](#contributing)
8. [License](#license)

### Overview
**Vuln** is a Python-based security tool designed to scan Python codebases for common security issues. This tool integrates with popular security scanning tools such as Bandit and provides a modular and extendable framework to help developers maintain secure code.

## Features
- **Bandit Module**: Scans Python code for security issues like hardcoded secrets, SQL injection, and more.
- **Error Handling**: Ensures graceful failure with informative error messages.
- **Modular Design**: Easily extend the tool with additional security scanners.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/vuln.git
    cd vuln
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate     # On Windows
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
4. Install Snyk using npm (Node.js must be installed):
    ```bash
    npm install -g snyk

## Usage
To scan a Python project for security issues using all tools, run:
```bash
python -m main --scan-path ../path/to/your/file
```

To scan a Python project for security issues using specific tools like Bandit, run:
```bash
python -m main --scan-path ../path/to/your/file --tools bandit
```


### Sample Output
    Tool: Bandit
    Issue Count: 3
    Description: The description is a pretty table with File, Line, Description, Severity and Confidence

The results are JSON-parsed, making it easy to further process or integrate into other tools if necessary.

## Running Tests
Unit tests are provided to verify the functionality of the Bandit module. You can run the tests using:

```bash
python -m unittest tests.test_bandit_runner
```

Otherwise you can run this command:

```bash
python -m unittest discover -s tests
```

This command will run all unit tests and ensure that the module works as expected.

## Branching Strategy
To maintain a clean and organized codebase, we use the following Git branching strategy:

- main: Contains production-ready code.
- develop: Integration branch for development features.
- feature/bandit-module: Dedicated branch for the Bandit security scanner module.

All new features should be developed in their own feature branches and merged into `develop` after review and testing.

## Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch:
    ```bash
    Copy code
    git checkout -b feature/your-feature
3. Commit your changes:
    ```bash
    Copy code
    git commit -m 'Add your feature'
4. Push the branch:
    ```bash
    Copy code
    git push origin feature/your-feature
5. Open a pull request to the `develop` branch.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

