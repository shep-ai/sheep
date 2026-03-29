#!/usr/bin/env python3
"""
Implementation script for feature 269: markdown-file-creation-6cc7be
Creates test-uh2jl0.md with proper markdown structure.
Phase 1: File Creation & Git Integration
"""

import subprocess
import sys
from pathlib import Path

# Module-level constants
FILENAME = "test-uh2jl0.md"
TITLE = "Feature 269: Markdown File Creation Test"
PROSE = (
    "This file is part of feature 269 in the Sheep automation platform's markdown file creation test series. "
    "The feature demonstrates the platform's ability to generate well-formed markdown files with proper structure, "
    "encoding, and git integration. By creating this self-documenting test file, we validate the core file creation "
    "and version control workflow that forms the foundation of the Sheep platform's automation capabilities."
)
COMMIT_MESSAGE = "feat(269): create markdown file test-uh2jl0.md with prose content"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-uh2jl0.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created file if successful.

    Raises:
        FileExistsError: If file already exists (defensive check).
        OSError: If file creation fails.
    """
    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Create file path
    file_path = Path(FILENAME)

    # Check file doesn't already exist (defensive check)
    if file_path.exists():
        raise FileExistsError(f"File {file_path} already exists")

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"[OK] Created {file_path}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        raise


def git_add():
    """
    Stage the created markdown file with git add.

    Executes: git add test-uh2jl0.md

    Raises:
        subprocess.CalledProcessError: If git add fails (file not found, git error, etc).
    """
    try:
        subprocess.run(
            ["git", "add", FILENAME],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"[OK] Staged {FILENAME} with git add")
    except subprocess.CalledProcessError as e:
        print(
            f"Error executing git add: {e}\nstderr: {e.stderr}",
            file=sys.stderr,
        )
        raise


def git_commit():
    """
    Commit the staged file with conventional commit message.

    Executes: git commit -m "feat(269): create markdown file test-uh2jl0.md with prose content"

    Raises:
        subprocess.CalledProcessError: If git commit fails.
    """
    try:
        subprocess.run(
            ["git", "commit", "-m", COMMIT_MESSAGE],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"[OK] Committed with message: {COMMIT_MESSAGE}")
    except subprocess.CalledProcessError as e:
        print(
            f"Error executing git commit: {e}\nstderr: {e.stderr}",
            file=sys.stderr,
        )
        raise


def git_push():
    """
    Push the commit to the feature branch with upstream tracking.

    Executes: git push -u origin HEAD

    Raises:
        subprocess.CalledProcessError: If git push fails.
    """
    try:
        subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        print("[OK] Pushed commit to remote branch")
    except subprocess.CalledProcessError as e:
        print(
            f"Error executing git push: {e}\nstderr: {e.stderr}",
            file=sys.stderr,
        )
        raise


def main():
    """
    Main orchestration: create file → add → commit → push.

    Executes the full workflow: file creation followed by git integration.
    Each step depends on the previous one completing successfully.

    Raises:
        FileExistsError: If file already exists.
        OSError: If file creation fails.
        subprocess.CalledProcessError: If any git operation fails.
    """
    try:
        print("Starting markdown file creation and git integration...")
        create_file()
        git_add()
        git_commit()
        git_push()
        print("\n[OK] Feature 269 implementation complete!")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
