import unittest
from unittest.mock import patch
from vuln.core.bandit_runner import run_bandit

class TestBanditRunner(unittest.TestCase):
    
    @patch('subprocess.run')
    def test_bandit_with_valid_path(self, mock_subprocess):
        # Mock subprocess to return a valid JSON output
        mock_subprocess.return_value.stdout = '{"results": []}'
        mock_subprocess.return_value.returncode = 0
        
        results = run_bandit('valid/path')
        self.assertIsInstance(results, dict)
        self.assertIn('results', results)

    @patch('subprocess.run')
    def test_bandit_with_invalid_path(self, mock_subprocess):
        # Mock subprocess to raise a FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            run_bandit('invalid/path')

    @patch('subprocess.run')
    def test_bandit_fails(self, mock_subprocess):
        # Simulate a subprocess failure
        mock_subprocess.side_effect = subprocess.CalledProcessError(1, 'bandit')
        
        results = run_bandit('valid/path')
        self.assertIn('error', results)
        self.assertEqual(results['error'], 'Bandit scan failed')

if __name__ == '__main__':
    unittest.main()
