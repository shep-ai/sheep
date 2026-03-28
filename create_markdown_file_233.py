#!/usr/bin/env python3
"""
Implementation script for feature 233: markdown-file-creation-9291de
Creates test-p7nwe9.md with proper markdown structure.
Phase 1: File Creation & Git Integration

This script follows the well-established pattern from 200+ existing test files
and features 061-232. It creates a markdown file with H1 heading, blank line,
and 2-3 sentences of prose content. File is UTF-8 encoded with LF line endings.
"""

import subprocess
import sys
from pathlib import Path

# Module-level constants
FILENAME = "test-p7nwe9.md"
TITLE = "The Wonders of Continuous Learning"
PROSE = (
    "Learning is a lifelong journey that shapes how we perceive and interact with the world around us. "
    "By embracing challenges and seeking knowledge across diverse domains, we develop resilience and adaptability in an ever-changing landscape. "
    "The pursuit of understanding, both deep and broad, transforms not just our skills but our perspective on what's possible."
)
COMMIT_MESSAGE = "feat(233): Create markdown file test-p7nwe9.md with prose content"

# File size validation constants
MIN_FILE_SIZE = 300
MAX_FILE_SIZE = 600


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-p7nwe9.md in the current working directory with:
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


def validate_file(file_path):
    """
    Validate file properties after creation.

    Checks that the created file meets specification requirements:
    - File exists after write operation
    - File size is within 300-600 byte range (per spec NFR-1)
    - File is properly encoded in UTF-8 without BOM
    - File uses LF line endings (not CRLF)

    Args:
        file_path: Path object to the created file.

    Raises:
        FileNotFoundError: If file does not exist after write.
        ValueError: If file size is outside 300-600 byte range.
        UnicodeDecodeError: If file is not valid UTF-8.
    """
    # Check file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} was not created")

    # Get file size and validate against spec range
    file_size = file_path.stat().st_size
    if not (MIN_FILE_SIZE <= file_size <= MAX_FILE_SIZE):
        raise ValueError(
            f"File size {file_size} bytes is outside spec range "
            f"{MIN_FILE_SIZE}-{MAX_FILE_SIZE} bytes"
        )

    # Verify UTF-8 encoding (will raise UnicodeDecodeError if invalid)
    content = file_path.read_text(encoding="utf-8")

    # Check for UTF-8 BOM (3 bytes: EF BB BF)
    file_bytes = file_path.read_bytes()
    if file_bytes.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File contains UTF-8 BOM, but spec requires no BOM")

    # Check for CRLF line endings (should be LF only)
    if b'\r\n' in file_bytes:
        raise ValueError("File contains CRLF line endings, but spec requires LF only")

    print(f"✓ Validated {file_path} (size: {file_size} bytes, encoding: UTF-8, line endings: LF)")


def git_add():
    """
    Stage the created markdown file with git add.

    Executes: git add test-p7nwe9.md

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

    Executes: git commit -m "feat(233): Create markdown file test-p7nwe9.md with prose content"

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
    Main orchestration: create file → validate → add → commit → push.

    Executes the full workflow: file creation followed by validation,
    then git integration. Each step depends on the previous one completing successfully.

    Raises:
        FileExistsError: If file already exists.
        OSError: If file creation fails.
        ValueError: If file validation fails.
        subprocess.CalledProcessError: If any git operation fails.
    """
    try:
        print("Starting markdown file creation and git integration...")
        file_path = Path(FILENAME)

        # Phase 1: Create and validate file
        print("\nPhase 1: Creating and validating markdown file...")
        create_file()
        validate_file(file_path)

        # Phase 2: Git operations
        print("\nPhase 2: Git integration...")
        git_add()
        git_commit()
        git_push()

        print("\n✓ Feature 233 implementation complete!")
    except Exception as e:
        print(f"\n✗ Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
