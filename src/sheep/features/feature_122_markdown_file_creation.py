"""Implementation for feature 122: Create markdown file test-duijn0.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 120 preceding features (001-121). The file is created with:
- Exact filename: test-duijn0.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations
"""

from pathlib import Path

from sheep.content_generators import (
    commit_markdown_file,
    generate_markdown_content,
    push_markdown_file,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 122
FEATURE_NAME = "markdown-file-creation-42732e"
MARKDOWN_FILENAME = "test-duijn0.md"


def create_markdown_file_feature(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 122.

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
    _logger.info(f"Starting feature {FEATURE_NUMBER} implementation")

    try:
        # Task-2: Generate markdown content
        _logger.debug("Task-2: Generating markdown content")
        content = generate_markdown_content()
        _logger.info(f"Generated content: {len(content)} bytes")
        _logger.debug(f"Content preview: {content[:80].rstrip()}...")

        # Task-3: Write file to disk
        _logger.debug("Task-3: Writing markdown file to disk")
        filepath = write_markdown_file(content, MARKDOWN_FILENAME)
        _logger.info(f"File created: {filepath}")

        # Task-4: Validate file
        _logger.debug("Task-4: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Task-5: Commit file
        _logger.debug("Task-5: Committing markdown file")
        commit_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
        commit_result = commit_markdown_file(
            filepath, content, repo_path, custom_message=commit_message
        )
        _logger.info(f"File committed with message: {commit_message}")

        # Task-5 (continued): Push to remote
        _logger.debug("Task-5 (continued): Pushing to remote")
        push_result = push_markdown_file(repo_path)
        _logger.info("File pushed to remote")

        _logger.info(f"Feature {FEATURE_NUMBER} completed successfully")
        return {
            "filepath": filepath,
            "content": content,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Feature {FEATURE_NUMBER} failed: {e}")
        raise


if __name__ == "__main__":
    """Execute feature 122 when run as a script."""
    result = create_markdown_file_feature()
    print("Feature 122 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
