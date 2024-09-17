"""
Unit tests for the Pylint runner module.
"""
import unittest
import subprocess
from unittest.mock import patch
from vuln.core.pylint_runner import run_pylint

class TestPylintRunner(unittest.TestCase):
    """Tests for the Pylint runner methods."""

    @patch('subprocess.run')
    def test_pylint_with_no_issues(self, mock_subprocess):
        """Test Pylint runner when no issues are found (rated 10.00/10)."""

        mock_subprocess.return_value.stdout = (
            "--------------------------------------------------------------------\n"
            "Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)\n"
        )
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stderr = ""

        results = run_pylint('D:/valid/file.py')

        self.assertIsInstance(results, dict)
        self.assertIn('output', results)
        self.assertIn("Your code has been rated at 10.00/10", results['output'])
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_pylint_with_linting_issues(self, mock_subprocess):
        """Test Pylint runner when linting issues are found."""

        mock_subprocess.return_value.stdout = (
            "************* Module valid.file_with_issues\n"
            "valid/file_with_issues.py:1:0: C0114: Missing module docstring\n"
            "--------------------------------------------------------------------\n"
            "Your code has been rated at 7.50/10 (previous run: 8.00/10, -0.50)\n"
        )
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = None

        results = run_pylint('valid/file_with_issues.py')
        self.assertIn('output', results)
        self.assertIn("Your code has been rated at 7.50/10", results['output'])
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_pylint_fatal_error(self, mock_subprocess):
        """Test Pylint runner when a fatal error occurs."""

        mock_subprocess.return_value.stderr = "Fatal error occurred."
        mock_subprocess.return_value.returncode = 2

        results = run_pylint('invalid/file.py')
        self.assertIn('error', results)
        self.assertEqual(results['error'], "Fatal error occurred.")

    @patch('subprocess.run')
    def test_pylint_execution_failure(self, mock_subprocess):
        """Test Pylint runner when subprocess fails."""

        mock_subprocess.side_effect = subprocess.CalledProcessError(
            1, 'pylint', stderr="Pylint execution failed."
        )

        results = run_pylint('valid/file.py')
        self.assertIn("Execution failed", results['error'])

if __name__ == '__main__':
    unittest.main()
