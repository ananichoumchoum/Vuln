"""
Unit tests for the Bandit runner module.
"""

import unittest  # Standard library
import subprocess  # Standard library
from unittest.mock import patch  # Standard library

from vuln.core.bandit_runner import run_bandit  # Local project import

class TestBanditRunner(unittest.TestCase):
    """Tests for Bandit runner methods."""

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_bandit_with_valid_path(self, mock_subprocess, _mock_exists):
        """Test Bandit runner with a valid path."""
        mock_subprocess.return_value.stdout = '{"results": []}'
        mock_subprocess.return_value.returncode = 0
        results = run_bandit('valid/path')
        self.assertIsInstance(results, dict)
        self.assertIn('results', results)

    @patch('os.path.exists', return_value=False)
    @patch('subprocess.run')
    def test_bandit_with_invalid_path(self, _mock_subprocess, _mock_exists):
        """Test Bandit runner with an invalid path."""
        with self.assertRaises(FileNotFoundError):
            run_bandit('invalid/path')

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_bandit_fails(self, mock_subprocess, _mock_exists):
        """Test Bandit runner with a subprocess failure."""
        mock_subprocess.side_effect = subprocess.CalledProcessError(
            1, 'bandit', stderr="Simulated Bandit error"
        )
        results = run_bandit('valid/path')
        self.assertIn('error', results)
        self.assertEqual(results['error'], 'Bandit scan failed')
        self.assertIn('Simulated Bandit error', results['details'])


if __name__ == '__main__':
    unittest.main()
