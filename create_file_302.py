#!/usr/bin/env python3
"""
Create a markdown file (test-94uqvv.md) with title and prose content.

This script automates the creation of a test markdown file following the established
pattern from 300+ existing test files in the Sheep repository. The implementation:
1. Creates a markdown file with H1 heading and 2-3 sentences of prose
2. Validates the file structure, encoding, and size
3. Stages, commits, and pushes the file to git

The script uses only Python standard library modules (pathlib, subprocess, sys)
and adheres to project requirements:
- UTF-8 encoding without BOM (Byte Order Mark)
- Unix-style LF line endings
- File size typically 400-600 bytes
- Conventional commit message format
"""

import subprocess
import sys
from pathlib import Path

# Ensure proper output encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Module-level constants
FILENAME = "test-94uqvv.md"
MARKDOWN_TITLE = "The Power of Curiosity"
MARKDOWN_PROSE = (
    "Curiosity is the fundamental drive that propels humans to explore, question, and discover new knowledge about the world around them. "
    "From ancient philosophers to modern scientists, the curious mind has been the engine of human progress and innovation throughout history. "
    "Cultivating and nurturing our natural curiosity allows us to lead more fulfilling, engaged, and meaningful lives."
)
COMMIT_MESSAGE = "feat(302): create markdown file test-94uqvv.md with prose content"


def create_file():
    """
    Create the markdown file with proper UTF-8 encoding and LF line endings.

    This function:
    - Defines the markdown content (H1 heading + 2-3 sentences of prose)
    - Writes the file using pathlib.Path.write_bytes() with explicit encoding
    - Ensures UTF-8 encoding without BOM and Unix LF line endings

    Returns:
        Path: The pathlib.Path object pointing to the created file

    Raises:
        IOError: If file creation fails (e.g., permission denied, disk full)
    """
    # Construct the markdown content with H1 heading and prose
    # Using explicit '\n' characters ensures LF line endings
    content = f"# {MARKDOWN_TITLE}\n\n{MARKDOWN_PROSE}\n"

    # Write the file using pathlib.Path.write_bytes() with explicit UTF-8 encoding
    # This ensures:
    # - UTF-8 encoding without BOM (Byte Order Mark)
    # - Unix LF line endings (not CRLF on Windows)
    # - Platform independence
    # Using write_bytes() with encode('utf-8') ensures no platform-specific line ending conversion
    filepath = Path(FILENAME)
    filepath.write_bytes(content.encode('utf-8'))

    return filepath


def validate_encoding(filepath):
    """
    Validate that file is UTF-8 encoded without BOM and uses Unix LF line endings.

    This function checks:
    - File does not contain UTF-8 BOM (byte sequence 0xEF 0xBB 0xBF)
    - File uses Unix LF (0x0A) line endings, not CRLF (0x0D 0x0A)

    Args:
        filepath (Path): Path object pointing to the markdown file

    Returns:
        bool: True if encoding validation passes

    Raises:
        AssertionError: If file contains BOM or CRLF line endings
    """
    # Read file as bytes to check encoding at byte level
    file_bytes = filepath.read_bytes()

    # Check 1: File should not contain UTF-8 BOM (0xEF 0xBB 0xBF)
    assert not file_bytes.startswith(b'\xef\xbb\xbf'), (
        "File contains UTF-8 BOM (Byte Order Mark). Use UTF-8 without BOM."
    )

    # Check 2: File should not contain CRLF (0x0D 0x0A) line endings
    assert b'\r\n' not in file_bytes, (
        "File contains CRLF (Windows) line endings. Use Unix LF (\\n) line endings instead."
    )

    return True


def validate_structure(filepath):
    """
    Validate file structure: H1 heading, blank line, 2-3 sentences, and file size.

    This function checks:
    - File contains H1 heading on first line (starts with "# ")
    - File contains blank line separator on line 2
    - File contains 2-3 sentences of prose (counted by periods)
    - File size is between 300-800 bytes

    Args:
        filepath (Path): Path object pointing to the markdown file

    Returns:
        bool: True if all structure validations pass

    Raises:
        AssertionError: If any structure check fails
    """
    # Read content as text for structure validation
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    # Check 1: File must start with H1 heading (# <title>)
    assert len(lines) > 0, "File is empty"
    assert lines[0].startswith('# '), (
        "File must start with H1 heading on line 1 (format: # <title>)"
    )

    # Check 2: Line 2 must be blank (blank line separator)
    assert len(lines) > 1, "File must have at least 2 lines"
    assert lines[1] == '', (
        "Line 2 must be blank (blank line separator between heading and prose)"
    )

    # Check 3: Prose must contain 2-3 sentences (detect by counting periods)
    # Extract prose after heading and blank line
    prose_lines = lines[2:]  # Skip H1 and blank line
    prose = '\n'.join(prose_lines).strip()

    sentence_count = prose.count('.')
    assert 2 <= sentence_count <= 3, (
        f"Prose must contain 2-3 sentences; found {sentence_count} period(s). "
        f"Sentence count is determined by counting periods (.)."
    )

    # Check 4: File size is in valid range (300-800 bytes)
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, (
        f"File size {file_size} bytes is outside valid range (300-800 bytes). "
        f"Expected approximately 400-600 bytes."
    )

    return True


