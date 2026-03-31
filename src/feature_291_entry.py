"""Entry point for feature 291: Markdown file creation (test-6sw4o8.md).

This module provides the entry point function for feature 291, which orchestrates
the creation of a markdown test file with a title and prose content.

The implementation delegates all functionality to the proven create_markdown_file()
orchestration function from sheep.content_generators, following the established
pattern from 290+ preceding identical features.
"""

from sheep.content_generators import create_markdown_file


def create_feature_291_markdown() -> dict[str, str]:
    """
    Create markdown file test-6sw4o8.md with H1 heading and prose content.

    Entry point for feature 291 that orchestrates the complete workflow:
    1. Generate markdown content with H1 heading and 2-3 sentences of prose
    2. Write file to repository root as test-6sw4o8.md
    3. Validate file structure, encoding, and line endings
    4. Commit with conventional commit message: feat(291): ...
    5. Push to remote with upstream tracking

    This function requires no parameters and delegates all operations to the
    proven create_markdown_file() orchestration function from sheep.content_generators.

    Returns:
        Dictionary with keys:
        - filepath: Full path to created file
        - content: The markdown content
        - commit_message: The git commit message used
        - push_result: The result from git push operation

    Raises:
        ValueError: If filename or content is invalid
        IOError: If file operations fail
        Exception: If git operations or LLM API fails
    """
    return create_markdown_file(filename="test-6sw4o8.md", feature_number=291)
