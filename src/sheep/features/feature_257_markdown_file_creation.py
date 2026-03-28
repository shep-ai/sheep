"""Implementation for feature 257: Create markdown file test-fl139g.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 256 preceding features (001-256). The file is created with:
- Exact filename: test-fl139g.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 250-600 bytes
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
FEATURE_NUMBER = 257
FEATURE_NAME = "markdown-file-creation-ef4e6e"
MARKDOWN_FILENAME = "test-fl139g.md"


def create_feature_257_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 257.

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

    content = None
    filepath = None
    commit_message = None
    push_result = None

    try:
        # Task 1: Generate valid markdown content
        _logger.info("Task 1: Generating markdown content")
        try:
            content = generate_markdown_content()
            _logger.debug(f"Generated {len(content)} bytes of content")
        except Exception as e:
            _logger.error(
                f"Task 1 failed (API/content generation): {type(e).__name__}: {e}"
            )
            raise

        # Task 2: Write file to disk with proper encoding
        _logger.info("Task 2: Writing markdown file to disk")
        try:
            filepath = write_markdown_file(content, MARKDOWN_FILENAME)
            _logger.debug(f"File written to: {filepath}")
        except Exception as e:
            _logger.error(f"Task 2 failed (file I/O): {type(e).__name__}: {e}")
            raise

        # Task 3: Validate file meets all specification requirements
        _logger.info("Task 3: Validating markdown file")
        try:
            validate_markdown_file(filepath)
            _logger.info("File validation passed")
        except Exception as e:
            _logger.error(
                f"Task 3 failed (file validation): {type(e).__name__}: {e}"
            )
            raise

        # Task 4: Stage and commit file with exact conventional message
        _logger.info("Task 4: Staging and committing file")
        try:
            commit_message = f"feat({FEATURE_NUMBER}): create markdown file {MARKDOWN_FILENAME} with prose content"
            _logger.debug(f"Using commit message: {commit_message}")
            commit_result = commit_markdown_file(
                filepath, content, repo_path, custom_message=commit_message
            )
            _logger.debug(f"Commit result: {commit_result}")
        except Exception as e:
            _logger.error(f"Task 4 failed (git commit): {type(e).__name__}: {e}")
            raise

        # Task 5: Push to remote repository
        _logger.info("Task 5: Pushing to remote repository")
        try:
            push_result = push_markdown_file(repo_path)
            _logger.debug(f"Push result: {push_result}")
        except Exception as e:
            _logger.error(f"Task 5 failed (git push): {type(e).__name__}: {e}")
            raise

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": str(filepath),
            "content": content,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(
            f"Feature {FEATURE_NUMBER} workflow failed: {type(e).__name__}: {e}"
        )
        raise


if __name__ == "__main__":
    """Execute feature 257 when run as a script."""
    try:
        result = create_feature_257_markdown_file()
        _logger.info("Feature 257 execution completed successfully")
        print("\nFeature 257 created successfully:")
        print(f"  File: {result['filepath']}")
        print(f"  Size: {len(result['content'])} bytes")
        print(f"  Message: {result['commit_message']}")
        print(f"  Push result: {result['push_result']}")
    except Exception as e:
        _logger.error(f"Feature 257 execution failed: {type(e).__name__}: {e}")
        print(f"\nFeature 257 failed: {e}", file=__import__("sys").stderr)
        raise
