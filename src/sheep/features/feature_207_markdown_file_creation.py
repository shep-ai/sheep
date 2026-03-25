"""Implementation for feature 207: Create markdown file test-ywcbdk.md with title and prose content.

This module orchestrates the creation of a markdown file with hard-coded, deterministic content.
Following the established pattern from feature 206, this feature uses hard-coded content to demonstrate
straightforward file creation within the Sheep workflow without external API dependencies.

The file is created with:
- Exact filename: test-ywcbdk.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size between 300-800 bytes
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
FILENAME = "test-ywcbdk.md"
FEATURE_NUMBER = 207
BRANCH_NAME = "feat/markdown-file-creation-94cf63"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME}"

# Hard-coded markdown content
# H1 title about cloud computing
TITLE_TEXT = "Cloud Computing Fundamentals"

# 2-3 sentences of prose content related to cloud computing
PROSE_CONTENT = (
    "Cloud computing has revolutionized how organizations deploy and manage their infrastructure "
    "by providing on-demand access to computing resources over the internet. This technology enables "
    "businesses to scale their operations dynamically while reducing capital expenditures on physical servers."
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
