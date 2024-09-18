"""
Unit tests for the Trugglehog runner module.
"""
import unittest
from unittest.mock import patch, MagicMock
import subprocess
import logging
import git
from vuln.core.trufflehog_runner import is_git_repo, has_remote_origin, run_trufflehog

# Initialize logger
logger = logging.getLogger(__name__)


class TestTruffleHogRunner(unittest.TestCase):
    """Tests for the Safety runner methods."""

    @patch('git.Repo')
    def test_is_git_repo_valid(self, mock_repo):
        """Test if the given path is a valid Git repository."""
        # Mock a valid Git repository
        mock_repo.return_value.git_dir = '/some/path/.git'

        scan_path = '/some/path'
        self.assertTrue(is_git_repo(scan_path))

    @patch('git.Repo')
    def test_is_git_repo_invalid(self, mock_repo):
        """Test when the given path is not a Git repository."""
        mock_repo.side_effect = git.exc.InvalidGitRepositoryError
        scan_path = '/invalid/path'
        self.assertFalse(is_git_repo(scan_path))

    @patch('git.Repo')
    def test_has_remote_origin_valid(self, mock_repo):
        """Test if the repository has a remote origin."""
        mock_remote = MagicMock()
        mock_remote.remotes = ['origin']
        mock_repo.return_value = mock_remote

        scan_path = '/valid/repo'
        self.assertTrue(has_remote_origin(scan_path))

    @patch('git.Repo')
    def test_has_remote_origin_invalid(self, mock_repo):
        """Test when the repository does not have a remote origin."""
        mock_repo.return_value.remotes = []
        scan_path = '/valid/repo/no-origin'
        self.assertFalse(has_remote_origin(scan_path))

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    @patch('vuln.core.trufflehog_runner.is_git_repo', return_value=True)
    @patch('vuln.core.trufflehog_runner.has_remote_origin', return_value=True)
    def test_run_trufflehog_success(
        self,
        mock_is_git_repo,
        mock_has_remote_origin,
        mock_subprocess,
        mock_path_exists
    ):
        """Test successful run of TruffleHog."""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = 'No secrets found.'
        mock_subprocess.return_value = mock_process

        scan_path = '/valid/repo'
        result = run_trufflehog(scan_path)

        self.assertIn("output", result)
        self.assertIsNone(result["error"])
        self.assertEqual(result["output"], 'No secrets found.')

    @patch('os.path.exists', return_value=True)
    @patch('subprocess.run')
    @patch('vuln.core.trufflehog_runner.is_git_repo', return_value=True)
    @patch('vuln.core.trufflehog_runner.has_remote_origin', return_value=False)
    def test_run_trufflehog_no_remote_origin(
        self,
        mock_is_git_repo,
        mock_has_remote_origin,
        mock_subprocess,
        mock_path_exists
    ):
        """Test when the repository has no remote origin."""
        scan_path = '/repo/no-origin'
        result = run_trufflehog(scan_path)

        self.assertIn("error", result)
        self.assertEqual(result["error"],
                         f"{scan_path} does not have a remote 'origin' set.\n")

    @patch('os.path.exists', return_value=False)
    @patch('vuln.core.trufflehog_runner.is_git_repo', return_value=True)
    @patch('vuln.core.trufflehog_runner.has_remote_origin', return_value=True)
    def test_run_trufflehog_invalid_git_history(
        self,
        mock_is_git_repo,
        mock_has_remote_origin,
        mock_path_exists
    ):
        """Test when the repository does not have a valid Git history."""
        scan_path = '/repo/no-git-history'
        result = run_trufflehog(scan_path)

        self.assertIn("error", result)
        self.assertEqual(result["error"],
                         f"{scan_path} does not contain valid Git history.\n")

    @patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'trufflehog'))
    @patch('os.path.exists', return_value=True)
    @patch('vuln.core.trufflehog_runner.is_git_repo', return_value=True)
    @patch('vuln.core.trufflehog_runner.has_remote_origin', return_value=True)
    def test_run_trufflehog_execution_failure(
        self,
        mock_is_git_repo,
        mock_has_remote_origin,
        mock_subprocess,
        mock_path_exists
    ):
        """Test when TruffleHog execution fails."""
        scan_path = '/valid/repo'
        result = run_trufflehog(scan_path)

        self.assertIn("error", result)
        self.assertTrue("TruffleHog execution failed" in result["error"])


if __name__ == '__main__':
    unittest.main()
