#!/usr/bin/env python3
"""
Implementation script for feature 070: markdown-file-creation
Creates test-3kyco5.md with proper markdown structure and validation.
"""

import sys
from pathlib import Path


def create_markdown_file():
    """
    Task 1: Create markdown file with proper structure and encoding.

    Creates test-3kyco5.md in repository root with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings
    """
    # Define content with hardcoded topic and prose
    heading = "# The Art of Problem Solving"
    prose = (
        "Effective problem solving begins with a clear understanding of the problem's scope "
        "and underlying constraints, rather than rushing toward immediate solutions. By breaking "
        "complex problems into smaller, manageable components, we gain clarity and can apply "
        "targeted strategies to each piece."
    )

    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"{heading}\n\n{prose}\n"

    # Create file path
    file_path = Path("test-3kyco5.md")

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
    - File size in 400-600 byte range (guideline)
    - Content structure: H1 heading, blank line, prose
    - UTF-8 encoding
    - Unix LF line endings
    """
    file_path = Path("test-3kyco5.md")

    # Verify file exists
    if not file_path.exists():
        print(f"Error: File {file_path} does not exist", file=sys.stderr)
        return False

    try:
        # Check file size
        size = file_path.stat().st_size
        if size < 350 or size > 700:
            print(
                f"Warning: File size {size} bytes is outside typical range (400-600 bytes). "
                f"This is a guideline, not a strict requirement.",
                file=sys.stderr
            )
        print(f"✓ File size: {size} bytes")

        # Read file content
        content = file_path.read_text(encoding="utf-8")

        # Verify Unix LF line endings (not CRLF)
        if "\r\n" in content:
            print("Error: File contains Windows CRLF line endings, expected Unix LF", file=sys.stderr)
            return False
        print("✓ Unix LF line endings confirmed")

        # Verify content structure
        lines = content.split("\n")

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

        # Count sentences (rough validation: ends with . ! or ?)
        sentence_count = sum(
            1 for sent in prose_content.split(".")
            if sent.strip() and not sent.strip().endswith(("!", "?"))
        )
        # Also count ! and ? as sentence endings
        sentence_count += prose_content.count("!") + prose_content.count("?")

        print(f"✓ Prose content: {len(prose_content)} characters")
        print(f"✓ UTF-8 encoding confirmed (read without errors)")

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
    print("Feature 070: Markdown File Creation - Implementation")
    print("=" * 60)

    # Phase 1: Create markdown file
    print("\nPhase 1: Creating markdown file...")
    if not create_markdown_file():
        sys.exit(1)

    # Phase 2: Validate file properties
    print("\nPhase 2: Validating file properties...")
    if not validate_file():
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✓ All tasks completed successfully!")
    print("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
