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
    2. Validate the file structure and content
    3. Perform git operations (add, commit, push)

    Exits with status code 0 on success, 1 on failure.
    """
    try:
        # Phase 1: File creation
        print("Creating markdown file...")
        filepath = create_file()
        print(f"✓ File created: {filepath}")

        print("Validating file...")
        validate_file(filepath)
        print("✓ File validation passed")

        # Phase 2: Git integration and execution
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
