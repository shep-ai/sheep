#!/usr/bin/env python3
"""
Implementation script for feature 229: markdown-file-creation-530bb9
Creates test-c1ds43.md with proper markdown structure and comprehensive validation.
Includes post-creation validation to ensure UTF-8 encoding, Unix LF line endings,
and proper markdown format before git operations.
"""

import subprocess
import sys
import re
from pathlib import Path

# Module-level constants
FILENAME = "test-c1ds43.md"
TITLE = "Observability in Modern Software Systems"
PROSE = (
    "Observability is essential for understanding complex distributed systems in production environments, "
    "where traditional debugging approaches fall short against the complexity of microservices architectures. "
    "Combining metrics, logs, and traces helps engineers identify root causes and respond quickly before users are impacted. "
    "By implementing comprehensive observability practices, teams can reduce mean time to recovery and build more reliable systems."
)
COMMIT_MESSAGE = "feat(229): create markdown file test-c1ds43.md with prose content"


def validate_markdown_file(file_path):
    """
    Validate markdown file format, encoding, and line endings.

    Checks:
    - File exists and is readable
    - Content starts with H1 heading (# )
    - File contains 2-3 sentences (counts . ! ? characters)
    - No CRLF line endings (Unix LF only)
    - No UTF-8 BOM
    - File size 400-600 bytes

    Args:
        file_path (Path): Path to the markdown file to validate

    Returns:
        bool: True if all validations pass

    Raises:
        AssertionError: If any validation fails with descriptive message
    """
    # Check file exists
    assert file_path.exists(), f"File {file_path} does not exist"

    # Read content as text
    content = file_path.read_text(encoding="utf-8")

    # Validate H1 heading
    assert content.startswith("# "), "File should start with H1 heading (# )"

    # Validate sentence count (2-3 sentences)
    sentence_count = sum(1 for char in content if char in ".!?")
    assert 2 <= sentence_count <= 3, (
        f"File should contain 2-3 sentences, found {sentence_count}"
    )

    # Validate no CRLF line endings
    assert "\r\n" not in content, "File should use LF line endings, not CRLF"

    # Validate no UTF-8 BOM
    with open(file_path, "rb") as f:
        first_bytes = f.read(3)
    assert first_bytes != b"\xef\xbb\xbf", "File should not have UTF-8 BOM"

    # Validate file size (400-600 bytes)
    file_size = file_path.stat().st_size
    assert 400 <= file_size <= 600, (
        f"File size {file_size} should be between 400-600 bytes"
    )

    return True


def create_and_validate_markdown():
    """
    Create markdown file with proper structure and comprehensive validation.

    Creates test-c1ds43.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Performs comprehensive post-creation validation to ensure:
    - H1 heading present
    - 2-3 sentences present
    - UTF-8 encoding without BOM
    - Unix LF line endings (not CRLF)
    - File size 400-600 bytes

    Returns:
        Path object to the created and validated file if successful.

    Raises:
        FileExistsError: If file already exists (defensive check).
        AssertionError: If validation fails.
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
        # encoding="utf-8" ensures UTF-8 without BOM (Python's default)
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"✓ Created {file_path}")

        # Perform comprehensive post-creation validation
        validate_markdown_file(file_path)
        print("✓ Validated file format, encoding, and line endings")

        return file_path

    except AssertionError as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        # Clean up invalid file
        if file_path.exists():
            file_path.unlink()
        raise
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        raise


def git_add():
    """
    Stage the markdown file in git.

    Uses 'git add' command to stage the file for commit.

    Raises:
        subprocess.CalledProcessError: If git add command fails.
    """
    try:
        subprocess.run(["git", "add", FILENAME], check=True)
        print(f"✓ Staged {FILENAME} with git add")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def git_commit():
    """
    Create a git commit with the markdown file.

    Uses 'git commit' with the conventional commit message format.

    Raises:
        subprocess.CalledProcessError: If git commit command fails.
    """
    try:
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
        print(f"✓ Created commit: {COMMIT_MESSAGE}")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def git_push():
    """
    Push the commit to the remote feature branch.

    Uses 'git push -u origin HEAD' to push to the current branch.
    The -u flag sets upstream tracking for the branch.

    Raises:
        subprocess.CalledProcessError: If git push command fails.
    """
    try:
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
        print("✓ Pushed to remote origin")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def main():
    """
    Main entry point: orchestrate complete workflow.

    Executes the full feature 229 workflow:
    1. Phase 1: Create markdown file with proper encoding and line endings,
       then validate format, encoding, and line endings
    2. Phase 2: Git integration (add, commit, push)

    Comprehensive validation per spec requirement ensures UTF-8 encoding,
    Unix LF line endings, and markdown format compliance before pushing.

    Catches specific exceptions and logs errors to stderr before exiting:
    - FileExistsError: File already exists (defensive check)
    - AssertionError: File validation failures
    - OSError: File I/O problems (system-level issue)
    - subprocess.CalledProcessError: Git command failures

    Returns:
        0 on success, 1 on failure
    """
    print("=" * 60)
    print("Feature 229: Markdown File Creation (with validation)")
    print("=" * 60)

    try:
        # Phase 1: Create and validate markdown file
        print("\nPhase 1: Creating and validating markdown file...")
        create_and_validate_markdown()

        # Phase 2: Git integration
        print("\nPhase 2: Git integration and workflow...")
        git_add()
        git_commit()
        git_push()

        # Success
        print("\n" + "=" * 60)
        print("Successfully created test-c1ds43.md")
        print("File has been created, validated, staged, committed, and pushed.")
        print("=" * 60)
        sys.exit(0)

    except FileExistsError as e:
        print(f"✗ File already exists: {e}", file=sys.stderr)
        sys.exit(1)
    except AssertionError as e:
        print(f"✗ File validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"✗ File I/O error: {e}", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"✗ Git command failed: {e.cmd}", file=sys.stderr)
        if e.stderr:
            print(f"  Error output: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
