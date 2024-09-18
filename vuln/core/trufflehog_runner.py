"""
This module contains functions to run trufflehog on a given file or directory
and return the scan output along with any errors encountered.
"""
import subprocess
import logging
import os
import git
from git.exc import InvalidGitRepositoryError, GitCommandError

# Initialize logger
logger = logging.getLogger(__name__)


def is_git_repo(scan_path):
    """
    Checks if the specified path is a valid Git repository.

    Args:
        scan_path (str): The directory path to check.

    Returns:
        bool: True if the path is a Git repository, False otherwise.
    """
    try:
        _ = git.Repo(scan_path).git_dir
        return True
    except InvalidGitRepositoryError:
        return False


def has_remote_origin(scan_path):
    """
    Checks if the Git repository has a remote 'origin' set.

    Args:
        scan_path (str): The directory path to check.

    Returns:
        bool: True if the remote origin is set, False otherwise.
    """
    try:
        repo = git.Repo(scan_path)
        return "origin" in repo.remotes
    except GitCommandError as e:
        logger.error("Error checking for remote origin: %s\n", e)
        return False


def run_trufflehog(scan_path):
    """
    Runs TruffleHog on the specified scan_path and returns the output.

    Args:
        scan_path (str): The file or directory path to scan with TruffleHog.

    Returns:
        dict: A dictionary containing the output of the scan.
    """
    print("Tool: TruffleHog")

    # Check if the directory is a valid Git repository
    if not is_git_repo(scan_path):
        error_msg = f"{scan_path} is not a valid Git repository.\n"
        logger.error(error_msg)
        return {"error": error_msg}

    # Check if the repository has a valid Git history
    if not os.path.exists(os.path.join(scan_path, '.git')):
        error_msg = f"{scan_path} does not contain a valid Git history.\n"
        logger.error(error_msg)
        return {"error": error_msg}

    # Check if the repository has a remote origin set
    if not has_remote_origin(scan_path):
        error_msg = f"{scan_path} does not have a remote 'origin' set.\n"
        logger.error(error_msg)
        return {"error": error_msg}

    try:
        # Command to run TruffleHog
        trufflehog_cmd = ['trufflehog', 'git', '--repo_path', scan_path]
        process = subprocess.run(
            trufflehog_cmd, capture_output=True, text=True, check=False)

        # Check if any secrets were found
        if process.returncode == 0:
            logger.info("TruffleHog scan completed with no issues.\n")
        else:
            logger.warning("TruffleHog found potential secrets.\n")

        return {"output": process.stdout,
                "error": process.stderr if process.returncode != 0 else None}

    except subprocess.CalledProcessError as e:
        error_msg = f"TruffleHog execution failed: {e}\n"
        logger.error(error_msg)
        return {"error": error_msg}
