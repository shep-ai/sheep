#!/usr/bin/env python3
"""Git integration for markdown file creation feature 262 (Phase 2)."""

import subprocess
from pathlib import Path


def stage_file(filename="test-mylh5m.md"):
    """Stage file with git add.

    Args:
        filename: Name of file to stage (default: test-mylh5m.md)

    Returns:
        bool: True if staging succeeded

    Raises:
        subprocess.CalledProcessError: If git add command fails
    """
    try:
        subprocess.run(['git', 'add', filename], check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to stage {filename}: {e.stderr}") from e


def is_file_staged(filename="test-mylh5m.md"):
    """Check if file is staged for commit.

    Args:
        filename: Name of file to check (default: test-mylh5m.md)

    Returns:
        bool: True if file is staged
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            check=True,
            capture_output=True,
            text=True
        )
        # Staged files start with 'A ' or 'M ' in porcelain output
        for line in result.stdout.split('\n'):
            if filename in line and line.startswith(('A ', 'M ')):
                return True
        return False
    except subprocess.CalledProcessError:
        return False


def commit_file(message="feat(262): Create markdown file test-mylh5m.md with prose content"):
    """Commit staged changes with conventional commit message.

    Args:
        message: Commit message (default: conventional format for feature 262)

    Returns:
        bool: True if commit succeeded

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
        return True
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to commit: {e.stderr}") from e


def is_commit_in_log(message="feat(262): Create markdown file test-mylh5m.md with prose content"):
    """Check if commit with given message is in git log.

    Args:
        message: Commit message to search for

    Returns:
        bool: True if commit message found in log
    """
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline'],
            check=True,
            capture_output=True,
            text=True
        )
        return message in result.stdout
    except subprocess.CalledProcessError:
        return False


def push_to_branch(branch="feat/markdown-file-creation-03c688", remote="origin"):
    """Push commits to feature branch.

    Args:
        branch: Branch name to push to (default: feat/262-markdown-file-creation-03c688)
        remote: Remote name (default: origin)

    Returns:
        bool: True if push succeeded

    Raises:
        subprocess.CalledProcessError: If git push command fails
    """
    try:
        subprocess.run(
            ['git', 'push', remote, branch],
            check=True,
            capture_output=True,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        # Extract meaningful error message
        error_msg = e.stderr or e.stdout or "Unknown error"
        raise RuntimeError(f"Failed to push to {remote}/{branch}: {error_msg}") from e


def get_current_branch():
    """Get the current branch name.

    Returns:
        str: Current branch name
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def verify_git_config():
    """Verify git is configured with user.name and user.email.

    Returns:
        dict: Configuration status with 'user_name' and 'user_email' keys
    """
    config = {'user_name': None, 'user_email': None}

    try:
        result = subprocess.run(
            ['git', 'config', 'user.name'],
            check=True,
            capture_output=True,
            text=True
        )
        config['user_name'] = result.stdout.strip()
    except subprocess.CalledProcessError:
        pass

    try:
        result = subprocess.run(
            ['git', 'config', 'user.email'],
            check=True,
            capture_output=True,
            text=True
        )
        config['user_email'] = result.stdout.strip()
    except subprocess.CalledProcessError:
        pass

    return config


if __name__ == "__main__":
    print("Git Integration for Feature 262")
    print("=" * 50)

    # Verify git config
    print("\n[1] Verifying git configuration...")
    config = verify_git_config()
    if config['user_name'] and config['user_email']:
        print(f"  [OK] Git configured: {config['user_name']} <{config['user_email']}>")
    else:
        print("  [FAIL] Git not fully configured")

    # Check current branch
    print("\n[2] Checking current branch...")
    branch = get_current_branch()
    if branch == "feat/262-markdown-file-creation-03c688":
        print(f"  [OK] On correct branch: {branch}")
    else:
        print(f"  [INFO] Current branch: {branch}")

    # Stage file
    print("\n[3] Staging test-mylh5m.md...")
    try:
        stage_file()
        if is_file_staged():
            print("  [OK] File staged successfully")
        else:
            print("  [FAIL] File not staged")
    except RuntimeError as e:
        print(f"  [FAIL] {e}")

    # Commit file
    print("\n[4] Committing with conventional message...")
    try:
        commit_file()
        message = "feat(262): Create markdown file test-mylh5m.md with prose content"
        if is_commit_in_log(message):
            print("  [OK] Commit created successfully")
        else:
            print("  [FAIL] Commit not found in log")
    except RuntimeError as e:
        print(f"  [FAIL] {e}")

    # Push to remote
    print("\n[5] Pushing to feature branch...")
    try:
        push_to_branch()
        print("  [OK] Push successful")
    except RuntimeError as e:
        print(f"  [FAIL] {e}")

    print("\n" + "=" * 50)
    print("Git integration complete!")
