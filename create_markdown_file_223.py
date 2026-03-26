#!/usr/bin/env python3
"""
Create a markdown file (test-vwl9jb.md) in the repository root.
This script demonstrates automated file creation, git integration, and conventional commits.
Part of the Sheep project feature 223 implementation.
"""

from pathlib import Path
import subprocess
import sys

# Constants for file creation and git workflow
FILENAME = "test-vwl9jb.md"
TITLE = "The Power of Continuous Learning"
PROSE = "Learning is a lifelong journey that opens doors to new possibilities and perspectives. By embracing growth and curiosity, we develop resilience and adaptability in an ever-changing world. Every experience, challenge, and success contributes to our evolution as individuals."
COMMIT_MESSAGE = "feat(223): Create markdown file test-vwl9jb.md"


def create_file() -> None:
    """
    Create the markdown file with H1 heading and prose content.
    Uses pathlib.Path.write_text() with explicit UTF-8 encoding and Unix LF line endings.
    Raises FileExistsError if file already exists.
    Raises OSError for file I/O failures.
    """
    try:
        # Compose markdown content: H1 heading + blank line + prose
        content = f"# {TITLE}\n\n{PROSE}\n"

        # Create file path object
        file_path = Path(FILENAME)

        # Write file with explicit UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF on all platforms (Windows, macOS, Linux)
        file_path.write_text(content, encoding="utf-8", newline="\n")

        print(f"[OK] Created file: {FILENAME}")
    except FileExistsError as e:
        print(f"[ERROR] File already exists: {e}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"[ERROR] File I/O error: {e}", file=sys.stderr)
        raise


def git_add() -> None:
    """
    Stage the created file in git using 'git add'.
    Raises subprocess.CalledProcessError if the command fails.
    """
    try:
        subprocess.run(["git", "add", FILENAME], check=True)
        print(f"[OK] Staged file in git: {FILENAME}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git add failed: {e.cmd}", file=sys.stderr)
        raise


def git_commit() -> None:
    """
    Create a git commit with the conventional commits message format.
    Raises subprocess.CalledProcessError if the command fails.
    """
    try:
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
        print(f"[OK] Created commit: {COMMIT_MESSAGE}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git commit failed: {e.cmd}", file=sys.stderr)
        raise


def git_push() -> None:
    """
    Push the commit to the remote origin on the feature branch.
    Raises subprocess.CalledProcessError if the command fails.
    """
    try:
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
        print("[OK] Pushed commit to remote")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git push failed: {e.cmd}", file=sys.stderr)
        raise


def main() -> int:
    """
    Orchestrate the complete workflow: create file, stage in git, commit, and push.
    Returns 0 on success, 1 on failure.
    """
    try:
        # Step 1: Create the markdown file
        create_file()

        # Step 2: Stage the file in git
        git_add()

        # Step 3: Create a commit with conventional message
        git_commit()

        # Step 4: Push the commit to remote
        git_push()

        print("\n[OK] Feature 223 implementation complete!")
        return 0
    except (FileExistsError, OSError, subprocess.CalledProcessError):
        print("\n[ERROR] Feature 223 implementation failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
