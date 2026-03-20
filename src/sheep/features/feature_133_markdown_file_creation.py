"""Implementation for feature 133: Create markdown file test-az5jtn.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from 132 preceding features (001-132). The file is created with:
- Exact filename: test-az5jtn.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 400-600 bytes
- Git staging, commit, and push operations
"""

import time
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
FEATURE_NUMBER = 133
FEATURE_NAME = "markdown-file-creation-682344"
MARKDOWN_FILENAME = "test-az5jtn.md"


def _run_step_with_logging(step_name: str, step_func, *args, **kwargs):
    """
    Execute a step with structured logging for entry, exit, and error handling.

    Logs step entry with parameters, execution time, and step exit. If an exception
    occurs, logs the full error context and re-raises the exception.

    Args:
        step_name: Human-readable name of the step (e.g., "Generate markdown content")
        step_func: Callable function to execute
        *args: Positional arguments to pass to step_func
        **kwargs: Keyword arguments to pass to step_func

    Returns:
        The return value from step_func

    Raises:
        Re-raises any exception from step_func after logging error context
    """
    _logger.info(f"Starting: {step_name}")
    start_time = time.time()

    try:
        result = step_func(*args, **kwargs)
        duration = time.time() - start_time
        _logger.info(f"Completed: {step_name}", duration_seconds=duration)
        return result
    except Exception as e:
        duration = time.time() - start_time
        _logger.error(
            f"Failed: {step_name}",
            duration_seconds=duration,
            error_type=type(e).__name__,
            error_message=str(e),
        )
        raise


def create_feature_133_markdown_file(repo_path: str | None = None) -> dict[str, str]:
    """
    Create markdown file for feature 133.

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
        # Task 1: Generate valid markdown content
        content = _run_step_with_logging(
            "Generate markdown content",
            generate_markdown_content,
        )
        _logger.debug(f"Generated {len(content)} bytes of content")

        # Task 2: Write file to disk with proper encoding
        filepath = _run_step_with_logging(
            "Write markdown file to disk",
            write_markdown_file,
            content,
            MARKDOWN_FILENAME,
        )
        _logger.debug(f"File written to: {filepath}")

        # Task 3: Validate file meets all specification requirements
        _run_step_with_logging(
            "Validate markdown file",
            validate_markdown_file,
            filepath,
        )
        _logger.info("File validation passed")

        # Task 4: Stage and commit file with exact conventional message
        commit_message = f"feat({FEATURE_NUMBER}): Create markdown file {MARKDOWN_FILENAME} with prose content"
        _logger.debug(f"Using commit message: {commit_message}")
        commit_result = _run_step_with_logging(
            "Stage and commit file",
            commit_markdown_file,
            filepath,
            content,
            repo_path,
            commit_message,
        )
        _logger.debug(f"Commit result: {commit_result}")

        # Task 5: Push to remote repository
        push_result = _run_step_with_logging(
            "Push to remote repository",
            push_markdown_file,
            repo_path,
        )
        _logger.debug(f"Push result: {push_result}")

        _logger.info(
            f"Successfully created and published feature {FEATURE_NUMBER}: {MARKDOWN_FILENAME}"
        )

        return {
            "filepath": filepath,
            "content": content,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create feature {FEATURE_NUMBER}: {e}")
        raise


if __name__ == "__main__":
    """Execute feature 133 when run as a script."""
    result = create_feature_133_markdown_file()
    print("Feature 133 created successfully:")
    print(f"  File: {result['filepath']}")
    print(f"  Size: {len(result['content'])} bytes")
    print(f"  Message: {result['commit_message']}")
