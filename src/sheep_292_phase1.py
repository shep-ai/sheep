"""Feature 292 Phase 1: Content Generation and Validation.

This module provides utilities for generating and validating markdown content
with retry logic and comprehensive structural validation.

Phase 1 Implementation:
- Task 1: Generate markdown content (H1 heading + 2-3 sentences) with retry logic
- Task 2: Validate heading structure
- Task 3: Validate sentence count
- Task 4: Validate prose length and encoding
"""

import re
import time
from pathlib import Path

from sheep.config.llm import get_reasoning_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Prompt template for markdown generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following structure:
1. An H1 heading (using #) with a title about any topic you choose
2. A blank line
3. Exactly 2-3 sentences of coherent prose about that topic

Return ONLY the markdown content, no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""

# Regex patterns for validation
HEADING_PATTERN = r'^# ([^\n]+)$'
SENTENCE_BOUNDARY_PATTERN = r'[.!?]+'

# Constants for validation
PROSE_MIN_LENGTH = 100
PROSE_MAX_LENGTH = 300


def generate_markdown_content_with_retry(
    max_retries: int = 3, retry_delay: float = 1.0
) -> str:
    """
    Generate markdown content with H1 heading and 2-3 sentences using Claude API.

    Implements retry logic with exponential backoff for transient failures.
    Each retry doubles the delay: 1s, 2s, 4s, etc.

    Args:
        max_retries: Maximum number of retry attempts (default: 3).
        retry_delay: Initial delay in seconds for exponential backoff (default: 1.0).

    Returns:
        Generated markdown content as a string.

    Raises:
        ValueError: If content generation fails after max retries.
        Exception: If Claude API is unavailable.
    """
    llm = get_reasoning_llm()
    last_error = None

    for attempt in range(max_retries):
        try:
            _logger.info(f"Generating markdown content (attempt {attempt + 1}/{max_retries})")

            # Call Claude API with the prompt
            response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

            # Extract response text
            if isinstance(response, dict):
                content = str(response.get("content", str(response)))
            else:
                content = str(response)

            _logger.debug(f"Raw LLM response (first 100 chars): {content[:100]}...")

            # Validate the generated content
            validate_content(content)

            _logger.info("Successfully generated and validated markdown content")
            return content

        except (ValueError, Exception) as e:
            last_error = e
            _logger.warning(f"Content generation failed (attempt {attempt + 1}): {e}")

            # Calculate delay for next retry with exponential backoff
            if attempt < max_retries - 1:
                delay = retry_delay * (2 ** attempt)
                _logger.debug(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
            else:
                _logger.error(
                    f"Content generation failed after {max_retries} attempts: {last_error}"
                )

    # All retries exhausted
    raise ValueError(
        f"Failed to generate valid markdown content after {max_retries} attempts: {last_error}"
    )


def validate_heading(content: str) -> bool:
    """
    Validate that content contains exactly one markdown H1 heading.

    Checks for:
    - Content starts with "# " (H1 heading format)
    - Heading has a non-empty title
    - No higher-level headings (must be level 1, not level 2+)

    Args:
        content: The markdown content to validate.

    Returns:
        True if heading is valid.

    Raises:
        ValueError: If heading is missing, malformed, or wrong level.
    """
    if not content or not content.strip():
        raise ValueError("Content is empty")

    # Check for H1 heading at start
    lines = content.split("\n")
    if not lines[0].startswith("# "):
        raise ValueError("Content must start with H1 heading (format: # Title)")

    # Extract heading text and validate it's not empty
    match = re.match(HEADING_PATTERN, lines[0])
    if not match:
        raise ValueError(
            "Heading format invalid: must be '# ' followed by title (spaces matter)"
        )

    title = match.group(1).strip()
    if not title:
        raise ValueError("Heading title cannot be empty")

    _logger.debug(f"Valid heading found: {lines[0]}")
    return True


def validate_sentence_count(prose: str) -> bool:
    """
    Validate that prose contains exactly 2-3 sentences.

    Detects sentence boundaries using . ! ? punctuation.
    Multiple punctuation marks (e.g., ?! or ...) count as single boundary.

    Args:
        prose: The prose content to validate (without heading).

    Returns:
        True if sentence count is exactly 2 or 3.

    Raises:
        ValueError: If sentence count is outside 2-3 range.
    """
    if not prose or not prose.strip():
        raise ValueError("Prose content is empty")

    # Find all sentence boundaries (., !, ?)
    # Split on sentence boundaries and count
    sentences = re.split(SENTENCE_BOUNDARY_PATTERN, prose.strip())
    # Filter out empty strings from the split
    sentences = [s.strip() for s in sentences if s.strip()]

    sentence_count = len(sentences)

    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"Prose must contain exactly 2-3 sentences, found {sentence_count}"
        )

    _logger.debug(f"Valid sentence count: {sentence_count}")
    return True


def validate_prose_length(
    prose: str, min_length: int = PROSE_MIN_LENGTH, max_length: int = PROSE_MAX_LENGTH
) -> bool:
    """
    Validate that prose length is within acceptable range.

    Args:
        prose: The prose content to validate.
        min_length: Minimum prose length in characters (default: 100).
        max_length: Maximum prose length in characters (default: 300).

    Returns:
        True if prose length is within range.

    Raises:
        ValueError: If prose length is outside specified range.
    """
    prose_len = len(prose.strip())

    if prose_len < min_length:
        raise ValueError(f"Prose too short: {prose_len} chars (minimum {min_length})")

    if prose_len > max_length:
        raise ValueError(f"Prose too long: {prose_len} chars (maximum {max_length})")

    _logger.debug(f"Valid prose length: {prose_len} chars")
    return True


def validate_utf8_encoding(content: str) -> bool:
    """
    Validate that content is valid UTF-8 without BOM.

    Args:
        content: The content to validate.

    Returns:
        True if content is valid UTF-8 without BOM.

    Raises:
        ValueError: If content has invalid encoding or BOM.
    """
    try:
        # Try to encode and decode to verify UTF-8 validity
        content.encode("utf-8").decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"Content contains invalid UTF-8: {e}")

    # Check for UTF-8 BOM
    content_bytes = content.encode("utf-8")
    if content_bytes.startswith(b"\xef\xbb\xbf"):
        raise ValueError("Content has UTF-8 BOM (must be UTF-8 without BOM)")

    _logger.debug("Valid UTF-8 encoding (no BOM)")
    return True


