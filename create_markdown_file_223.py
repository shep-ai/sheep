#!/usr/bin/env python3
"""
Implementation script for feature 223: markdown-file-creation-995640
Creates test-do4dr9.md with proper markdown structure.
No validation layer per spec requirement.
"""

import subprocess
import sys
from pathlib import Path

# Module-level constants
FILENAME = "test-do4dr9.md"
TITLE = "The Art of Learning"
PROSE = (
    "Learning is a lifelong journey that shapes who we become and how we engage with the world. "
    "Every experience, whether success or failure, offers valuable lessons that deepen our understanding "
    "and expand our capabilities. By remaining curious and open to new ideas, we unlock our potential "
    "to grow and adapt in an ever-changing environment."
)
COMMIT_MESSAGE = "feat(223): Create markdown file test-do4dr9.md"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-do4dr9.md in the current working directory with:
    - H1 heading on line 1
    - Blank line on line 2
    - 2-3 sentences of prose content
    - UTF-8 encoding without BOM
    - Unix LF line endings

    Returns:
        Path object to the created file if successful.

    Raises:
        FileExistsError: If file already exists (defensive check).
        OSError: If file creation fails.
    """
    # Construct content string with proper structure:
    # Heading\n\nProse\n
    content = f"# {TITLE}\n\n{PROSE}\n"

    # Create file path
    file_path = Path(FILENAME)

    # Check file doesn't already exist (defensive check)
    if file_path.exists():
        raise FileExistsError(f"File {file_path} already exists")

    try:
        # Write file with UTF-8 encoding and Unix LF line endings
        # encoding="utf-8" ensures UTF-8 without BOM
        # newline="\n" forces Unix LF line endings on all platforms
        file_path.write_text(content, encoding="utf-8", newline="\n")
        print(f"✓ Created {file_path}")
        return file_path
    except PermissionError:
        print(f"Error: Permission denied writing to {file_path}", file=sys.stderr)
        raise
    except OSError as e:
        print(f"Error creating file: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    pass
