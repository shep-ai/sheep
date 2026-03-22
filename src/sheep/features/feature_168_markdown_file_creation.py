"""Implementation for feature 168: Create markdown file test-oyiqcz.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 167 preceding features (001-167). The file is created with:
- Exact filename: test-oyiqcz.md
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
FEATURE_NUMBER = 168
MARKDOWN_FILENAME = "test-oyiqcz.md"
COMMIT_MESSAGE = "feat(168): Create markdown file test-oyiqcz.md with prose content"


def create_feature_168_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 168 with content generation retry logic.

    Orchestrates the complete workflow:
    1. Generate valid markdown content (H1 heading + 2-3 sentences) with retry logic
       - Retries up to 2 times on validation failure (3 total attempts)
    2. Write file to repository root with UTF-8 encoding
    3. Validate file size meets specification (300-600 bytes)
    4. Validate file meets all other specification requirements
    5. Stage and commit with conventional message
    6. Push to remote feature branch

    Args:
        repo_path: Path to git repository (defaults to current directory).

    Returns:
        Dictionary containing:
        - filepath: Full path to created file
        - content: Markdown content
        - commit_message: Git commit message used
        - push_result: Result from git push

    Raises:
        ValueError: If content or file is invalid after all retries
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

    try:
        # Task 1: Generate valid markdown content with retry logic
        _logger.info("Task 1: Generating markdown content (with retry logic)")
        for attempt in range(1, 4):  # 1 initial attempt + 2 retries = 3 total
            try:
                _logger.debug(f"Attempt {attempt}/3: Generating markdown content...")
                content = generate_markdown_content()
                _logger.info(f"Content generation succeeded on attempt {attempt}/3")
                _logger.debug(f"Generated {len(content)} bytes of content")
                break  # Success, exit retry loop
            except ValueError as e:
                if attempt == 3:  # Last attempt
                    _logger.error(
                        f"Content validation failed after 3 attempts: {e}"
                    )
                    raise
                _logger.warning(
                    f"Attempt {attempt}/3 failed: {e}. Retrying..."
                )

        # Task 2: Write file to disk with proper encoding
        _logger.info("Task 2: Writing markdown file to disk")
        filepath = write_markdown_file(content, MARKDOWN_FILENAME)
        _logger.debug(f"File written to: {filepath}")

        # Task 3: Validate file size (300-600 bytes)
        _logger.info("Task 3: Validating file size specification")
        file_path_obj = Path(filepath)
        file_size = file_path_obj.stat().st_size
        _logger.debug(f"File size: {file_size} bytes")
        if not (300 <= file_size <= 600):
            _logger.error(
                f"File size {file_size} bytes is outside 300-600 range"
            )
            # Delete the file before raising exception
            file_path_obj.unlink(missing_ok=True)
            _logger.debug(f"Deleted oversized file: {filepath}")
            raise ValueError(
                f"File size {file_size} bytes is outside 300-600 range"
            )
        _logger.info("File size validation passed")

        # Task 4: Validate file meets all specification requirements
        _logger.info("Task 4: Validating markdown file properties")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Task 5: Stage and commit file with exact conventional message
        _logger.info("Task 5: Staging and committing file")
        _logger.debug(f"Using commit message: {COMMIT_MESSAGE}")
        commit_result = commit_markdown_file(
            filepath, content, repo_path, custom_message=COMMIT_MESSAGE
        )
        _logger.debug(f"Commit result: {commit_result}")

        # Task 6: Push to remote repository
        _logger.info("Task 6: Pushing to remote repository")
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
    """Execute feature 168 when run as a script."""
    result = create_feature_168_markdown_file()
    print("Feature 168 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
