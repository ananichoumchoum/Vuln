"""
Unit tests for the Checkov runner module.
"""
import unittest
import subprocess
from unittest.mock import patch, MagicMock
from vuln.core.checkov_runner import run_checkov

class TestRunCheckov(unittest.TestCase):
    """Tests for Checkov runner methods."""
    @patch('subprocess.run')
    def test_run_checkov_success(self, mock_subprocess):
        """Test successful Checkov scan with no issues."""
        # Mock a successful Checkov run
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = 'No issues found.'
        mock_process.stderr = ''
        mock_subprocess.return_value = mock_process

        scan_path = 'valid/path/to/scan'
        result = run_checkov(scan_path)

        self.assertIn("No issues found", result["output"])
        self.assertEqual(result["error"], "No error")

    @patch('subprocess.run')
    def test_run_checkov_with_warnings(self, mock_subprocess):
        """Test Checkov scan with warnings or security misconfigurations."""
        # Mock a Checkov run with warnings
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = 'Security misconfigurations found.'
        mock_process.stderr = 'Warning: some security issues found.'
        mock_subprocess.return_value = mock_process

        scan_path = 'valid/path/to/scan'
        result = run_checkov(scan_path)

        self.assertIn("Security misconfigurations found", result["output"])
        self.assertIn("some security issues found", result["error"])

    @patch('subprocess.run')
    def test_run_checkov_execution_failure(self, mock_subprocess):
        """Test Checkov scan failure due to execution error."""
        # Mock a subprocess.CalledProcessError
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'checkov')

        scan_path = 'invalid/path'
        result = run_checkov(scan_path)

        self.assertIn("Checkov execution failed", result["error"])

if __name__ == '__main__':
    unittest.main()
