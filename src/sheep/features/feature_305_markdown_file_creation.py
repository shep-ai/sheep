"""Implementation for feature 305: Create markdown file test-evp6mu.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 300+ preceding features (001-304). The file is created with:
- Exact filename: test-evp6mu.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
- Git staging, commit, and push operations
"""

from pathlib import Path

from sheep.content_generators import create_markdown_file
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 305
FEATURE_NAME = "markdown-file-creation-209cc3"
MARKDOWN_FILENAME = "test-evp6mu.md"


def create_feature_305_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 305.

    Orchestrates the complete workflow:
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
        # Call orchestration function from content_generators
        result = create_markdown_file(
            filename=MARKDOWN_FILENAME, repo_path=repo_path, feature_number=FEATURE_NUMBER
        )

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return result

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


def main() -> int:
    """
    Execute feature 305 as a standalone task.

    Returns:
        0 on success, 1 on failure.
    """
    try:
        result = create_feature_305_markdown_file()
        _logger.info(f"Feature {FEATURE_NUMBER} completed successfully")
        print("Feature 305 created successfully:")
        print(f"  File: {result['filepath']}")
        print(f"  Size: {len(result['content'])} bytes")
        print(f"  Message: {result['commit_message']}")
        return 0
    except Exception as e:
        _logger.error(f"Feature {FEATURE_NUMBER} failed: {e}")
        print(f"Error: Failed to create feature {FEATURE_NUMBER}: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
