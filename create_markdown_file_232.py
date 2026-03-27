#!/usr/bin/env python3
"""
Implementation script for feature 232: markdown-file-creation-3a8cc2
Creates test-rnfcfc.md with proper markdown structure.
Phase 1: File Creation & Content Composition
No validation layer per spec requirement.
"""

import sys
from pathlib import Path

# Module-level constants
FILENAME = "test-rnfcfc.md"
TITLE = "The Magic of Natural Curiosity"
PROSE = (
    "Curiosity is a fundamental human trait that drives learning, innovation, and personal growth throughout our lives. "
    "When we embrace questions and explore ideas with genuine wonder, we unlock new perspectives and develop deeper understanding of the world around us. "
    "By nurturing this natural instinct to discover and learn, we create pathways to creativity and meaningful progress."
)
COMMIT_MESSAGE = "feat(232): Create markdown file test-rnfcfc.md with prose content"


def create_file():
    """
    Create markdown file with proper structure and encoding.

    Creates test-rnfcfc.md in the current working directory with:
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
