import unittest
from unittest.mock import patch
import subprocess
from vuln.core.mypy_runner import run_mypy

class TestMypyRunner(unittest.TestCase):
    """Tests for the MyPy runner methods."""

    @patch('subprocess.run')
    def test_mypy_with_no_issues(self, mock_subprocess):
        """Test MyPy runner when no type-checking issues are found (exit code 0)."""
        # Mock subprocess to simulate MyPy running without issues
        mock_subprocess.return_value.stdout = "Success: no issues found in 1 source file"
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stderr = ""

        results = run_mypy('valid/file.py')
        self.assertIsInstance(results, dict)
        self.assertIn('output', results)
        self.assertEqual(results['output'], "Success: no issues found in 1 source file")
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_mypy_with_type_issues(self, mock_subprocess):
        """Test MyPy runner when type-checking issues are found (exit code 1)."""
        # Mock subprocess to simulate MyPy finding type issues
        mock_subprocess.return_value.stdout = (
            "valid/file_with_issues.py:3: error: Incompatible types in assignment"
        )
        mock_subprocess.return_value.returncode = 1
        mock_subprocess.return_value.stderr = None

        results = run_mypy('valid/file_with_issues.py')
        self.assertIsInstance(results, dict)
        self.assertIn('output', results)
        self.assertEqual(results['output'], "valid/file_with_issues.py:3: error: Incompatible types in assignment")
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_mypy_with_fatal_error(self, mock_subprocess):
        """Test MyPy runner when a fatal error occurs (exit code 2)."""
        # Mock subprocess to simulate a fatal error (exit code 2)
        mock_subprocess.return_value.stdout = ""
        mock_subprocess.return_value.returncode = 2
        mock_subprocess.return_value.stderr = "error: failed to find module"

        results = run_mypy('invalid/file.py')
        self.assertIn('error', results)
        self.assertEqual(results['error'], "error: failed to find module")

    @patch('subprocess.run')
    def test_mypy_execution_failure(self, mock_subprocess):
        """Test MyPy runner when subprocess fails."""
        # Mock subprocess to raise a CalledProcessError
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            1, 'mypy', stderr="MyPy execution failed."
        )

        results = run_mypy('valid/file.py')
        self.assertIn("error", results)
        self.assertIn("MyPy execution failed", results['error'])

if __name__ == '__main__':
    unittest.main()
