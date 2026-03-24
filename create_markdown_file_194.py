#!/usr/bin/env python3
"""
Implementation script for feature 194: markdown-file-creation-195fc2
Creates test-omg7kb.md with proper markdown structure and validation.
"""

import sys
import subprocess
from pathlib import Path

# Module-level constants
FILENAME = "test-omg7kb.md"
TITLE = "The Wonder of Deep Sea Exploration"
PROSE = (
    "The deep ocean remains one of Earth's final frontiers, "
    "harboring extraordinary creatures and ecosystems that exist in almost complete darkness and extreme pressure. "
    "Scientists continue to make remarkable discoveries about bioluminescence, hydrothermal vents, and bizarre life forms adapted to these harsh conditions. "
    "These underwater expeditions expand our understanding of life's resilience and reveal the incredible diversity hidden beneath the ocean's surface."
)
COMMIT_MESSAGE = "feat(194): create markdown file test-omg7kb.md with prose content"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-omg7kb.md in the current working directory with:
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
    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Create file path
    file_path = Path(FILENAME)

    # Check file doesn't already exist
    if file_path.exists():
        print(f"Error: File {file_path} already exists", file=sys.stderr)
        return None

    try:
        # Write file with UTF-8 encoding and Unix LF line endings.
        # Using write_bytes() with explicit .encode('utf-8') provides:
        # - Guarantee of UTF-8 without BOM (no 0xEF 0xBB 0xBF prefix)
        # - Explicit control over line endings (bypasses platform translation)
        # - LF (\n) is guaranteed on all platforms (Windows, macOS, Linux)
        file_path.write_bytes(content.encode('utf-8'))
        print(f"[OK] Created {file_path}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        return None
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        return None


def validate_file(file_path):
    """
    Validate markdown file structure and properties.

    Performs comprehensive validation of the created markdown file:
    - File exists and has non-zero size
    - UTF-8 encoding without BOM
    - Unix LF line endings (no CRLF)
    - H1 heading on first line
    - Blank line on second line
    - 2-3 sentences of prose content
    - File ends with newline
    - File size within 300-600 bytes

    Args:
        file_path: Path object or string path to file to validate.

    Returns:
        True if validation passes.

    Raises:
        ValueError: If any validation check fails, with descriptive message.
    """
    file_path = Path(file_path)

    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    # Check file size is non-zero
    file_size = file_path.stat().st_size
    if file_size == 0:
        raise ValueError(f"File is empty: {file_path}")

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
        content = binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    # Split into lines (preserving empty lines)
    lines = content.split("\n")

    # Check H1 heading on first line
    if not lines or not lines[0].startswith("# "):
        raise ValueError("First line must be H1 heading starting with '# '")

    # Check blank line on second line
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank")

    # Check prose content has 2-3 sentences
    if len(lines) < 3:
        raise ValueError("File must contain prose content after heading")

    prose_content = "\n".join(lines[2:]).strip()
    if not prose_content:
        raise ValueError("Prose content is empty")

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

    return True


def git_add():
    """
    Stage the markdown file in git.

    Uses 'git add' command to stage the file for commit.

    Raises:
        subprocess.CalledProcessError: If git add command fails.
    """
    try:
        subprocess.run(["git", "add", FILENAME], check=True)
        print(f"[OK] Staged {FILENAME} with git add")
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
        print(f"[OK] Created commit: {COMMIT_MESSAGE}")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def git_push():
    """
    Push the commit to the feature branch.

    Uses 'git push origin HEAD' to push to the current branch.

    Raises:
        subprocess.CalledProcessError: If git push command fails.
    """
    try:
        subprocess.run(["git", "push", "origin", "HEAD"], check=True)
        print("[OK] Pushed commit to feature branch")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            e.output,
            e.stderr,
        ) from e


def main():
    """Main entry point for the feature implementation."""
    try:
        # Phase 1: File Creation & Validation Foundation
        print("=== Phase 1: File Creation & Validation ===")

        # Create the markdown file
        file_path = create_file()
        if file_path is None:
            print("Error: Failed to create file", file=sys.stderr)
            return 1

        # Validate the file
        try:
            validate_file(file_path)
            print(f"[OK] Validated {FILENAME}")
        except ValueError as e:
            print(f"Error: Validation failed: {e}", file=sys.stderr)
            return 1

        # Phase 2: Git Integration & Delivery
        print("\n=== Phase 2: Git Integration ===")

        # Stage the file
        try:
            git_add()
        except subprocess.CalledProcessError as e:
            print(f"Error: git add failed", file=sys.stderr)
            if e.stderr:
                print(e.stderr, file=sys.stderr)
            return 1

        # Commit the file
        try:
            git_commit()
        except subprocess.CalledProcessError as e:
            print(f"Error: git commit failed", file=sys.stderr)
            if e.stderr:
                print(e.stderr, file=sys.stderr)
            return 1

        # Push the commit
        try:
            git_push()
        except subprocess.CalledProcessError as e:
            print(f"Error: git push failed", file=sys.stderr)
            if e.stderr:
                print(e.stderr, file=sys.stderr)
            return 1

        print("\n[OK] Feature 194 implementation complete")
        return 0

    except Exception as e:
        print(f"Error: Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
