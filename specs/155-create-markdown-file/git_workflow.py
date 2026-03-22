"""Git workflow functions for markdown file creation."""

import subprocess
import sys
from pathlib import Path
from typing import Optional


# Constants for git workflow
FILENAME = "test-0h4oez.md"
COMMIT_MESSAGE = "feat(155): create markdown file test-0h4oez.md with prose content"
FEATURE_BRANCH = "feat/create-markdown-file"
REMOTE_NAME = "origin"


def git_add(filepath: str = FILENAME) -> bool:
    """
    Stage a file in git using 'git add'.

    Args:
        filepath: Name of the file to stage (defaults to test-0h4oez.md)

    Returns:
        True if successful

    Raises:
        subprocess.CalledProcessError: If git add command fails
    """
    try:
        subprocess.run(
            ['git', 'add', filepath],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Staged file in git: {filepath}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Git add failed: {e.stderr}", file=sys.stderr)
        raise


def git_commit(message: str = COMMIT_MESSAGE) -> bool:
    """
    Commit staged changes with a conventional commit message.

    Args:
        message: Commit message following conventional commits format

    Returns:
        True if successful

    Raises:
        subprocess.CalledProcessError: If git commit command fails
    """
    try:
        subprocess.run(
            ['git', 'commit', '-m', message],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Committed with message: {message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Git commit failed: {e.stderr}", file=sys.stderr)
        raise


def git_push(
    remote: str = REMOTE_NAME,
    branch: str = FEATURE_BRANCH
) -> bool:
    """
    Push commits to remote repository.

    Args:
        remote: Remote repository name (defaults to 'origin')
        branch: Branch name to push (defaults to feature branch)

    Returns:
        True if successful

    Raises:
        subprocess.CalledProcessError: If git push command fails
    """
    try:
        subprocess.run(
            ['git', 'push', '-u', remote, branch],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Pushed to remote: {remote}/{branch}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Git push failed: {e.stderr}", file=sys.stderr)
        raise


def get_current_branch() -> str:
    """
    Get the currently checked out branch name.

    Returns:
        Current branch name

    Raises:
        subprocess.CalledProcessError: If git command fails
    """
    result = subprocess.run(
        ['git', 'branch', '--show-current'],
        check=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def get_commit_message(commit_ref: str = "HEAD") -> str:
    """
    Get the commit message for a given commit reference.

    Args:
        commit_ref: Git reference (defaults to HEAD)

    Returns:
        Commit message

    Raises:
        subprocess.CalledProcessError: If git command fails
    """
    result = subprocess.run(
        ['git', 'log', '-1', '--pretty=%B', commit_ref],
        check=True,
        capture_output=True,
        text=True
    )
    return result.stdout.strip()


def is_file_tracked(filepath: str) -> bool:
    """
    Check if a file is tracked by git.

    Args:
        filepath: Path to the file to check (relative to git root)

    Returns:
        True if file is tracked by git
    """
    result = subprocess.run(
        ['git', 'ls-files', '--', filepath],
        capture_output=True,
        text=True,
        cwd=subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True
        ).stdout.strip()
    )
    return bool(result.stdout.strip())


def verify_branch_match(expected_branch: str) -> bool:
    """
    Verify that the current branch matches the expected branch.

    Args:
        expected_branch: Expected branch name

    Returns:
        True if current branch matches expected branch

    Raises:
        ValueError: If branch names don't match
    """
    current = get_current_branch()
    if current != expected_branch:
        raise ValueError(
            f"Branch mismatch: current branch is '{current}', "
            f"expected '{expected_branch}'"
        )
    return True
