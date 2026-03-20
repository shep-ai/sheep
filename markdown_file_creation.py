#!/usr/bin/env python3
"""
Markdown File Creation for feature 126, Phase 3, Task 3-1.

This module provides functions to create markdown test files with proper format,
encoding, and validation. Files are created at the repository root with:
- Level-1 markdown heading (# Title) as first line
- Blank line separator
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- LF (Unix-style) line endings
- File size between 400-600 bytes
"""

from pathlib import Path
import sys


def create_markdown_file(title, prose, repo_root=None):
    """
    Create a markdown file with proper format and encoding.

    Args:
        title: str - Markdown heading title (without the '# ' prefix)
        prose: str - 2-3 sentences of prose content
        repo_root: Path | str | None - Repository root directory. If None, uses current directory.

    Returns:
        Path - Path to the created file

    Raises:
        ValueError: If inputs are invalid (empty title, invalid prose, etc.)
        RuntimeError: If file creation fails or validation fails
    """
    # Validate inputs
    if not title or not isinstance(title, str):
        raise ValueError("title must be a non-empty string")
    if not prose or not isinstance(prose, str):
        raise ValueError("prose must be a non-empty string")

    # Determine repository root
    if repo_root is None:
        repo_root = Path.cwd()
    else:
        repo_root = Path(repo_root)

    # Construct file path
    file_path = repo_root / "test-lqbnqn.md"

    # Format content: heading + blank line + prose + final newline
    content = f"# {title}\n\n{prose}\n"

    # Create file with explicit UTF-8 encoding and LF line endings
    try:
        file_path.write_text(content, encoding="utf-8", newline="\n")
    except Exception as e:
        raise RuntimeError(f"Failed to create markdown file: {e}") from e

    # Validate the created file
    try:
        _validate_markdown_file(file_path)
    except ValueError as e:
        # Clean up on validation failure
        file_path.unlink(missing_ok=True)
        raise RuntimeError(f"File validation failed: {e}") from e

    return file_path


def _validate_markdown_file(file_path):
    """
    Validate markdown file properties.

    Args:
        file_path: Path - Path to the markdown file

    Raises:
        ValueError: If any validation check fails
    """
    # Check file exists
    if not file_path.exists():
        raise ValueError(f"File does not exist: {file_path}")

    # Check encoding (UTF-8 without BOM)
    binary_content = file_path.read_bytes()

    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File contains UTF-8 BOM (Byte Order Mark)")

    # Verify content can be decoded as UTF-8
    try:
        text_content = binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8 encoded: {e}") from e

    # Check line endings (LF only, no CRLF or CR)
    if b"\r\n" in binary_content:
        raise ValueError("File contains CRLF line endings (Windows-style)")
    if b"\r" in binary_content:
        raise ValueError("File contains CR line endings")

    # Check file structure
    lines = text_content.split("\n")

    if not lines:
        raise ValueError("File is empty")

    # Check heading
    if not lines[0].startswith("# "):
        raise ValueError("First line is not a markdown heading (# )")

    # Check blank line separator
    if len(lines) < 3 or lines[1] != "":
        raise ValueError("Second line is not blank (missing separator between heading and prose)")

    # Check prose content exists
    prose_lines = lines[2:]
    prose_content = "\n".join(prose_lines).strip()

    if not prose_content:
        raise ValueError("No prose content found after heading")

    # Check sentence count (2-3 sentences)
    sentence_count = prose_content.count(".")
    if not (2 <= sentence_count <= 3):
        raise ValueError(f"Prose must contain 2-3 sentences, found {sentence_count}")

    # Check file ends with newline
    if not text_content.endswith("\n"):
        raise ValueError("File does not end with a newline")

    # Check file size (400-600 bytes)
    file_size = len(binary_content)
    if not (400 <= file_size <= 600):
        raise ValueError(f"File size {file_size} bytes is outside range 400-600 bytes")


def main():
    """Main entry point for markdown file creation."""
    # For now, this would be called by another module that provides title and prose
    # This is a placeholder for manual testing if needed
    print("Markdown file creation module loaded successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
