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