def validate_file(filepath):
    """
    Validate the markdown file structure, encoding, and size.

    This function checks:
    - File exists and is readable
    - File size is in typical range (300-800 bytes)
    - File contains H1 heading on first line
    - File contains blank line after heading
    - File contains prose content

    Args:
        filepath (Path): Path object pointing to the markdown file

    Returns:
        bool: True if all validations pass

    Raises:
        AssertionError: If any validation fails
    """
    # Check 1: File exists
    assert filepath.exists(), f"File {filepath} does not exist"

    # Check 2: File size is in typical range (300-800 bytes)
    # The 400-600 byte range is a soft guideline; we tolerate 300-800 for flexibility
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, (
        f"File size {file_size} bytes is outside typical range (300-800 bytes). "
        f"Expected approximately 400-600 bytes for structure: H1 heading + 2-3 sentences."
    )

    # Check 3: File contains H1 heading on first line
    content = filepath.read_text(encoding='utf-8')
    assert content.startswith('# '), "File must start with H1 heading (# )"

    # Check 4: File contains blank line after heading
    assert '\n\n' in content, "File must contain blank line after heading (double newline)"

    # Check 5: File has prose content after blank line
    # Split by double newline to separate heading from prose
    parts = content.split('\n\n', 1)
    assert len(parts) == 2, "File structure should be: heading, blank line, prose"
    prose = parts[1].strip()
    assert len(prose) > 0, "File must contain prose content after heading"

    return True


def git_operations():
    """
    Stage, commit, and push the markdown file to git.

    This function performs:
    1. git add test-94uqvv.md (stage the file)
    2. git commit -m "feat(302): create markdown file test-94uqvv.md with prose content"
    3. git push -u origin HEAD (push to remote)

    Uses subprocess.run() with check=True for strict error handling.
    Any git command failure raises CalledProcessError.

    Raises:
        subprocess.CalledProcessError: If any git command fails
    """
    # Stage the file using git add
    # check=True ensures CalledProcessError is raised if git add fails
    print("Staging file with git add...")
    subprocess.run(["git", "add", FILENAME], check=True)
    print("✓ File staged")

    # Commit the file with conventional commit message
    print(f"Committing with message: {COMMIT_MESSAGE}")
    subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
    print("✓ File committed")

    # Push to remote origin using current branch
    # The -u flag sets upstream tracking for the current branch
    # HEAD refers to the current branch being worked on
    print("Pushing to remote origin...")
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)
    print("✓ File pushed to remote")


def main():
    """
    Main entry point: orchestrate file creation, validation, and git operations.

    This function coordinates the workflow:
    1. Create the markdown file
    2. Validate the file encoding (UTF-8 without BOM, Unix LF line endings)
    3. Validate the file structure (H1 heading, blank line, 2-3 sentences, file size)
    4. Perform git operations (add, commit, push)

    Exits with status code 0 on success, 1 on failure.
    """
    try:
        # Phase 1: File creation
        print("Creating markdown file...")
        filepath = create_file()
        print(f"✓ File created: {filepath}")

        # Phase 2: Comprehensive validation before git operations
        print("\nValidating file encoding...")
        validate_encoding(filepath)
        print("✓ File encoding validation passed (UTF-8 without BOM, Unix LF line endings)")

        print("Validating file structure...")
        validate_structure(filepath)
        print("✓ File structure validation passed (H1 heading, blank line, 2-3 sentences, file size)")

        # Phase 3: Git integration and execution
        print("\nPerforming git operations...")
        git_operations()

        print("\n✓ Workflow complete!")
        print("File has been created, validated, staged, committed, and pushed to remote.")
        sys.exit(0)

    except subprocess.CalledProcessError as e:
        print(f"✗ Git command failed: {e}", file=sys.stderr)
        print(f"Command: {e.cmd}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
