#!/usr/bin/env python3
"""
Content generation and validation for markdown file creation (Feature 199).

This module provides utilities for:
1. Generating markdown content using Claude API with AI-generated prose
2. Validating generated content against quality requirements
3. Retrying failed content generation with exponential backoff
"""

import re
import time
from typing import Optional

from sheep.config.llm import get_reasoning_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Prompt template for markdown content generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a new topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""

# Regex pattern for sentence boundary detection
# Matches sentences ending with period, question mark, or exclamation mark
SENTENCE_BOUNDARY_PATTERN = r'[.!?]\s+'


def generate_markdown_content(max_retries: int = 3, retry_delay: float = 1.0) -> dict[str, str]:
    """
    Generate markdown content with H1 heading and 2-3 sentences of prose using Claude API.

    Uses the Claude reasoning LLM to generate unique, coherent prose that is thematically
    related to the title. Implements retry logic with exponential backoff for API failures.

    Args:
        max_retries: Maximum number of retry attempts for API calls (default: 3).
        retry_delay: Initial delay in seconds for exponential backoff (default: 1.0).

    Returns:
        Dictionary with keys:
        - 'title': The H1 heading text (without # prefix)
        - 'prose': The 2-3 sentences of prose content
        - 'full_content': The complete markdown including heading

    Raises:
        ValueError: If content generation fails after retries or content is invalid.
        Exception: If Claude API is unavailable or authentication fails.
    """
    llm = get_reasoning_llm()

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
            validation_result = validate_content(content)
            if not validation_result['is_valid']:
                raise ValueError(f"Content validation failed: {validation_result['errors']}")

            # Parse the content into title and prose
            title, prose = _parse_markdown_content(content)

            _logger.info(f"Successfully generated markdown content with title: '{title}'")
            return {
                'title': title,
                'prose': prose,
                'full_content': content,
            }

        except ValueError as e:
            # Validation or parsing error - retry with backoff
            _logger.warning(f"Content generation failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                delay = retry_delay * (2 ** attempt)  # Exponential backoff
                _logger.debug(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
            else:
                raise ValueError(f"Failed to generate valid markdown after {max_retries} attempts: {e}")

        except Exception as e:
            # API or authentication error - don't retry on non-validation errors
            _logger.error(f"Claude API error: {e}")
            raise ValueError(f"Claude API call failed: {e}")

    raise ValueError(f"Failed to generate markdown after {max_retries} attempts")


def validate_content(content: str) -> dict[str, any]:
    """
    Validate generated markdown content against quality requirements.

    Checks for:
    - Content is not empty
    - Starts with H1 heading (# )
    - Contains exactly 2-3 sentences
    - Reasonable length (100-300 characters for prose)
    - Valid UTF-8 encoding

    Args:
        content: The markdown content to validate.

    Returns:
        Dictionary with keys:
        - 'is_valid': Boolean indicating if content passes all validations
        - 'errors': List of validation errors (empty if valid)
        - 'details': Dict with validation details (sentence_count, prose_length, etc.)
    """
    errors = []
    details = {
        'content_length': len(content),
        'sentence_count': 0,
        'prose_length': 0,
        'has_h1_heading': False,
        'starts_with_h1': False,
    }

    # Check content is not empty
    if not content or not content.strip():
        errors.append("Generated content is empty")
        return {'is_valid': False, 'errors': errors, 'details': details}

    # Check for H1 heading (# prefix)
    if not content.lstrip().startswith("# "):
        errors.append("Content must start with H1 heading (format: # Title)")
        return {'is_valid': False, 'errors': errors, 'details': details}

    details['starts_with_h1'] = True

    # Extract title and prose
    lines = content.strip().split('\n')
    if not lines[0].startswith("# "):
        errors.append("First line must be H1 heading")
        return {'is_valid': False, 'errors': errors, 'details': details}

    details['has_h1_heading'] = True
    title = lines[0][2:].strip()

    # Check for blank line separator (if multiple lines)
    if len(lines) > 1 and lines[1] != '':
        errors.append("Second line must be blank (separator between heading and prose)")
        return {'is_valid': False, 'errors': errors, 'details': details}

    # Get prose content (skip heading and blank line)
    prose_start_idx = 2 if len(lines) > 2 else 1
    prose_lines = lines[prose_start_idx:]

    # Remove trailing empty lines
    while prose_lines and prose_lines[-1].strip() == '':
        prose_lines.pop()

    if not prose_lines:
        errors.append("No prose content found after heading")
        return {'is_valid': False, 'errors': errors, 'details': details}

    prose = '\n'.join(prose_lines).strip()
    details['prose_length'] = len(prose)

    # Validate sentence count using regex
    sentences = _count_sentences(prose)
    details['sentence_count'] = sentences

    if sentences < 2 or sentences > 3:
        errors.append(f"Prose must contain exactly 2-3 sentences (found {sentences})")

    # Validate prose length (100-300 characters)
    if len(prose) < 100:
        errors.append(f"Prose is too short ({len(prose)} chars, minimum 100)")
    elif len(prose) > 300:
        errors.append(f"Prose is too long ({len(prose)} chars, maximum 300)")

    # Validate that prose content is meaningful (not just repeated words)
    if len(set(prose.lower().split())) < 10:
        errors.append("Prose content lacks sufficient vocabulary variety")

    is_valid = len(errors) == 0
    if is_valid:
        _logger.debug(f"Content validation passed: {sentences} sentences, {len(prose)} chars")
    else:
        _logger.warning(f"Content validation failed: {', '.join(errors)}")

    return {
        'is_valid': is_valid,
        'errors': errors,
        'details': details,
    }


def validate_sentence_count(prose: str) -> tuple[bool, int, Optional[str]]:
    """
    Validate that prose contains exactly 2-3 sentences.

    Uses regex-based sentence boundary detection (periods, question marks, exclamation marks).

    Args:
        prose: The prose text to validate.

    Returns:
        Tuple of (is_valid, sentence_count, error_message)
        - is_valid: True if exactly 2-3 sentences found
        - sentence_count: Number of sentences detected
        - error_message: Descriptive error message if invalid, None if valid
    """
    if not prose or not prose.strip():
        return False, 0, "Prose content is empty"

    sentence_count = _count_sentences(prose)

    if sentence_count < 2:
        return False, sentence_count, f"Too few sentences: expected 2-3, found {sentence_count}"
    elif sentence_count > 3:
        return False, sentence_count, f"Too many sentences: expected 2-3, found {sentence_count}"

    return True, sentence_count, None


def validate_prose_length(prose: str, min_length: int = 100, max_length: int = 300) -> tuple[bool, int, Optional[str]]:
    """
    Validate that prose is within acceptable length range.

    Args:
        prose: The prose text to validate.
        min_length: Minimum prose length in characters (default: 100).
        max_length: Maximum prose length in characters (default: 300).

    Returns:
        Tuple of (is_valid, prose_length, error_message)
        - is_valid: True if length is within range
        - prose_length: Length of prose in characters
        - error_message: Descriptive error message if invalid, None if valid
    """
    if not prose:
        return False, 0, "Prose content is empty"

    prose_length = len(prose)

    if prose_length < min_length:
        return False, prose_length, f"Prose too short: {prose_length} chars, minimum {min_length}"
    elif prose_length > max_length:
        return False, prose_length, f"Prose too long: {prose_length} chars, maximum {max_length}"

    return True, prose_length, None


def _count_sentences(text: str) -> int:
    """
    Count sentences in text using regex sentence boundary detection.

    Detects sentence boundaries at periods, question marks, or exclamation marks
    followed by whitespace.

    Args:
        text: The text to count sentences in.

    Returns:
        Number of sentences detected (0 if no text).
    """
    if not text or not text.strip():
        return 0

    # Split on sentence boundaries
    sentences = re.split(SENTENCE_BOUNDARY_PATTERN, text.strip())

    # Filter out empty strings (from terminal punctuation)
    sentences = [s for s in sentences if s.strip()]

    return len(sentences)


def _parse_markdown_content(content: str) -> tuple[str, str]:
    """
    Parse markdown content to extract title and prose.

    Args:
        content: The full markdown content.

    Returns:
        Tuple of (title, prose)
        - title: The H1 heading text without # prefix
        - prose: The prose content (2-3 sentences)

    Raises:
        ValueError: If content cannot be parsed or is malformed.
    """
    lines = content.strip().split('\n')

    if not lines or not lines[0].startswith("# "):
        raise ValueError("Content does not start with H1 heading")

    title = lines[0][2:].strip()
    if not title:
        raise ValueError("H1 heading is empty")

    # Get prose content (skip heading and blank line)
    prose_start_idx = 2 if len(lines) > 2 and lines[1] == '' else 1
    prose_lines = lines[prose_start_idx:]

    # Remove trailing empty lines
    while prose_lines and prose_lines[-1].strip() == '':
        prose_lines.pop()

    if not prose_lines:
        raise ValueError("No prose content found")

    prose = '\n'.join(prose_lines).strip()
    if not prose:
        raise ValueError("Prose content is empty after parsing")

    return title, prose
