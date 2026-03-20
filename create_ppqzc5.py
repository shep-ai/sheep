#!/usr/bin/env python3
"""
Feature 130 implementation: Create markdown file test-ppqzc5.md
with a level-1 heading and 2-3 sentences of prose content.

Uses pathlib.Path.write_text() with explicit UTF-8 encoding and
Unix-style LF line endings (\n) for cross-platform compatibility.
"""

from pathlib import Path


def create_markdown_file():
    """
    Create test-ppqzc5.md at the repository root.

    File structure:
    - Level-1 markdown heading (# Title)
    - One blank line
    - 2-3 sentences of readable prose

    Encoding: UTF-8 without BOM
    Line endings: LF (\n), not CRLF
    """

    # Define the markdown content with human-written prose
    # Topic: Technology and Innovation
    content = (
        "# The Evolution of Technology\n"
        "\n"
        "Technology has fundamentally transformed human civilization, enabling us to solve complex problems and connect across vast distances. From the invention of the printing press to the internet, each technological revolution has shaped how we communicate, work, and learn. As we continue to innovate, we must consider both the tremendous opportunities and the responsibilities that come with powerful tools."
    )

    # Create the file using pathlib with explicit UTF-8 encoding and LF line endings
    # encoding='utf-8' ensures UTF-8 without BOM (Python's UTF-8 codec doesn't add BOM by default)
    # newline='\n' ensures Unix-style LF line endings (0x0A) on all platforms, including Windows
    file_path = Path("test-ppqzc5.md")
    file_path.write_text(content, encoding='utf-8', newline='\n')

    # Verify file was created
    assert file_path.exists(), "Failed to create test-ppqzc5.md"

    # Get file stats for validation
    file_size = file_path.stat().st_size
    print(f"Created test-ppqzc5.md ({file_size} bytes)")

    return file_path


if __name__ == "__main__":
    create_markdown_file()
