#!/usr/bin/env python3
"""
Git integration for feature 213: Execute git add, commit, and push operations
with secure subprocess execution and fail-fast error handling.
"""

import subprocess
from pathlib import Path


def git_add(filename):
    """
    Stage file with git add.

    Args:
        filename: Name of the file to stage

    Raises:
        subprocess.CalledProcessError: If git add fails
    """
    print(f"Staging file: {filename}")
    subprocess.run(["git", "add", filename], check=True)
    print(f"[OK] File staged: git add {filename}")


def git_commit(message):
    """
    Create git commit with conventional commit message.

    Args:
        message: Commit message following Conventional Commits format

    Raises:
        subprocess.CalledProcessError: If git commit fails
    """
    print(f"Creating commit: {message}")
    subprocess.run(["git", "commit", "-m", message], check=True)
    print(f"[OK] Commit created: {message}")


def git_push():
    """
    Push changes to feature branch.

    Raises:
        subprocess.CalledProcessError: If git push fails
    """
    print("Pushing to feature branch...")
    subprocess.run(["git", "push"], check=True)
    print("[OK] Changes pushed to feature branch")


def verify_file_exists(filename):
    """
    Verify that the file exists before git operations.

    Args:
        filename: Name of the file to verify

    Raises:
        FileNotFoundError: If file does not exist
    """
    filepath = Path(filename)
    if not filepath.exists():
        raise FileNotFoundError(f"File {filename} does not exist")
    print(f"[OK] File exists: {filename}")


def main():
    """Execute git integration workflow: add, commit, and push."""
    filename = "test-lyi2gl.md"
    commit_message = "feat(213): Create markdown file test-lyi2gl.md"

    try:
        # Verify file exists before starting git operations
        print("Verifying file existence...")
        verify_file_exists(filename)

        # Execute git operations sequentially
        print("\nExecuting git workflow...")
        git_add(filename)
        git_commit(commit_message)
        git_push()

        print("\n" + "=" * 60)
        print("[OK] ALL GIT OPERATIONS COMPLETED SUCCESSFULLY")
        print("[OK] File test-lyi2gl.md is committed and pushed")
        return True

    except FileNotFoundError as e:
        print(f"\n[ERROR] FILE ERROR: {e}")
        return False

    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] GIT ERROR: Command failed with exit code {e.returncode}")
        print(f"  Command: {' '.join(e.cmd)}")
        return False

    except Exception as e:
        print(f"\n[ERROR] UNEXPECTED ERROR: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
