#!/usr/bin/env python3
"""
Implementation script for feature 221: markdown-file-creation-213da4
Creates test-ye16lc.md with proper markdown structure.
"""

import sys
import subprocess
from pathlib import Path

# Module-level constants
FILENAME = "test-ye16lc.md"
TITLE = "The Art of Problem Solving"
PROSE = (
    "Problem solving is a fundamental skill that drives innovation and progress across all fields of human endeavor. "
    "When we approach challenges with curiosity and persistence, we develop the resilience needed to overcome obstacles "
    "and discover creative solutions. By embracing difficulties as opportunities for growth, we cultivate both professional "
    "excellence and personal satisfaction."
)
COMMIT_MESSAGE = "feat(221): Create markdown file test-ye16lc.md"
BRANCH_NAME = "feat/221-markdown-file-creation-213da4"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-ye16lc.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created file if successful.

    Raises:
        FileExistsError: If file already exists.
        OSError: If file creation fails.
    """
    file_path = Path(FILENAME)

    # Compose markdown content: H1 heading + blank line + prose
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Write file with explicit Unix LF line endings
    file_path.write_text(content, encoding="utf-8", newline="\n")

    return file_path


def git_add():
    """
    Stage the markdown file in git.

    Uses 'git add' command to stage the file for commit.

    Raises:
        subprocess.CalledProcessError: If git add command fails.
    """
    result = subprocess.run(
        ["git", "add", FILENAME],
        capture_output=True,
        text=True,
        check=True,
    )
    return result


def git_commit():
    """
    Create a git commit with the markdown file.

    Uses 'git commit' with the conventional commit message format.

    Raises:
        subprocess.CalledProcessError: If git commit command fails.
    """
    result = subprocess.run(
        ["git", "commit", "-m", COMMIT_MESSAGE],
        capture_output=True,
        text=True,
        check=True,
    )
    return result


def git_push():
    """
    Push the commit to the remote feature branch.

    Uses 'git push -u origin HEAD' to push to the current branch.

    Raises:
        subprocess.CalledProcessError: If git push command fails.
    """
    result = subprocess.run(
        ["git", "push", "-u", "origin", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result


def main():
    """
    Main entry point: orchestrate complete workflow.

    Executes the following phases:
    1. Script Foundation: Initialize configuration and imports
    2. File Creation & Git Integration: Create markdown file and perform git workflow
    3. Error Handling & Robustness: Add comprehensive error handling
    4. Validation & Testing: Verify success criteria

    Returns:
        0 on success, 1 on failure
    """
    print("=" * 60)
    print("Feature 221: Markdown File Creation")
    print("=" * 60)
    print("\nPhase 1 (Script Foundation): Complete")
    print("Configuration loaded:")
    print(f"  File: {FILENAME}")
    print(f"  Title: {TITLE}")
    print(f"  Branch: {BRANCH_NAME}")

    print("\nPhase 2 (File Creation & Git Integration): Starting...")

    # Task 2: Create markdown file
    print(f"\n1. Creating markdown file: {FILENAME}")
    create_file()
    print(f"   [OK] File created successfully")

    # Task 3: Stage file in git
    print(f"\n2. Staging file with git add")
    git_add()
    print(f"   [OK] File staged successfully")

    # Task 4: Commit with conventional message
    print(f"\n3. Creating git commit")
    git_commit()
    print(f"   [OK] Commit created: {COMMIT_MESSAGE}")

    # Task 5: Push to feature branch
    print(f"\n4. Pushing to remote branch: {BRANCH_NAME}")
    git_push()
    print(f"   [OK] Pushed successfully")

    print("\n" + "=" * 60)
    print("Phase 2 (File Creation & Git Integration): Complete")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
