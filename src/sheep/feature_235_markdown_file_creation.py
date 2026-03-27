"""Feature 235: Create markdown file test-2k7sog.md with title and 2-3 sentences of content.

This module implements the workflow to create a single markdown file following
the established pattern from 230+ prior markdown-file-creation features.

Phase 1 Implementation:
- Create feature module that orchestrates existing helper functions
- Define the create_markdown_file_235() function
"""

import os
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

# Fallback content for when LLM API is not available
# Must use LF line endings (not CRLF) - critical for validation on Windows
FALLBACK_CONTENT = "# The Art of Persistent Learning\n\nContinuous learning is the foundation of personal and professional growth in today's rapidly evolving world. By dedicating time to understanding new concepts and practicing new skills, individuals develop resilience and adaptability that serve them across all aspects of life. The commitment to lifelong learning opens doors to opportunities, deepens understanding, and contributes meaningfully to society.\n"


def _generate_content_with_fallback() -> str:
    """
    Generate markdown content, falling back to hardcoded content if ANTHROPIC_API_KEY is not set.

    Returns:
        String containing valid markdown with H1 heading and prose content.
    """
    # Check if ANTHROPIC_API_KEY is available
    if not os.environ.get("ANTHROPIC_API_KEY"):
        _logger.info("ANTHROPIC_API_KEY not set, using fallback content for demonstration")
        return FALLBACK_CONTENT

    # Use LLM generation if API key is available
    try:
        _logger.info("Attempting LLM-based content generation")
        content = generate_markdown_content()
        _logger.info("LLM content generation succeeded")
        return content
    except Exception as e:
        # If API key exists but generation still fails, propagate the error
        _logger.error(f"LLM generation failed: {e}")
        raise


def create_markdown_file_235() -> dict[str, str]:
    """
    Execute complete workflow to create, validate, commit, and push a markdown file.

    Orchestrates the following steps:
    1. Generate markdown content (H1 heading + 2-3 sentences via LLM or fallback)
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
        Exception: If git operations fail.
    """
    _logger.info(f"Feature {FEATURE_NUMBER}: Creating markdown file {FILENAME}")

    try:
        # Step 1: Generate markdown content
        _logger.info("Step 1: Generating markdown content")
        content = _generate_content_with_fallback()
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
