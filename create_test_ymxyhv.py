#!/usr/bin/env python3
"""
Implementation script for feature 081: markdown-file-creation
Creates test-ymxyhv.md with proper markdown structure and validation.
"""

import sys
from pathlib import Path


def create_markdown_file():
    """
    Task 1: Create markdown file with proper structure and encoding.

    Creates test-ymxyhv.md in repository root with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings
    """
    # Define content with hardcoded topic and prose
    heading = "# The Dance of Northern Lights"
    prose = (
        "The aurora borealis paints the Arctic sky with ribbons of green and purple light, "
        "creating a natural phenomenon that has captivated humanity for centuries. This celestial "
        "display results from charged solar particles colliding with Earth's magnetic field and atmosphere, "
        "producing one of nature's most stunning visual spectacles. Witnessing the northern lights remains "
        "a profound experience that connects us to the vastness and beauty of the cosmos."
    )

    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"{heading}\n\n{prose}\n"

    # Create file path
    file_path = Path("test-ymxyhv.md")

    # Check file doesn't already exist
    if file_path.exists():
        print(f"Error: File {file_path} already exists", file=sys.stderr)
        return False

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM (NFR-1)
        # newline="\n" forces Unix LF line endings (NFR-2)
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"✓ Created {file_path}")
        return True
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        return False
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        return False


def validate_file():
    """
    Task 2: Validate file properties and structure.

    Validates:
    - File exists at repository root
    - File size in 300-600 byte range (guideline)
    - Content structure: H1 heading, blank line, prose
    - UTF-8 encoding without BOM
    - Unix LF line endings
    - Prose content has exactly 2-3 sentences
    """
    file_path = Path("test-ymxyhv.md")

    # Verify file exists
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist", file=sys.stderr)
        return False

    try:
        # Read file in binary mode to validate encoding and line endings
        binary_content = file_path.read_bytes()

        # Verify UTF-8 encoding (no BOM)
        if binary_content.startswith(b'\xef\xbb\xbf'):
            print("Error: File has UTF-8 BOM (should not have BOM)", file=sys.stderr)
            return False
        print("✓ UTF-8 encoding confirmed (no BOM)")

        # Verify Unix-style LF line endings (not Windows CRLF)
        if b'\r\n' in binary_content:
            print("Error: File uses Windows CRLF line endings (should use Unix LF)", file=sys.stderr)
            return False
        print("✓ Unix LF line endings confirmed")

        # Check file size
        size = len(binary_content)
        if size < 300 or size > 600:
            print(
                f"Warning: File size {size} bytes is outside typical range (300-600 bytes). "
                f"This is a guideline, not a strict requirement.",
                file=sys.stderr
            )
        else:
            print(f"✓ File size: {size} bytes (valid: 300-600)")

        # Read file content as text for structure validation
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Verify content structure
        # Line 0 should be H1 heading
        if not lines[0].startswith("# "):
            print(
                f"Error: First line must be H1 heading (starts with '# '), got: '{lines[0]}'",
                file=sys.stderr
            )
            return False
        print(f"✓ H1 heading: {lines[0]}")

        # Line 1 should be blank
        if lines[1] != "":
            print(
                f"Error: Second line must be blank, got: '{lines[1]}'",
                file=sys.stderr
            )
            return False
        print("✓ Blank line after heading")

        # Lines 2+ should contain prose
        prose_content = "\n".join(lines[2:]).strip()
        if not prose_content:
            print("Error: No prose content found after heading", file=sys.stderr)
            return False

        # Count sentences by counting sentence-ending punctuation
        # Count periods, exclamation marks, and question marks
        sentence_count = prose_content.count('.') + prose_content.count('!') + prose_content.count('?')

        if not (2 <= sentence_count <= 3):
            print(
                f"Error: Expected 2-3 sentences, found {sentence_count}",
                file=sys.stderr
            )
            return False
        print(f"✓ Prose content: {sentence_count} sentences (valid: 2-3)")
        print(f"✓ Prose length: {len(prose_content)} characters")

        return True

    except UnicodeDecodeError as e:
        print(f"Error: File is not valid UTF-8: {e}", file=sys.stderr)
        return False
    except OSError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point: create file, validate, and exit with appropriate status."""
    print("=" * 60)
    print("Feature 081: Markdown File Creation - Implementation")
    print("=" * 60)

    # Task 1: Create markdown file
    print("\nTask 1: Creating markdown file...")
    if not create_markdown_file():
        sys.exit(1)

    # Task 2: Validate file properties
    print("\nTask 2: Validating file properties...")
    if not validate_file():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✓ Phase 1 (File Creation & Validation) complete!")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
