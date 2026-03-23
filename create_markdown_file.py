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
