"""Implementation for feature 305: Create markdown file test-9s145k.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 304 preceding features (001-304). The file is created with:
- Exact filename: test-9s145k.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 250-600 bytes
- Git staging, commit, and push operations
"""

from pathlib import Path

from sheep.content_generators import create_markdown_file
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 305
FEATURE_NAME = "markdown-file-creation-e9500c"
MARKDOWN_FILENAME = "test-9s145k.md"


def create_feature_305_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 305.

    Orchestrates the complete workflow through the existing create_markdown_file()
    utility which handles:
    1. Generate valid markdown content (H1 heading + 2-3 sentences)
    2. Write file to repository root with UTF-8 encoding
    3. Validate file meets all specification requirements
    4. Stage and commit with conventional message
    5. Push to remote feature branch

    Args:
        repo_path: Path to git repository (defaults to current directory).

    Returns:
        Dictionary containing:
        - filepath: Full path to created file
        - content: Markdown content
        - commit_message: Git commit message used
        - push_result: Result from git push

    Raises:
        ValueError: If content or file is invalid
        IOError: If file operations fail
        Exception: If git operations fail
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    _logger.info(
        f"Creating feature {FEATURE_NUMBER} markdown file: {MARKDOWN_FILENAME}"
    )

    try:
        result = create_markdown_file(MARKDOWN_FILENAME, repo_path, feature_number=FEATURE_NUMBER)
        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )
        return result

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


if __name__ == "__main__":
    """Execute feature 305 when run as a script."""
    result = create_feature_305_markdown_file()
    print("Feature 305 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
