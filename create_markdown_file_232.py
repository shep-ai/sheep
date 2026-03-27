#!/usr/bin/env python3
"""
Implementation script for feature 232: markdown-file-creation-3a8cc2
Creates test-rnfcfc.md with proper markdown structure.
Phase 1: File Creation & Content Composition
No validation layer per spec requirement.
"""

import sys
import subprocess
from pathlib import Path

# Module-level constants
FILENAME = "test-rnfcfc.md"
TITLE = "The Magic of Natural Curiosity"
PROSE = (
    "Curiosity is a fundamental human trait that drives learning, innovation, and personal growth throughout our lives. "
    "When we embrace questions and explore ideas with genuine wonder, we unlock new perspectives and develop deeper understanding of the world around us. "
    "By nurturing this natural instinct to discover and learn, we create pathways to creativity and meaningful progress."
)
COMMIT_MESSAGE = "feat(232): Create markdown file test-rnfcfc.md with prose content"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-rnfcfc.md in the current working directory with:
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
        print(f"✓ Created {file_path}")
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

    Executes: git add test-rnfcfc.md

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
        print(f"✓ Staged {FILENAME} with git add")
    except subprocess.CalledProcessError as e:
        print(
            f"Error executing git add: {e}\nstderr: {e.stderr}",
            file=sys.stderr,
        )
        raise


def git_commit():
    """
    Commit the staged file with conventional commit message.

    Executes: git commit -m "feat(232): Create markdown file test-rnfcfc.md with prose content"

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
        print(f"✓ Committed with message: {COMMIT_MESSAGE}")
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
        print("✓ Pushed commit to remote branch")
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
        print("\n✓ Feature 232 implementation complete!")
    except Exception as e:
        print(f"\n✗ Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
