"""Feature 123: Create markdown file test-b3x0s1.md with title and 2-3 sentences of content.

This module implements the workflow to create a single markdown file following
the established pattern from 122+ prior markdown-file-creation features.

Phase 1 Implementation:
- Module foundation: Constants, imports, and module structure
Phase 2 Implementation:
- Task 2: Generate markdown content (H1 heading + 2-3 sentences)
- Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings
"""

from pathlib import Path

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
    commit_markdown_file,
    push_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Configuration for feature 123
FEATURE_NUMBER = 123
FILENAME = "test-b3x0s1.md"


def task_2_generate_markdown_content() -> str:
    """
    Task 2: Generate markdown content with H1 heading and 2-3 sentences.

    This task calls the existing generate_markdown_content() function which:
    - Uses the CrewAI LLM framework to generate coherent prose
    - Returns markdown with H1 heading about an implementer-chosen topic
    - Ensures 2-3 sentences of prose content
    - Adds trailing newline for Unix convention

    Returns:
        String containing valid markdown (H1 heading + blank line + 2-3 sentences).

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        Exception: If LLM API call fails.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 2: Generating markdown content")

    try:
        # Call the existing generate_markdown_content function
        content = generate_markdown_content()

        # Validate sentence count (hard requirement: must be 2-3 sentences)
        sentence_count = content.count(".")
        if sentence_count < 2 or sentence_count > 3:
            raise ValueError(
                f"Content validation failed: expected 2-3 sentences, found {sentence_count}"
            )

        _logger.info(
            f"Task 2 complete: Generated {len(content)} bytes of markdown content "
            f"with {sentence_count} sentences"
        )
        return content

    except Exception as e:
        _logger.error(f"Task 2 failed: {e}")
        raise


def task_3_write_markdown_file_to_disk(content: str) -> str:
    """
    Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings.

    This task calls the existing write_markdown_file() function which:
    - Persists markdown content to test-b3x0s1.md in repository root
    - Uses UTF-8 encoding without BOM
    - Ensures Unix-style LF line endings (not CRLF)
    - Validates file was created successfully

    Args:
        content: The markdown content to write (from task 2).

    Returns:
        Full path to the created file.

    Raises:
        ValueError: If content is invalid or filename is unsafe.
        IOError: If file write operation fails.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Task 3: Writing markdown file to disk")

    try:
        # Check that file does not already exist (fail-fast on conflicts)
        repo_root = Path.cwd()
        file_path = repo_root / FILENAME
        if file_path.exists():
            raise ValueError(f"File already exists: {FILENAME}")

        # Call the existing write_markdown_file function
        filepath = write_markdown_file(content, FILENAME)

        _logger.info(
            f"Task 3 complete: Wrote markdown file to {filepath} "
            f"({Path(filepath).stat().st_size} bytes)"
        )
        return filepath

    except Exception as e:
        _logger.error(f"Task 3 failed: {e}")
        raise


def main() -> dict[str, str]:
    """
    Execute phase 2 implementation: Content Generation & Validation.

    This function orchestrates the two tasks:
    - Task 2: Generate markdown content
    - Task 3: Write to disk

    Returns:
        Dictionary with results:
        - content: The generated markdown content
        - filepath: Full path to the created file

    Raises:
        Any exceptions from task 2 or task 3 are propagated to the caller.
    """
    _logger.info(f"Feature {FEATURE_NUMBER} - Phase 2: Content Generation & Validation")

    try:
        # Execute task 2: Generate markdown content
        content = task_2_generate_markdown_content()

        # Execute task 3: Write markdown file to disk
        filepath = task_3_write_markdown_file_to_disk(content)

        _logger.info(f"Feature {FEATURE_NUMBER} - Phase 2 complete")

        return {
            "content": content,
            "filepath": filepath,
        }

    except Exception as e:
        _logger.error(f"Feature {FEATURE_NUMBER} - Phase 2 failed: {e}")
        raise


if __name__ == "__main__":
    # Allow running this module directly for testing
    result = main()
    print(f"Success! Created file: {result['filepath']}")
    print(f"File contains {len(result['content'])} bytes of content")
