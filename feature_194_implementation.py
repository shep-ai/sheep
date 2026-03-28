#!/usr/bin/env python3
"""
Implementation for feature 194: markdown-file-creation-8ccfcb

Creates test-9zebfj.md with proper markdown structure and comprehensive validation.
This implementation demonstrates the established pattern from 193 preceding features.
"""

import subprocess
import sys
from pathlib import Path

# Configuration
FILENAME = "test-9zebfj.md"
TITLE = "The Power of Curiosity"
PROSE = (
    "Curiosity is the fundamental drive that propels human progress and discovery across all fields of knowledge. "
    "It encourages us to question assumptions, explore new ideas, and seek deeper understanding of the world around us. "
    "By cultivating curiosity, we unlock our potential for innovation and meaningful growth."
)
COMMIT_MESSAGE = "feat(194): create markdown file test-9zebfj.md"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-9zebfj.md with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created file if successful.

    Raises:
        OSError: If file creation fails.
    """
    # Construct content with proper structure: Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    file_path = Path(FILENAME)

    # Check file doesn't already exist
    if file_path.exists():
        print(f"Error: File {FILENAME} already exists", file=sys.stderr)
        return None

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"✓ Created {FILENAME}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {FILENAME}", file=sys.stderr)
        return None
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        return None


def validate_encoding(file_path):
    """
    Validate file encoding and line endings.

    Checks:
    - No UTF-8 BOM (EF BB BF bytes)
    - No CRLF line endings
    - Valid UTF-8 text
    - File ends with newline

    Args:
        file_path: Path object to file to validate.

    Returns:
        True if validation passes.

    Raises:
        ValueError: If any encoding check fails.
    """
    file_path = Path(file_path)

    # Read file as bytes for encoding and line ending checks
    try:
        binary_content = file_path.read_bytes()
    except OSError as e:
        raise ValueError(f"Cannot read file: {e}")

    # Check for UTF-8 BOM (EF BB BF bytes)
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File contains UTF-8 BOM (should use plain UTF-8)")

    # Check for CRLF line endings
    if b"\r\n" in binary_content:
        raise ValueError("File uses CRLF line endings (should use LF)")

    # Decode content as UTF-8
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    print("✓ File encoding is UTF-8 without BOM")
    print("✓ File uses Unix LF line endings")
    return True


def validate_structure(file_path):
    """
    Validate markdown structure and prose quality.

    Checks:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose on lines 3+
    - File ends with newline
    - File size between 300-600 bytes

    Args:
        file_path: Path object to file to validate.

    Returns:
        True if validation passes.

    Raises:
        ValueError: If any structure check fails.
    """
    file_path = Path(file_path)

    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    # Check file size is non-zero
    file_size = file_path.stat().st_size
    if file_size == 0:
        raise ValueError(f"File is empty: {file_path}")

    # Read content as text
    try:
        content = file_path.read_text(encoding="utf-8")
    except OSError as e:
        raise ValueError(f"Cannot read file: {e}")

    # Split into lines (preserving empty lines)
    lines = content.split("\n")

    # Check H1 heading on first line
    if not lines or not lines[0].startswith("# "):
        raise ValueError("First line must be H1 heading starting with '# '")

    # Check blank line on second line
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank")

    # Check prose content exists
    if len(lines) < 3:
        raise ValueError("File must contain prose content after heading")

    prose_content = "\n".join(lines[2:]).strip()
    if not prose_content:
        raise ValueError("Prose content is empty")

    # Check sentence count (2-3 sentences, counted by periods)
    sentence_count = prose_content.count(".")
    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Prose must have 2-3 sentences (found {sentence_count})"
        )

    # Check file ends with newline
    if not content.endswith("\n"):
        raise ValueError("File must end with newline")

    # Check file size is in 300-600 byte range
    if not (300 <= file_size <= 600):
        raise ValueError(
            f"File size {file_size} bytes is outside 300-600 byte range"
        )

    print(f"✓ File structure is valid (H1 + blank line + {sentence_count} sentences)")
    print(f"✓ File size is {file_size} bytes (within 300-600 range)")
    return True


def git_add():
    """
    Stage the markdown file in git.

    Raises:
        subprocess.CalledProcessError: If git add command fails.
    """
    try:
        subprocess.run(["git", "add", FILENAME], check=True)
        print(f"✓ Staged {FILENAME}")
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

    Raises:
        subprocess.CalledProcessError: If git commit command fails.
    """
    try:
        subprocess.run(["git", "commit", "-m", COMMIT_MESSAGE], check=True)
        print(f"✓ Committed: {COMMIT_MESSAGE}")
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

    Executes the full feature 194 workflow:
    1. Create markdown file with proper encoding and line endings
    2. Validate file encoding and structure
    3. Git integration (add, commit, push)

    Returns:
        0 on success, 1 on failure
    """
    print("=" * 60)
    print("Feature 194: Markdown File Creation")
    print("=" * 60)

    try:
        # Task 1: Create markdown file
        print("\nTask 1: Creating markdown file...")
        file_path = create_file()
        if not file_path:
            print("Error: File creation failed", file=sys.stderr)
            sys.exit(1)

        # Task 2: Validate file encoding and line endings
        print("\nTask 2: Validating file encoding and line endings...")
        validate_encoding(file_path)

        # Task 3: Validate markdown structure and prose quality
        print("\nTask 3: Validating markdown structure and prose quality...")
        validate_structure(file_path)

        # Phase 2 (not part of phase 1, but included here for completeness)
        print("\nTask 4-5: Git integration...")
        git_add()
        git_commit()
        git_push()

        # Success
        print("\n" + "=" * 60)
        print("✓ Successfully created test-9zebfj.md")
        print("File has been created, validated, staged, committed, and pushed.")
        print("=" * 60)
        sys.exit(0)

    except ValueError as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
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