def validate_content(content: str) -> bool:
    """
    Validate complete markdown content against all requirements.

    Performs comprehensive validation:
    1. Validates heading structure (H1 format, non-empty title)
    2. Validates sentence count (exactly 2-3)
    3. Validates prose length (100-300 characters)
    4. Validates UTF-8 encoding (no BOM)
    5. Validates blank line separator between heading and prose

    Args:
        content: The markdown content to validate.

    Returns:
        True if all validations pass.

    Raises:
        ValueError: If any validation fails with descriptive message.
    """
    if not content or not content.strip():
        raise ValueError("Content is empty")

    # Validate UTF-8 encoding first (fail fast)
    validate_utf8_encoding(content)

    # Validate heading
    validate_heading(content)

    # Extract prose (after heading and blank line)
    lines = content.split("\n")

    # Check for blank line separator
    if len(lines) < 2 or lines[1] != "":
        raise ValueError(
            "Content structure invalid: must have blank line after heading"
        )

    # Get prose lines (skip heading and blank line)
    prose_lines = lines[2:]

    # Remove trailing empty lines for prose extraction
    while prose_lines and prose_lines[-1] == "":
        prose_lines.pop()

    if not prose_lines:
        raise ValueError("No prose content found after heading")

    prose = "\n".join(prose_lines).strip()

    # Validate sentence count first (more specific error)
    validate_sentence_count(prose)

    # Validate prose length
    validate_prose_length(prose)

    _logger.info("Content validation passed: all checks successful")
    return True
