#!/usr/bin/env python3
"""
Implementation script for feature 234: markdown-file-creation-42fd65
Creates test-y7gbjb.md with proper markdown structure.
Phase 1: File Creation & Validation

This script follows the well-established pattern from 230+ existing test files
and features 061-233. It creates a markdown file with H1 heading, blank line,
and 2-3 sentences of prose content. File is UTF-8 encoded with LF line endings.
"""

import sys
import subprocess
import re
from pathlib import Path

# Module-level constants
FILENAME = "test-y7gbjb.md"
TITLE = "Automated File Creation with Python"
PROSE = (
    "This document demonstrates the capabilities of automated markdown file generation using Python. "
    "The process validates encoding standards and integrates with version control systems. "
    "File creation automation improves efficiency and consistency across large-scale projects."
)
COMMIT_MESSAGE = "feat(234): Create markdown file test-y7gbjb.md with prose content"

# File size validation constants
MIN_FILE_SIZE = 200
MAX_FILE_SIZE = 1000


def validate_encoding(file_path):
    """
    Validate file encoding: UTF-8 without BOM, Unix LF line endings.

    Checks that the file was created with:
    - UTF-8 encoding (no BOM signature)
    - Unix LF line endings (no Windows CRLF)

    Args:
        file_path: Path object to the created file.

    Raises:
        ValueError: If encoding or line endings are invalid.
    """
    file_bytes = file_path.read_bytes()

    # Check for UTF-8 BOM (3 bytes: EF BB BF)
    if file_bytes.startswith(b'\xef\xbb\xbf'):
        raise ValueError("File contains UTF-8 BOM, but spec requires no BOM")

    # Check for CRLF line endings (should be LF only)
    if b'\r\n' in file_bytes:
        raise ValueError("File contains CRLF line endings, but spec requires LF only")


def validate_prose(prose_text):
    """
    Validate prose content has minimum 2 sentences.

    Uses flexible minimum validation: counts sentence-ending punctuation
    and ensures at least 2 sentences. Avoids brittle exact counts that
    struggle with abbreviations and complex punctuation.

    Args:
        prose_text: The prose content string.

    Returns:
        int: Number of sentences found.

    Raises:
        ValueError: If prose has fewer than 2 sentences.
    """
    # Count sentences via regex split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+', prose_text.strip())
    sentence_count = len([s for s in sentences if s.strip()])

    if sentence_count < 2:
        raise ValueError(
            f"Prose must contain at least 2 sentences, found {sentence_count}"
        )

    return sentence_count


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-y7gbjb.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2+ sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created file if successful.

    Raises:
        OSError: If file creation fails.
    """
    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Create file path
    file_path = Path(FILENAME)

    # Log if file is being overwritten (idempotency support)
    if file_path.exists():
        print(f"[WARN] File {file_path} already exists, overwriting...")

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


def validate_file(file_path):
    """
    Validate file properties after creation.

    Checks that the created file meets specification requirements:
    - File exists after write operation
    - File size is within 200-1000 byte range
    - File is properly encoded in UTF-8 without BOM
    - File uses LF line endings (not CRLF)
    - Prose contains at least 2 sentences

    Args:
        file_path: Path object to the created file.

    Raises:
        FileNotFoundError: If file does not exist after write.
        ValueError: If file size or content validation fails.
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

    # Validate encoding (UTF-8, no BOM, LF line endings)
    validate_encoding(file_path)

    # Read text content for prose validation
    content = file_path.read_text(encoding="utf-8")

    # Verify UTF-8 can be decoded (will raise UnicodeDecodeError if invalid)
    # This is redundant with validate_encoding but provides extra safety
    try:
        _ = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    # Extract and validate prose content
    if '\n\n' not in content:
        raise ValueError("File should have blank line separating heading from prose")

    parts = content.split('\n\n', 1)
    heading = parts[0].strip()
    prose = parts[1].strip() if len(parts) > 1 else ""

    if not heading.startswith('# '):
        raise ValueError("File should start with H1 heading (# Title)")

    if not prose:
        raise ValueError("Prose content is missing")

    # Validate prose has at least 2 sentences
    sentence_count = validate_prose(prose)

    print(
        f"[OK] Validated {file_path} "
        f"(size: {file_size} bytes, encoding: UTF-8, line endings: LF, "
        f"sentences: {sentence_count})"
    )


def git_add():
    """
    Stage the created markdown file with git add.

    Executes: git add test-y7gbjb.md

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

    Executes: git commit -m "feat(234): Create markdown file test-y7gbjb.md with prose content"

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
    Main orchestration: create file → validate → add → commit → push.

    Executes the full workflow: file creation followed by validation,
    then git integration. Each step depends on the previous one completing successfully.

    Raises:
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

        print("\n[OK] Feature 234 implementation complete!")
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
