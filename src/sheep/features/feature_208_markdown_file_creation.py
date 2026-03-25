"""Implementation for feature 208: Create markdown file test-mujic0.md with Claude API.

This module orchestrates the creation of a markdown file using Claude API with temperature=0
for deterministic, AI-generated content. Following the established pattern from feature 207
with the LLM integration approach from features 200+, this feature demonstrates the Sheep
platform's capability to execute deterministic file creation workflows with Claude API integration.

The file is created with:
- Exact filename: test-mujic0.md
- H1 markdown heading as title (AI-generated)
- 2-3 sentences of prose content (AI-generated with temperature=0)
- UTF-8 encoding without BOM
- Unix LF line endings
- File size between 250-600 bytes
- Git staging, commit, and push operations

This approach provides:
- Deterministic output (identical on repeated execution with temperature=0)
- AI-generated content leveraging Claude API
- Simplified error handling with comprehensive validation
- Reliable testing and review (reproducible results)
- Demonstrates LLM integration within the Sheep platform
"""

import subprocess
import sys
from pathlib import Path

from sheep.config.llm import create_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 208 constants
FILENAME = "test-mujic0.md"
FEATURE_NUMBER = 208
BRANCH_NAME = "feat/markdown-file-creation-9f7556"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with AI-generated content"

# Prompt template for deterministic markdown content generation with temperature=0
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title
4. Each sentence must end with a period

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def extract_prose_content(filename: str = FILENAME) -> str:
    """Extract prose content from file (text after blank line).

    Args:
        filename: Name of file to extract from (default: FILENAME)

    Returns:
        Prose content (text after H1 heading and blank line)

    Example:
        >>> prose = extract_prose_content("test-mujic0.md")
        >>> print(prose)
    """
    content = Path(filename).read_text(encoding="utf-8")
    lines = content.split("\n")

    # Prose starts after the blank line (line 2)
    # Join remaining lines, strip trailing whitespace
    if len(lines) > 2:
        prose = "\n".join(lines[2:]).strip()
        return prose

    return ""


def count_sentences(prose: str) -> int:
    """Count sentences in prose content (count periods).

    Uses simple period counting for human-written prose with proper punctuation.

    Args:
        prose: Text content to analyze

    Returns:
        Number of periods (sentences) in prose

    Example:
        >>> count_sentences("First sentence. Second sentence.")
        2
    """
    return prose.count(".")


def generate_content() -> tuple[str, str]:
    """Generate H1 title and 2-3 sentences of prose using Claude API with temperature=0.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same execution produces identical content on repeated calls.

    The function:
    1. Calls Claude API with markdown generation prompt
    2. Parses response to extract H1 title and prose
    3. Validates sentence count (2-3 periods)
    4. Returns tuple of (title_text, prose_text)

    Returns:
        Tuple of (title, prose) where:
        - title: H1 heading text (without # prefix)
        - prose: 2-3 sentences of prose content

    Raises:
        ValueError: If API response format is invalid or requirements not met
        Exception: If Claude API call fails

    Example:
        >>> title, prose = generate_content()
        >>> print(f"# {title}\\n\\n{prose}")
        # Example Title
        <BLANKLINE>
        This is a sentence. This is another sentence.
    """
    _logger.info("Generating markdown content using Claude API (temperature=0)")

    try:
        # Create LLM with temperature=0 for deterministic generation
        llm = create_llm(temperature=0)

        # Call Claude API with the generation prompt
        response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

        # Extract response text
        if isinstance(response, dict):
            content = str(response.get("content", str(response)))
        else:
            content = str(response)

        _logger.debug(f"Raw LLM response (first 100 chars): {content[:100]}...")

        # Parse markdown content
        lines = content.strip().split("\n")

        # Find and extract H1 title (first line should start with "# ")
        if not lines or not lines[0].startswith("# "):
            raise ValueError(
                "Generated content must start with H1 heading (# Title)"
            )

        title = lines[0].replace("# ", "").strip()
        if not title:
            raise ValueError("Generated title is empty")

        # Find blank line separator (should be after title)
        blank_line_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "" and i > 0:
                blank_line_idx = i
                break

        if blank_line_idx is None:
            raise ValueError(
                "Generated content missing blank line separator after heading"
            )

        # Extract prose content (all lines after blank line)
        prose_lines = lines[blank_line_idx + 1 :]
        prose = "\n".join(prose_lines).strip()

        if not prose:
            raise ValueError("Generated prose content is empty")

        # Validate sentence count (2-3 periods)
        sentence_count = prose.count(".")
        if not (2 <= sentence_count <= 3):
            raise ValueError(
                f"Generated prose has {sentence_count} sentences, expected 2-3"
            )

        _logger.info(
            f"Successfully generated content: title='{title}', "
            f"prose_length={len(prose)}, sentence_count={sentence_count}"
        )
        return (title, prose)

    except ValueError as e:
        _logger.error(f"Validation failed in generate_content: {e}")
        raise
    except Exception as e:
        _logger.error(f"Failed to generate content: {e}")
        raise
