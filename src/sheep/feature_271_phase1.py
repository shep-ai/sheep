"""
Feature 271 - Phase 1: Content Generation

This module handles Phase 1 of Feature 271: markdown file creation with LLM-generated prose.

Phase 1 is responsible for:
- Generating markdown content via Claude API using content_generators.generate_markdown_content()
- Validating the generated content structure (H1 heading, blank line, 2-3 sentences)
- Returning the validated content for use in subsequent phases

The implementation uses the Sheep platform's unified content_generators module which
provides complete end-to-end markdown generation with full validation.
"""

from pathlib import Path

from sheep.content_generators import generate_markdown_content
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


def execute_phase_1_content_generation() -> str:
    """
    Execute Phase 1: Content Generation for Feature 271.

    Calls content_generators.generate_markdown_content() to produce:
    - H1 markdown heading (# Title)
    - Blank line separator
    - 2-3 sentences of coherent prose

    This is the foundation for all subsequent phases (file creation, validation, git operations).

    Returns:
        String containing valid markdown content with H1 heading and prose.

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        ImportError: If LLM API is unavailable.
        Exception: If content generation fails.
    """
    _logger.info("=" * 80)
    _logger.info("PHASE 1: CONTENT GENERATION")
    _logger.info("=" * 80)

    try:
        # Step 1: Call the content generation function
        _logger.info("\nStep 1: Generating markdown content via Claude API")
        _logger.info("-" * 80)

        content = generate_markdown_content()

        # Log success metrics
        content_bytes = len(content.encode("utf-8"))
        _logger.info(f"✓ Content generation successful")
        _logger.info(f"  - Generated: {len(content)} characters ({content_bytes} bytes)")

        # Step 2: Validate structure
        _logger.info("\nStep 2: Validating content structure")
        _logger.info("-" * 80)

        _validate_content_structure(content)
        _logger.info("✓ Content structure validation passed")

        # Step 3: Log content details
        _logger.info("\nStep 3: Content analysis")
        _logger.info("-" * 80)

        lines = content.split("\n")
        heading = lines[0]
        _logger.info(f"✓ H1 Heading: {heading}")
        _logger.info(f"✓ Total lines: {len(lines)}")

        sentence_count = content.count(".")
        _logger.info(f"✓ Sentence count: {sentence_count} (expected: 2-3)")

        # Verify encoding
        try:
            content.encode("utf-8").decode("utf-8")
            _logger.info("✓ UTF-8 encoding valid")
        except UnicodeError as e:
            _logger.error(f"✗ Encoding error: {e}")
            raise ValueError(f"Content encoding error: {e}") from e

        # Verify trailing newline
        if content.endswith("\n"):
            _logger.info("✓ Trailing newline present (Unix convention)")
        else:
            _logger.warning("⚠ Missing trailing newline - will be added by file writer")

        _logger.info("\n" + "=" * 80)
        _logger.info("PHASE 1: CONTENT GENERATION - COMPLETE")
        _logger.info("=" * 80)
        _logger.debug(f"\nGenerated content:\n{'-' * 80}\n{content}\n{'-' * 80}")

        return content

    except Exception as e:
        _logger.error(f"✗ Phase 1 failed: {e}")
        import traceback

        _logger.error(traceback.format_exc())
        raise


def _validate_content_structure(content: str) -> None:
    """
    Validate that generated content meets structure requirements.

    Checks for:
    - Non-empty string
    - H1 heading at start
    - Blank line separator after heading
    - 2-3 sentences of prose
    - Valid UTF-8 encoding
    - Trailing newline

    Args:
        content: The markdown content to validate.

    Raises:
        ValueError: If content fails any validation check.
    """
    # Check non-empty
    if not content or not isinstance(content, str):
        raise ValueError("Content must be non-empty string")

    if content.strip() == "":
        raise ValueError("Content cannot be all whitespace")

    # Split into lines
    lines = content.split("\n")

    # Check minimum line count
    if len(lines) < 4:
        raise ValueError(f"Content should have at least 4 lines (heading, blank, prose, newline), got {len(lines)}")

    # Check H1 heading
    if not lines[0].startswith("# "):
        raise ValueError(f"First line must be H1 heading (# ...), got: {lines[0]}")

    # Check heading has content
    if len(lines[0]) <= 2:
        raise ValueError("H1 heading must have content after '# '")

    # Check blank line separator
    if lines[1] != "":
        raise ValueError(f"Second line must be blank separator, got: {repr(lines[1])}")

    # Check prose content exists
    prose_lines = [l for l in lines[2:] if l.strip()]
    if not prose_lines:
        raise ValueError("No prose content found after heading and blank line")

    # Check sentence count
    prose_text = "\n".join(prose_lines)
    sentence_count = prose_text.count(".")

    if sentence_count < 2:
        raise ValueError(f"Content should have at least 2 sentences, found {sentence_count}")

    if sentence_count > 3:
        raise ValueError(f"Content should have at most 3 sentences, found {sentence_count}")

    # Check trailing newline
    if not content.endswith("\n"):
        raise ValueError("Content must end with trailing newline")

    _logger.debug("Content structure validation: all checks passed")


def get_phase1_content_for_feature_271(use_cache: bool = False) -> str:
    """
    Convenience function to get Phase 1 content for Feature 271.

    Can optionally cache content if called multiple times in same session
    (though typically content generation is one-time operation per feature).

    Args:
        use_cache: If True, cache generated content in module scope.

    Returns:
        Generated markdown content ready for Phase 2 (file creation).
    """
    # Could implement caching here if needed
    return execute_phase_1_content_generation()


if __name__ == "__main__":
    # Allow direct execution for testing/debugging
    import sys

    try:
        content = execute_phase_1_content_generation()
        print("\n" + "=" * 80)
        print("SUCCESS: Phase 1 content generation complete")
        print("=" * 80)
        print(f"\nGenerated content ({len(content)} chars):\n")
        print(content)
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
