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


def validate_encoding() -> None:
    """Validate that file is properly encoded as UTF-8 without BOM.

    Checks:
    - File exists
    - File does not contain UTF-8 BOM (byte order mark: 0xEF 0xBB 0xBF)
    - File content is valid UTF-8 text

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file has UTF-8 BOM or invalid UTF-8 encoding
    """
    file_path = Path(FILENAME)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File {FILENAME} does not exist")

    # Read file as binary to check for BOM and encoding
    binary_content = file_path.read_bytes()

    # Check for UTF-8 BOM (byte order mark)
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"File {FILENAME} contains UTF-8 BOM (byte order mark)")

    # Verify content is valid UTF-8
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File {FILENAME} contains invalid UTF-8 encoding: {e}")


def validate_line_endings(filename: str = FILENAME) -> None:
    """Validate that file uses Unix LF line endings exclusively.

    Rejects files with Windows CRLF (\\r\\n) or Mac CR (\\r) line endings.
    Ensures cross-platform consistency for markdown files.

    Args:
        filename: Path to file to validate (defaults to FILENAME)

    Raises:
        ValueError: If file contains CRLF or CR line endings
        FileNotFoundError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} not found")

    binary_content = file_path.read_bytes()

    # Check for CRLF (Windows line endings)
    if b"\r\n" in binary_content:
        raise ValueError(
            f"File {filename} contains Windows CRLF (\\r\\n) line endings. "
            "Only Unix LF (\\n) line endings are allowed."
        )

    # Check for CR without LF (old Mac line endings)
    if b"\r" in binary_content:
        raise ValueError(
            f"File {filename} contains Mac CR (\\r) carriage return characters. "
            "Only Unix LF (\\n) line endings are allowed."
        )


def count_sentences(text: str) -> int:
    """Count sentences in text based on periods.

    Counts the number of periods in the text, treating each period as
    the end of one sentence.

    Args:
        text: Text to count sentences in

    Returns:
        Number of sentences (count of periods)
    """
    return text.count(".")


def validate_structure(filename: str) -> None:
    """Validate markdown file structure: H1 heading and 2-3 sentences.

    Verifies that the file contains:
    - Exactly one H1 heading (line starting with "# ")
    - 2-3 sentences of prose content (counted by periods)

    Args:
        filename: Path to file to validate

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If H1 heading is missing or sentence count is not 2-3
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")

    # Check for H1 heading (must start with "# ")
    lines = content.split("\n")
    if not lines or not lines[0].startswith("# "):
        raise ValueError(
            "Invalid markdown structure: file must start with H1 heading (# Title)"
        )

    # Get prose content (everything after the heading and blank line)
    # Typically: lines[0] = "# Title", lines[1] = "", lines[2+] = prose
    prose_lines = []
    if len(lines) > 2:
        # Join all lines after the blank line, excluding the final empty line from trailing \n
        prose_lines = lines[2:]

    prose_text = "\n".join(prose_lines).strip()
    sentence_count = count_sentences(prose_text)

    if sentence_count < 2:
        raise ValueError(
            f"Invalid markdown structure: expected 2-3 sentences, found {sentence_count}"
        )
    elif sentence_count > 3:
        raise ValueError(
            f"Invalid markdown structure: expected 2-3 sentences, found {sentence_count}"
        )


def validate_file_size(filename: str) -> None:
    """Validate that file size is within acceptable range (450-550 bytes).

    Checks that the file exists and has a size between 450 and 550 bytes,
    inclusive. File sizes outside this range indicate potential truncation,
    padding, or content issues.

    Args:
        filename: Path to file to validate

    Raises:
        ValueError: If file size is outside the acceptable range (450-550 bytes)
    """
    MIN_SIZE = 450
    MAX_SIZE = 550

    file_path = Path(filename)
    file_size = file_path.stat().st_size

    if not (MIN_SIZE <= file_size <= MAX_SIZE):
        raise ValueError(
            f"File size {file_size} bytes outside acceptable range {MIN_SIZE}-{MAX_SIZE} bytes"
        )
