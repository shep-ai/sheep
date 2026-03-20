#!/usr/bin/env python3
"""Create markdown file test-z4ucz3.md with manual prose content."""

from pathlib import Path
from sheep.content_generators import write_markdown_file, validate_markdown_file
from sheep.tools import GitCommitTool, GitPushTool
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


def create_markdown_file_manual():
    """
    Create test-z4ucz3.md with manually-written prose.

    This implementation follows the spec decision to use manual prose
    instead of LLM-generated content, since the user requested
    flexibility ("about anything") and manual prose aligns with the
    project's established pattern of 100+ test files.
    """
    filename = "test-z4ucz3.md"

    # Manual prose on a topic of interest
    prose = """# The Evolution of Programming Languages

Programming languages have evolved dramatically over the past seven decades, from machine code and assembly to high-level abstractions like Python and JavaScript that prioritize readability and developer productivity. This evolution reflects humanity's continuous effort to bridge the gap between human reasoning and machine instruction. Today's language design choices shape not only how we write software, but also what kinds of problems we can efficiently solve."""

    # Ensure trailing newline (Unix convention)
    if not prose.endswith("\n"):
        prose = prose + "\n"

    _logger.info(f"Creating markdown file: {filename}")
    _logger.debug(f"Prose length: {len(prose)} bytes")

    try:
        # Step 1: Write file using existing utility
        _logger.info("Step 1: Writing markdown file")
        filepath = write_markdown_file(prose, filename)
        _logger.info(f"File written: {filepath}")

        # Step 2: Validate file
        _logger.info("Step 2: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Step 3: Commit with exact message from spec
        _logger.info("Step 3: Committing markdown file")
        exact_message = "feat(123): Create markdown file test-z4ucz3.md with prose content"
        commit_tool = GitCommitTool()
        commit_result = commit_tool._run(
            repo_path=str(Path.cwd()),
            message=exact_message,
            add_all=True
        )
        _logger.info(f"Commit result: {commit_result}")

        # Step 4: Push to remote
        _logger.info("Step 4: Pushing to remote")
        push_tool = GitPushTool()
        push_result = push_tool._run(
            repo_path=str(Path.cwd()),
            remote="origin",
            set_upstream=True
        )
        _logger.info(f"Push result: {push_result}")

        _logger.info("Successfully created and published markdown file")
        return {
            "filepath": filepath,
            "commit_message": exact_message,
            "commit_result": commit_result,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


if __name__ == "__main__":
    result = create_markdown_file_manual()
    print(f"✓ File created: {result['filepath']}")
    print(f"✓ Committed: {result['commit_message']}")
    print(f"✓ Pushed to remote")
