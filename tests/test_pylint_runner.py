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
        """Test Pylint runner with no linting issues."""
        # Mock subprocess to simulate Pylint running without issues
        mock_subprocess.return_value.stdout = "Pylint scan completed with no issues."
        mock_subprocess.return_value.returncode = 0

        results = run_pylint('valid/file.py')
        self.assertIsInstance(results, dict)
        self.assertIn('pylint_output', results)
        self.assertEqual(results['pylint_output'], "Pylint scan completed with no issues.")
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_pylint_with_linting_issues(self, mock_subprocess):
        """Test Pylint runner with linting issues found."""
        # Mock subprocess to simulate Pylint finding linting issues
        mock_subprocess.return_value.stdout = "Some linting issues found."
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = None

        results = run_pylint('valid/file_with_issues.py')
        self.assertIn('pylint_output', results)
        self.assertEqual(results['pylint_output'], "Some linting issues found.")
        self.assertIsNone(results['error'])


    @patch('subprocess.run')
    def test_pylint_fatal_error(self, mock_subprocess):
        """Test Pylint runner when a fatal error occurs."""
        # Mock subprocess to simulate a fatal error (exit code 2)
        mock_subprocess.return_value.stderr = "Fatal error occurred."
        mock_subprocess.return_value.returncode = 2

        results = run_pylint('invalid/file.py')
        self.assertIn('error', results)
        self.assertEqual(results['error'], "Fatal error occurred.")

    @patch('subprocess.run')
    def test_pylint_internal_error(self, mock_subprocess):
        """Test Pylint runner when an internal error occurs (exit code 20)."""
        # Mock subprocess to simulate an internal Pylint error with exit code 20
        mock_subprocess.return_value.stdout = "Pylint internal error."
        mock_subprocess.return_value.returncode = 20
        mock_subprocess.return_value.stderr = None  # Internal error but no stderr

        results = run_pylint('valid/file.py')
        self.assertIn('pylint_output', results)
        self.assertEqual(results['pylint_output'], "Pylint internal error.")
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_pylint_execution_failure(self, mock_subprocess):
        """Test Pylint runner when subprocess fails."""
        # Mock subprocess to raise a CalledProcessError
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            1, 'pylint', stderr="Pylint execution failed."
        )

        results = run_pylint('valid/file.py')
        self.assertIn("Command 'pylint' returned non-zero exit status", results['details'])

if __name__ == '__main__':
    unittest.main()
