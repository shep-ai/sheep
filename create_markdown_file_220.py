#!/usr/bin/env python3
"""
Create a markdown file named test-yt6y8d.md with a title and 2 sentences of prose.
Stage it in git, commit with a conventional commit message, and push to the feature branch.
"""

import subprocess
from pathlib import Path


# Constants
FILENAME = "test-yt6y8d.md"
TITLE = "# Innovation and Continuous Progress"
PROSE = "Innovation is the cornerstone of human progress and societal advancement, enabling organizations and individuals to create meaningful change by challenging established norms and discovering entirely new possibilities. Strategic innovation requires a delicate balance between visionary thinking and practical execution, combining bold ideas with disciplined implementation to deliver lasting impact and sustainable growth."
COMMIT_MESSAGE = "feat(220): Create markdown file test-yt6y8d.md"
BRANCH = "feat/markdown-file-creation-ebef0e"


def create_markdown_file():
    """
    Create a markdown file at repository root with H1 heading and prose content.

    File format:
    - Line 1: H1 heading (# [Title])
    - Line 2: Blank line
    - Lines 3+: Prose content (2 sentences)

    Uses UTF-8 encoding without BOM and Unix LF line endings.
    """
    content = f"{TITLE}\n\n{PROSE}\n"
    file_path = Path(FILENAME)
    file_path.write_text(content, encoding="utf-8", newline="\n")


def stage_file():
    """
    Stage the markdown file in git using 'git add'.

    Uses subprocess.run() with shell=False for security and check=True for fail-fast.
    """
    subprocess.run(["git", "add", FILENAME], check=True)


def commit_file():
    """
    Commit the staged file with a conventional commit message.

    Message format: feat(220): Create markdown file test-yt6y8d.md
    """
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)


def push_to_branch():
    """
    Push the commit to the feature branch on remote origin.

    Branch: feat/220-markdown-file-creation-ebef0e
    """
    subprocess.run(["git", "push", "-u", "origin", BRANCH], check=True)


def main():
    """
    Execute the complete workflow: create → stage → commit → push.
    """
    print("Creating markdown file...")
    create_markdown_file()
    print(f"✓ File '{FILENAME}' created")

    print("Staging file in git...")
    stage_file()
    print("✓ File staged")

    print("Committing file...")
    commit_file()
    print("✓ File committed")

    print("Pushing to branch...")
    push_to_branch()
    print("✓ Push successful")

    print("\n✓ Feature 220 implementation complete!")


if __name__ == "__main__":
    main()
