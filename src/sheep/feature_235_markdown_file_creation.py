"""Feature 235: Create markdown file test-2k7sog.md with title and 2-3 sentences of content.

This module implements the workflow to create a single markdown file following
the established pattern from 230+ prior markdown-file-creation features.

Phase 1 Implementation:
- Create feature module that orchestrates existing helper functions
- Define the create_markdown_file_235() function
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

# Configuration for feature 235
FEATURE_NUMBER = 235
FILENAME = "test-2k7sog.md"


def create_markdown_file_235() -> dict[str, str]:
    """
    Execute complete workflow to create, validate, commit, and push a markdown file.

    Orchestrates the following steps:
    1. Generate markdown content (H1 heading + 2-3 sentences via LLM)
    2. Write markdown file to disk with UTF-8 encoding and LF line endings
    3. Validate the file meets all structural and encoding requirements
    4. Stage and commit with conventional commit message
    5. Push to remote with upstream tracking

    Returns:
        Dictionary with results:
        - filepath: Full path to the created file
        - content: The generated markdown content
        - commit_message: The git commit message used
        - push_result: The result from git push operation

    Raises:
        ValueError: If content or filename is invalid.
        IOError: If file operations fail.
        Exception: If LLM API call or git operations fail.
    """
    _logger.info(f"Feature {FEATURE_NUMBER}: Creating markdown file {FILENAME}")

    try:
        # Step 1: Generate markdown content
        _logger.info("Step 1: Generating markdown content")
        content = generate_markdown_content()
        _logger.debug(f"Generated {len(content)} bytes of markdown content")

        # Step 2: Write file to disk
        _logger.info("Step 2: Writing markdown file to disk")
        filepath = write_markdown_file(content, FILENAME)
        _logger.debug(f"File written to: {filepath}")

        # Step 3: Validate file
        _logger.info("Step 3: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Step 4: Commit file
        _logger.info("Step 4: Committing markdown file")
        commit_message = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with prose content"
        commit_result = commit_markdown_file(filepath, content, custom_message=commit_message)
        _logger.debug(f"Commit result: {commit_result}")

        # Step 5: Push to remote
        _logger.info("Step 5: Pushing to remote repository")
        push_result = push_markdown_file()
        _logger.debug(f"Push result: {push_result}")

        _logger.info(f"Feature {FEATURE_NUMBER}: Successfully created and published {FILENAME}")

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
    # Allow running this module directly for testing
    result = create_markdown_file_235()
    print(f"Success! Created file: {result['filepath']}")
    print(f"File contains {len(result['content'])} bytes of content")
    print(f"Commit message: {result['commit_message']}")
