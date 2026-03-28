#!/usr/bin/env python3
"""
Feature 195 Phase 2: File Creation & Validation (Local Implementation)

This script implements:
- Task 2: Write markdown file with correct encoding and line endings
- Task 3: Validate markdown file (structure, encoding, content)

Since phase 1 (content generation) may not have API credentials available,
this local implementation generates meaningful prose directly.
"""

import sys
from pathlib import Path

FILENAME = "test-2xz0x5.md"


def generate_markdown_content_local() -> str:
    """Generate meaningful markdown content locally without API."""
    # Generate thematically coherent title and prose
    title = "The Art of Clear Communication"

    prose = (
        "Clear communication is the foundation of human connection and understanding across all contexts. "
        "When we express our thoughts with precision and listen actively to others, we build trust and foster "
        "meaningful relationships that transcend barriers. Mastering this skill transforms both our personal "
        "and professional lives in profound ways."
    )

    content = f"# {title}\n\n{prose}\n"
    return content


def validate_markdown_content(content: str) -> bool:
    """
    Validate that content meets markdown format requirements.

    Returns:
        True if valid, raises ValueError otherwise.
    """
    if not content or not content.strip():
        raise ValueError("Generated content is empty")

    if not content.lstrip().startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")

    if len(content) < 50:
        raise ValueError("Generated content is too short to be meaningful")

    # Count sentences (periods)
    sentence_count = content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(f"Content should have 2-3 sentences, found {sentence_count}")

    return True


def write_file_with_encoding(filepath: str, content: str) -> None:
    """Write file with UTF-8 encoding and LF line endings."""
    # Validate filename safety
    if "/" in filepath or "\\" in filepath or filepath.startswith("."):
        raise ValueError(f"Invalid filename: {filepath}")

    # Get repository root (current directory)
    repo_root = Path.cwd()
    file_path = repo_root / filepath

    print(f"Writing markdown file to {file_path}")

    # Write with UTF-8 encoding and explicit LF line endings
    # Using newline='' and writing content as-is ensures LF only
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    # Verify file was created
    if not file_path.exists():
        raise OSError(f"File was not created: {file_path}")

    # Verify file has content
    file_size = file_path.stat().st_size
    if file_size == 0:
        raise OSError(f"File was created but is empty: {file_path}")

    print(f"✓ File created: {file_path} ({file_size} bytes)")


def validate_file_properties(filepath: str) -> bool:
    """
    Validate file encoding and line endings.

    Checks for:
    - UTF-8 encoding with no BOM
    - Unix LF line endings (not CRLF)
    """
    path = Path(filepath)

    if not path.exists():
        raise ValueError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    # Read file as binary to check encoding and line endings
    with open(path, "rb") as f:
        binary_content = f.read()

    # Check for UTF-8 BOM (should not be present)
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File has UTF-8 BOM (should not be present)")

    # Check for CRLF line endings (should use LF instead)
    if b"\r\n" in binary_content:
        raise ValueError("File uses CRLF line endings (should use LF)")

    # Verify the file is valid UTF-8
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")

    print("✓ File encoding validation passed (UTF-8, LF line endings)")
    return True


def validate_markdown_structure(filepath: str) -> bool:
    """
    Validate markdown structure and prose content.

    Checks for:
    - H1 heading on first line
    - Blank line separator
    - Exactly 2-3 sentences
    - Trailing newline
    """
    path = Path(filepath)

    # Read as text
    with open(path, encoding="utf-8") as f:
        text_content = f.read()

    lines = text_content.split("\n")

    # Check that first line is H1 heading
    if not lines[0].startswith("# "):
        raise ValueError("First line must be H1 heading (# )")

    # Check that second line is blank (separator)
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank (separator after heading)")

    # Get prose content (skip heading and blank line)
    prose_lines = lines[2:]

    # Remove trailing empty lines for prose validation
    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()

    if not prose_lines:
        raise ValueError("No prose content found after heading")

    prose_content = "\n".join(prose_lines).strip()

    # Validate sentence count (count periods)
    sentence_count = prose_content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(f"Content must have 2-3 sentences, found {sentence_count}")

    # Check for trailing newline (Unix convention)
    if not text_content.endswith("\n"):
        raise ValueError("File must end with trailing newline")

    # Check file size (250-600 bytes typical)
    file_size = path.stat().st_size
    if not (250 <= file_size <= 600):
        print(f"  Warning: File size {file_size} bytes is outside typical range (250-600)")

    print("✓ Markdown structure validation passed")
    print(f"  - H1 heading: '{lines[0]}'")
    print(f"  - Sentences: {sentence_count}")
    print(f"  - File size: {file_size} bytes")

    return True


def main():
    """Execute phase 2: File creation and validation."""
    print("=== Feature 195 Phase 2: File Creation & Validation ===\n")

    try:
        # Step 1: Generate markdown content
        print("Step 1: Generating markdown content")
        content = generate_markdown_content_local()
        validate_markdown_content(content)
        print(f"✓ Generated {len(content)} bytes of content\n")

        # Step 2: Write file with correct encoding (Task 2)
        print("Step 2: Writing markdown file with correct encoding/line endings")
        write_file_with_encoding(FILENAME, content)
        print("✓ Task 2 Complete\n")

        # Step 3: Validate file properties (Task 3 - Part A)
        print("Step 3a: Validating file properties (encoding, line endings)")
        full_path = Path.cwd() / FILENAME
        validate_file_properties(full_path)

        # Step 4: Validate file structure (Task 3 - Part B)
        print("Step 3b: Validating file structure and prose content")
        validate_markdown_structure(full_path)
        print("✓ Task 3 Complete\n")

        print("=== Phase 2 Complete ===")
        print(f"File: {FILENAME}")
        print(f"Path: {full_path}")
        print("Status: Ready for Phase 3 (Git Integration & Push)")

        return 0

    except Exception as e:
        print(f"\n✗ Phase 2 failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
