"""
Git workflow module for feature 278: markdown file creation.

This module provides functions to execute git operations (add, commit, push)
for the created markdown file.

Operations:
- Stage file with 'git add'
- Commit with conventional commit message
- Push to feature branch
"""

import subprocess

# ============================================================================
# Constants
# ============================================================================

FILENAME = "test-6ektaf.md"
FEATURE_NUMBER = "278"
COMMIT_MESSAGE = "feat(278): create markdown file test-6ektaf.md with title and prose content"
FEATURE_BRANCH = "feat/278-markdown-file-creation-dae11e"


# ============================================================================
# Exception Class
# ============================================================================


class GitWorkflowError(Exception):
    """
    Custom exception for git workflow errors.

    Provides detailed error messages for git operation failures.
    """
    pass


# ============================================================================
# Git Workflow Class
# ============================================================================


class GitWorkflow:
    """
    Orchestrates git operations for markdown file creation feature.

    Provides methods to:
    - Add file to staging area
    - Commit changes with conventional message
    - Push to feature branch
    """

    def __init__(self, filename=FILENAME, branch=FEATURE_BRANCH, message=COMMIT_MESSAGE):
        """
        Initialize GitWorkflow with configuration.

        Args:
            filename (str): Name of file to add (default: test-6ektaf.md)
            branch (str): Feature branch name (default: feat/278-markdown-file-creation-dae11e)
            message (str): Commit message (default: conventional format)
        """
        self.filename = filename
        self.branch = branch
        self.message = message

    def add_file(self):
        """
        Stage file in git using 'git add' command.

        Returns:
            bool: True if add succeeds

        Raises:
            GitWorkflowError: If git add fails with descriptive error message
        """
        try:
            result = subprocess.run(
                ["git", "add", self.filename],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise GitWorkflowError(
                    f"git add failed with return code {result.returncode}: {result.stderr}"
                )
            return True
        except Exception as e:
            raise GitWorkflowError(f"Failed to add file: {e}") from e

    def commit_changes(self):
        """
        Commit staged changes with conventional commit message.

        Returns:
            bool: True if commit succeeds

        Raises:
            GitWorkflowError: If git commit fails with descriptive error message
        """
        try:
            result = subprocess.run(
                ["git", "commit", "-m", self.message],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise GitWorkflowError(
                    f"git commit failed with return code {result.returncode}: {result.stderr}"
                )
            return True
        except Exception as e:
            raise GitWorkflowError(f"Failed to commit changes: {e}") from e

    def push_to_branch(self):
        """
        Push committed changes to feature branch.

        Returns:
            bool: True if push succeeds

        Raises:
            GitWorkflowError: If git push fails with descriptive error message
        """
        try:
            result = subprocess.run(
                ["git", "push", "origin", self.branch],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise GitWorkflowError(
                    f"git push failed with return code {result.returncode}: {result.stderr}"
                )
            return True
        except Exception as e:
            raise GitWorkflowError(f"Failed to push to branch: {e}") from e

    def execute_workflow(self):
        """
        Execute complete git workflow: add, commit, push.

        Returns:
            bool: True if all operations succeed

        Raises:
            GitWorkflowError: If any operation fails
        """
        self.add_file()
        self.commit_changes()
        self.push_to_branch()
        return True
