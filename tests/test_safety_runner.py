"""
Unit tests for the Safety runner module.
"""

import unittest
import subprocess
from unittest.mock import patch
from vuln.core.safety_runner import run_safety

class TestSafetyRunner(unittest.TestCase):
    """Tests for the Safety runner methods."""

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_safety_with_valid_file(self, mock_subprocess, _mock_exists):
        """Test Safety runner with a valid requirements file."""
        mock_subprocess.return_value.stdout = '{"vulnerabilities": []}'
        mock_subprocess.return_value.returncode = 0

        results = run_safety('valid/requirements.txt')
        self.assertIsInstance(results, dict)
        self.assertIn('vulnerabilities', results)

    @patch('os.path.exists', return_value=False)
    @patch('subprocess.run')
    def test_safety_with_invalid_file(self, _mock_subprocess, _mock_exists):
        """Test Safety runner with an invalid requirements file."""
        with self.assertRaises(FileNotFoundError):
            run_safety('invalid/requirements.txt')

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_safety_fails(self, mock_subprocess, _mock_exists):
        """Test Safety runner when subprocess fails."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            1, 'safety', stderr="Simulated Safety error")

        results = run_safety('valid/requirements.txt')
        self.assertIn('error', results)
        self.assertEqual(results['error'], 'Safety scan failed')
        self.assertIn('Simulated Safety error', results['details'])

if __name__ == '__main__':
    unittest.main()
