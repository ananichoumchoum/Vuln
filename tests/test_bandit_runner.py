import subprocess
from unittest.mock import patch
from vuln.core.bandit_runner import run_bandit
import unittest

class TestBanditRunner(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_bandit_with_valid_path(self, mock_subprocess, mock_exists):
        # Mock subprocess to return a valid JSON output
        mock_subprocess.return_value.stdout = '{"results": []}'
        mock_subprocess.return_value.returncode = 0
        
        results = run_bandit('valid/path')
        self.assertIsInstance(results, dict)
        self.assertIn('results', results)

    @patch('os.path.exists', return_value=False)
    @patch('subprocess.run')
    def test_bandit_with_invalid_path(self, mock_subprocess, mock_exists):
        # Mock subprocess to raise a FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            run_bandit('invalid/path')

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    def test_bandit_fails(self, mock_subprocess, mock_exists):
        # Simulate a subprocess failure with stderr
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'bandit', stderr="Simulated Bandit error")
        
        results = run_bandit('valid/path')
        self.assertIn('error', results)
        self.assertEqual(results['error'], 'Bandit scan failed')
        self.assertIn('Simulated Bandit error', results['details'])

if __name__ == '__main__':
    unittest.main()
