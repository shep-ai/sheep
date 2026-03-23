#!/usr/bin/env python3
"""
Implementation script for feature 174: markdown-file-creation-1fc9b9
Creates test-u9soe6.md with proper markdown structure and validation.
"""

import sys
from pathlib import Path

# Module-level constants
FILENAME = "test-u9soe6.md"
TITLE = "The Art of Thoughtful Design"
PROSE = (
    "Thoughtful design considers the needs and experiences of users at every stage of the journey, "
    "understanding that each interaction shapes how people perceive and engage with products. "
    "It balances aesthetics with functionality, creating solutions that are both beautiful and intuitive to navigate. "
    "By prioritizing clarity and empathy in design decisions, we create products that resonate deeply with people and transform their daily experiences."
)
COMMIT_MESSAGE = "feat(174): create markdown file test-u9soe6.md with prose content"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-u9soe6.md in the current working directory with:
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
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"✓ Created {file_path}")
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
    - File size within 400-600 bytes

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

    # Check file size is in 400-600 byte range
    if not (400 <= file_size <= 600):
        raise ValueError(
            f"File size {file_size} bytes is outside 400-600 byte range"
        )

    return True


def main():
    """Main entry point: create file."""
    print("=" * 60)
    print("Feature 174: Markdown File Creation - Phase 1")
    print("=" * 60)

    try:
        print("\nPhase 1: Creating markdown file...")
        file_path = create_file()
        if not file_path:
            sys.exit(1)

        print("\n" + "=" * 60)
        print("✓ File created successfully!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    main()
