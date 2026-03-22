"""Implementation for feature 158: Create markdown file test-p2qj1z.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 157 preceding features (001-157). The file is created with:
- Exact filename: test-p2qj1z.md
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
    push_markdown_file,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature metadata
FEATURE_NUMBER = 158
MARKDOWN_FILENAME = "test-p2qj1z.md"
COMMIT_MESSAGE = "feat(158): Create markdown file test-p2qj1z.md with prose content"

# Hard-coded prose content following the spec requirement for no external dependencies
MARKDOWN_CONTENT = """# The Power of Continuous Learning

Continuous learning is essential for personal and professional growth in a rapidly changing world. It expands our knowledge, sharpens our skills, and opens new opportunities for advancement and success. By embracing learning as a lifelong practice, we become more adaptable and capable of facing whatever challenges come our way."""


def create_feature_158_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 158.

    Orchestrates the complete workflow:
    1. Use hard-coded markdown content (H1 heading + 2-3 sentences)
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
        # Use hard-coded content (no LLM generation)
        content = MARKDOWN_CONTENT + "\n"
        _logger.info(f"Using hard-coded markdown content ({len(content)} bytes)")

        # Task 1: Write file to disk with proper encoding
        _logger.info("Task 1: Writing markdown file to disk")
        filepath = write_markdown_file(content, MARKDOWN_FILENAME)
        _logger.debug(f"File written to: {filepath}")

        # Task 2: Validate file meets all specification requirements
        _logger.info("Task 2: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Task 3: Stage and commit file with exact conventional message
        _logger.info("Task 3: Staging and committing file")
        _logger.debug(f"Using commit message: {COMMIT_MESSAGE}")
        commit_result = commit_markdown_file(
            filepath, content, repo_path, custom_message=COMMIT_MESSAGE
        )
        _logger.debug(f"Commit result: {commit_result}")

        # Task 4: Push to remote repository
        _logger.info("Task 4: Pushing to remote repository")
        push_result = push_markdown_file(repo_path)
        _logger.debug(f"Push result: {push_result}")

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": filepath,
            "content": content,
            "commit_message": COMMIT_MESSAGE,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


if __name__ == "__main__":
    """Execute feature 158 when run as a script."""
    result = create_feature_158_markdown_file()
    print("Feature 158 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
