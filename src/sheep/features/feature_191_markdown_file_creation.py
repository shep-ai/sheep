"""Implementation for feature 191: Create markdown file test-u1rtbw.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-u1rtbw.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 450-550 bytes
- Git staging, commit, and push operations
"""

import subprocess
import sys
from pathlib import Path

# Task 1: Define file content constants
FILENAME = "test-u1rtbw.md"
TITLE = "The Value of Clear Code Documentation"
PROSE = "Clear documentation is essential for building maintainable software systems that teams can understand and modify across different time periods and expertise levels. Well-documented code reduces cognitive load for developers and accelerates onboarding of new team members. By investing time in clear documentation, comments, and examples, developers create a foundation for long-term success and help teams deliver higher quality software."


def check_file_does_not_exist() -> None:
    """Verify that test-u1rtbw.md does not already exist.

    Raises:
        FileExistsError: If file exists with descriptive message
    """
    if Path(FILENAME).exists():
        raise FileExistsError(f"File {FILENAME} already exists")


def create_markdown_file() -> str:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings.

    Returns:
        Path to created file

    Raises:
        FileExistsError: If file already exists
        OSError: If file write operation fails
    """
    check_file_does_not_exist()
    content = f"# {TITLE}\n\n{PROSE}\n"
    Path(FILENAME).write_text(content, encoding="utf-8", newline="\n")
    return str(Path(FILENAME).absolute())
