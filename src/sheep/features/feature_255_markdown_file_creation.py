"""Implementation for feature 255: Create markdown file test-i3iccc.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern from
250+ prior implementations. The feature uses:
- LLM-based content generation via content_generators module
- pathlib.Path for file I/O with UTF-8 encoding and Unix LF line endings
- Comprehensive validation at each phase
- Standard git operations (add, commit, push)

The module implements phase 1 of 4: Content Generation & Validation
This phase focuses on:
1. Generating markdown content using LLM
2. Validating generated content meets format requirements

Subsequent phases (not in scope for this module):
3. File creation & disk validation
4. Git workflow integration and testing
"""

from sheep.content_generators import generate_markdown_content
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 255 constants
FILENAME = "test-i3iccc.md"
FEATURE_NUMBER = 255
BRANCH_NAME = "feat/255-markdown-file-creation-17ca12"
COMMIT_MESSAGE_TEMPLATE = f"feat({FEATURE_NUMBER}): create markdown file {FILENAME} with prose content"


def generate_content() -> str:
    """Generate markdown content with H1 heading and 2-3 sentences of prose.

    Uses the content_generators module to generate content via Claude API.
    The generated content will have:
    - H1 markdown heading on first line
    - Blank line separator on second line
    - 2-3 sentences of prose content starting on third line
    - Trailing newline (Unix convention)

    Returns:
        String containing valid markdown content that meets format requirements.

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        Exception: If LLM API call fails.
    """
    _logger.info("Generating markdown content with LLM")

    try:
        # Call content_generators module to generate markdown
        content = generate_markdown_content()

        _logger.debug(f"Generated {len(content)} bytes of markdown content")
        _logger.info("Markdown content generated successfully")
        return content

    except Exception as e:
        _logger.error(f"Failed to generate markdown content: {e}")
        raise


def validate_content(content: str) -> None:
    """Validate that generated markdown content meets format requirements.

    Checks that:
    1. Content is not empty
    2. First line is H1 heading (starts with "# ")
    3. Second line is blank (separator between heading and prose)
    4. Prose content has exactly 2-3 sentences (counted by periods)
    5. Content has trailing newline

    Args:
        content: The markdown content string to validate.

    Raises:
        ValueError: If content doesn't meet any format requirement.
    """
    _logger.info("Validating generated markdown content")

    if not content or not content.strip():
        raise ValueError("Generated content is empty")

    lines = content.split("\n")

    # Check for H1 heading on first line
    if not lines or not lines[0].startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")

    # Check for blank line on second line
    if len(lines) < 2 or lines[1] != "":
        raise ValueError("Second line must be blank (separator between heading and prose)")

    # Check prose content has 2-3 sentences
    prose_lines = lines[2:]
    prose_content = "\n".join(prose_lines).strip()

    if not prose_content:
        raise ValueError("No prose content found after heading and blank line")

    sentence_count = prose_content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(f"Content should have 2-3 sentences, found {sentence_count}")

    # Check for trailing newline
    if not content.endswith("\n"):
        raise ValueError("Content must end with trailing newline")

    _logger.info("Content validation passed")


def run() -> bool:
    """Main orchestration function for feature 255 phase 1.

    Coordinates content generation and validation:
    1. Generate markdown content using LLM
    2. Validate generated content meets all format requirements

    Returns:
        True on success.

    Raises:
        ValueError: If validation fails.
        Exception: If content generation fails.
    """
    _logger.info("Starting feature 255 phase 1: Content Generation & Validation")

    try:
        # Phase 1a: Generate content
        _logger.info("Phase 1a: Generating markdown content")
        content = generate_content()

        # Phase 1b: Validate content
        _logger.info("Phase 1b: Validating generated content")
        validate_content(content)

        _logger.info("✓ Feature 255 phase 1 completed successfully")
        return True

    except ValueError as e:
        _logger.error(f"Content validation failed: {e}")
        raise
    except Exception as e:
        _logger.error(f"Feature 255 phase 1 failed: {e}")
        raise


if __name__ == "__main__":
    run()
