#!/usr/bin/env python3
"""
Create markdown file test-70rjoj.md following the established pattern.

This script implements the markdown-file-creation feature (243) by:
1. Creating test-70rjoj.md with hardcoded prose content (H1 heading + 2-3 sentences)
2. Validating file format (UTF-8 encoding, LF line endings, correct structure)
3. Staging the file with git add
4. Committing with conventional commit message
5. Pushing to the feature branch

The implementation follows the pattern established by 240+ similar test files
in the repository and uses only Python standard library (pathlib, subprocess).
"""

from pathlib import Path
import subprocess
import sys


# Markdown content: H1 heading + blank line + 2-3 sentences about a meaningful topic
# Topic: The importance of resilience in overcoming life's challenges
# When encoded as UTF-8, this content is approximately 400-600 bytes
MARKDOWN_CONTENT = """# The Art of Resilience

Resilience is the quiet strength that emerges when we face adversity and choose to persist despite obstacles. It is not about avoiding challenges, but rather developing the capacity to adapt, learn, and grow through difficult experiences. This quality, cultivated through patience and self-reflection, becomes the foundation upon which we build meaningful and fulfilling lives."""

MARKDOWN_FILE = "test-70rjoj.md"
COMMIT_MESSAGE = "feat(243): create markdown file test-70rjoj.md with prose content"
BRANCH_NAME = "feat/markdown-file-creation-967ad1"


def create_markdown_file():
    """
    Create the markdown file in repository root using pathlib.

    Writes MARKDOWN_CONTENT to test-70rjoj.md with UTF-8 encoding and LF line endings.
    The newline='' parameter ensures LF (\\n) on all platforms, including Windows.

    Raises:
        IOError: If file creation fails (permissions, disk space, etc.)
    """
    markdown_path = Path(MARKDOWN_FILE)
    # Use encoding='utf-8' to ensure UTF-8 without BOM
    # Use newline='' to preserve explicit \\n and prevent CRLF conversion on Windows
    markdown_path.write_text(MARKDOWN_CONTENT, encoding='utf-8', newline='')


def validate_file():
    """
    Validate the created markdown file against all requirements.

    Checks:
    - File exists at repository root
    - File size is 400-600 bytes
    - File is readable as UTF-8 (no encoding errors)
    - File uses LF line endings (no CRLF)
    - Markdown structure is correct (one heading, blank line, 2-3 sentences)

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If any validation check fails
    """
    markdown_path = Path(MARKDOWN_FILE)

    # Check file exists
    if not markdown_path.exists():
        raise FileNotFoundError(f"File {MARKDOWN_FILE} was not created")

    # Check file size is in expected range
    file_size = markdown_path.stat().st_size
    if file_size < 400 or file_size > 600:
        raise ValueError(
            f"File size {file_size} bytes is outside expected range (400-600 bytes)"
        )

    # Read file content and verify UTF-8 encoding
    try:
        content = markdown_path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    # Verify no CRLF line endings (should be LF only)
    if '\r\n' in content:
        raise ValueError("File contains CRLF line endings (Windows style); must use LF")

    # Verify markdown structure: one heading, blank line, sentences
    lines = content.split('\n')

    # Check for exactly one H1 heading (line starting with #)
    heading_count = sum(1 for line in lines if line.startswith('# '))
    if heading_count != 1:
        raise ValueError(
            f"Expected exactly 1 H1 heading, found {heading_count}"
        )

    # Check for blank line after heading (second line should be blank)
    if len(lines) < 3 or lines[1] != '':
        raise ValueError("Expected blank line after heading")

    # Count sentences (roughly) by counting sentence-ending punctuation
    prose_text = '\n'.join(lines[2:])
    sentence_count = sum(1 for char in prose_text if char in '.!?')
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"Expected 2-3 sentences, found approximately {sentence_count}"
        )


def stage_file():
    """
    Stage the markdown file in git using 'git add'.

    Raises:
        RuntimeError: If git add fails
    """
    try:
        result = subprocess.run(
            ['git', 'add', MARKDOWN_FILE],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to stage file with git add: {e.stderr or e.stdout}"
        )


def commit_file():
    """
    Commit the staged file with conventional commit message.

    Uses exact message: "feat(243): create markdown file test-70rjoj.md with prose content"

    Raises:
        RuntimeError: If git commit fails
    """
    try:
        result = subprocess.run(
            ['git', 'commit', '-m', COMMIT_MESSAGE],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to commit file: {e.stderr or e.stdout}"
        )


def push_commit():
    """
    Push the commit to the feature branch.

    Pushes to: origin/feat/243-markdown-file-creation-967ad1

    Raises:
        RuntimeError: If git push fails
    """
    try:
        result = subprocess.run(
            ['git', 'push', 'origin', BRANCH_NAME],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to push commit: {e.stderr or e.stdout}"
        )


def main():
    """
    Main entry point for markdown file creation.

    Returns:
        int: Exit code (0 on success, 1 on any error)
    """
    try:
        print("Feature 243: Markdown file creation starting...")
        create_markdown_file()
        print(f"Created {MARKDOWN_FILE}")
        validate_file()
        print(f"Validated {MARKDOWN_FILE}")

        # Git integration: stage, commit, push
        stage_file()
        print(f"Staged {MARKDOWN_FILE} with git add")

        commit_file()
        print(f"Committed with message: {COMMIT_MESSAGE}")

        push_commit()
        print(f"Pushed to {BRANCH_NAME}")

        print("Feature 243: Markdown file creation completed successfully!")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
