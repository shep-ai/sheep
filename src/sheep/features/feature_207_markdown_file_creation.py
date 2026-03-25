"""Implementation for feature 207: Create markdown file test-jkyks3.md with title and prose content.

This module orchestrates the creation of a markdown file with hard-coded, deterministic content.
Following the established pattern from feature 206, this feature uses hard-coded content to demonstrate
straightforward file creation within the Sheep workflow without external API dependencies.

The file is created with:
- Exact filename: test-jkyks3.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations

This approach provides:
- Deterministic output (identical on repeated execution)
- Transparent, auditable content (no API dependencies)
- Simplified error handling (no network failures)
- Faster execution (no API latency)
- Reliable testing and review (reproducible results)
"""

import subprocess
import sys
from pathlib import Path

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 207 constants
FILENAME = "test-jkyks3.md"
FEATURE_NUMBER = 207
BRANCH_NAME = "feat/207-markdown-file-creation-53da5b"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME}"

# Hard-coded markdown content
# H1 title about a technical topic
TITLE_TEXT = "The Power of Asynchronous Programming"

# 2-3 sentences of prose content related to the title
PROSE_CONTENT = (
    "Asynchronous programming enables applications to handle multiple tasks concurrently "
    "without blocking the main execution thread. This approach is essential for building responsive "
    "user interfaces and efficient server applications. Modern programming languages and frameworks "
    "provide powerful abstractions like async/await that make asynchronous code easier to write and understand."
)


def create_markdown_file() -> Path:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings via pathlib.Path.write_text().

    Returns:
        Path object pointing to created file

    Raises:
        ValueError: If file creation fails
        OSError: If file write operation fails
    """
    _logger.info(f"Creating markdown file: {FILENAME}")

    try:
        # Construct markdown content: # Title \n \n Prose
        markdown_content = f"# {TITLE_TEXT}\n\n{PROSE_CONTENT}\n"

        # Write file with UTF-8 encoding and LF line endings
        file_path = Path(FILENAME)
        file_path.write_text(markdown_content, encoding="utf-8")

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {file_path}")

        file_size = file_path.stat().st_size
        _logger.info(f"Successfully created {FILENAME} ({file_size} bytes)")

        return file_path

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


def verify_file_exists(filename: str = FILENAME) -> None:
    """Verify that the markdown file exists.

    Args:
        filename: Path to file to verify (defaults to FILENAME)

    Raises:
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Checking file exists: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")


def validate_markdown_format(filename: str = FILENAME) -> None:
    """Validate markdown file structure: H1 heading, blank line, prose.

    Checks that:
    1. File starts with exactly one H1 heading (# Title)
    2. Line 2 is blank (separator between heading and prose)
    3. Exactly one H1 heading exists in the file

    Args:
        filename: Path to markdown file to validate

    Raises:
        ValueError: If markdown format is invalid
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating markdown format: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Check first line is H1 heading
    if not lines or not lines[0].startswith("# "):
        raise ValueError("File must start with H1 heading (# Title)")

    # Check second line is blank (blank line separator)
    if len(lines) < 2 or lines[1].strip() != "":
        raise ValueError("Second line must be blank (separator between heading and prose)")

    # Check exactly one H1 heading exists
    h1_count = sum(1 for line in lines if line.startswith("# ") and not line.startswith("# #"))
    if h1_count != 1:
        raise ValueError(f"File must contain exactly one H1 heading, found {h1_count}")


def extract_prose_content(filename: str = FILENAME) -> str:
    """Extract prose content from markdown file.

    Extracts the text content that appears after the H1 heading and blank line.
    This helper function is used by other validation functions.

    Args:
        filename: Path to markdown file

    Returns:
        Prose content as string (empty if no prose found)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file structure is invalid
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Find blank line after heading (should be at index 1)
    blank_line_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "" and i > 0:
            blank_line_idx = i
            break

    if blank_line_idx is None:
        raise ValueError("No blank line separator found after heading")

    # Extract prose content (all lines after blank line)
    prose_lines = lines[blank_line_idx + 1:]
    prose_text = "\n".join(prose_lines).strip()

    return prose_text


def count_sentences(prose: str) -> int:
    """Count sentences in prose text using period counting.

    Counts the number of periods (.) in the prose content. This is a simple
    but effective approach for validating sentence count in typical prose.

    Args:
        prose: Text content to count sentences in

    Returns:
        Number of periods found in the prose

    Raises:
        ValueError: If prose is empty
    """
    if not prose:
        raise ValueError("Prose content is empty")

    return prose.count(".")


def validate_sentence_count(filename: str = FILENAME) -> None:
    """Validate file contains exactly 2-3 sentences of prose.

    Extracts prose content and counts periods to validate exactly 2-3 sentences.
    This function uses the extract_prose_content() and count_sentences() helpers.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If sentence count is not 2-3
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating sentence count: {filename}")
    prose_text = extract_prose_content(filename)
    sentence_count = count_sentences(prose_text)

    if not (2 <= sentence_count <= 3):
        raise ValueError(f"Expected 2-3 sentences, found {sentence_count}")
