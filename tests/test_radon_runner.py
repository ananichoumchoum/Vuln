"""
Unit tests for the Radon runner module.
"""
import unittest
import subprocess
from unittest.mock import patch
from vuln.core.radon_runner import run_radon


class TestRadonRunner(unittest.TestCase):
    """Tests for the Radon runner."""

    @patch('subprocess.run')
    def test_radon_with_low_complexity(self, mock_subprocess):
        """Test Radon runner with low complexity (A and B grades)."""
        mock_subprocess.return_value.stdout = (
            "..\\python_test\\app.py\n"
            "    F 3:0 main - A (1)\n"
            "    F 8:0 unused_function - A (1)\n"
        )
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stderr = ""

        results = run_radon('valid/file.py')
        self.assertIsInstance(results, dict)
        self.assertIn('output', results)
        self.assertIn("All functions have low complexity (A or B).", results['output'])
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_radon_with_high_complexity(self, mock_subprocess):
        """Test Radon runner with high complexity (C or higher)."""
        mock_subprocess.return_value.stdout = (
            "..\\python_test\\complexity.py\n"
            "    F 1:0 higher_complexity_logic - C (19)\n"
        )
        mock_subprocess.return_value.returncode = 0
        mock_subprocess.return_value.stderr = ""

        results = run_radon('valid/file.py')
        self.assertIn('output', results)
        self.assertIn("Function: higher_complexity_logic", results['output'])
        self.assertIn("Complexity: C (Moderate Complexity)", results['output'])
        self.assertIsNone(results['error'])

    @patch('subprocess.run')
    def test_radon_execution_error(self, mock_subprocess):
        """Test Radon runner when a subprocess error occurs."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'radon')

        results = run_radon('invalid/scan_path')

        self.assertIn("Radon scan failed", results['error'])

if __name__ == '__main__':
    unittest.main()
