"""Implementation for feature 207: Create markdown file test-5q8o2a.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-5q8o2a.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations

Content generation uses Claude API with temperature=0 for deterministic, reproducible output.
Same input produces identical output on repeated calls.
"""

import subprocess
import sys
from pathlib import Path

from sheep.config.llm import create_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 207 constants
FILENAME = "test-5q8o2a.md"
FEATURE_NUMBER = 207
BRANCH_NAME = "feat/207-markdown-file-creation-521e88"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with title and prose content"

# Prompt template for deterministic markdown content generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def generate_prose(feature_number: int = FEATURE_NUMBER) -> str:
    """Generate 2-3 sentences of prose content using Claude API.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same feature input produces identical prose output on repeated calls.

    Args:
        feature_number: Feature number to seed generation (default: 207)

    Returns:
        String containing 2-3 sentences of meaningful, coherent prose

    Raises:
        ValueError: If generated prose is invalid or doesn't meet requirements
        Exception: If Claude API call fails
    """
    _logger.info("Generating prose content using Claude API (temperature=0)")

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

        # Parse prose from markdown content (second paragraph after blank line)
        lines = content.strip().split("\n")

        # Find blank line separator (should be after title)
        blank_line_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "" and i > 0:
                blank_line_idx = i
                break

        if blank_line_idx is None:
            raise ValueError("Generated content missing blank line separator after heading")

        # Extract prose content (all lines after blank line)
        prose_lines = lines[blank_line_idx + 1:]
        prose = "\n".join(prose_lines).strip()

        if not prose:
            raise ValueError("Generated prose content is empty")

        # Validate sentence count
        sentence_count = prose.count(".")
        if not (2 <= sentence_count <= 3):
            raise ValueError(
                f"Generated prose has {sentence_count} sentences, expected 2-3"
            )

        _logger.info(f"Successfully generated prose with {sentence_count} sentences")
        return prose

    except Exception as e:
        _logger.error(f"Failed to generate prose: {e}")
        raise


def generate_title(feature_number: int = FEATURE_NUMBER) -> str:
    """Generate H1 markdown title using Claude API.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same feature input produces identical title output on repeated calls.

    Args:
        feature_number: Feature number to seed generation (default: 207)

    Returns:
        String containing H1 markdown heading (without # prefix)

    Raises:
        ValueError: If generated title is invalid
        Exception: If Claude API call fails
    """
    _logger.info("Generating title using Claude API (temperature=0)")

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

        # Parse title from markdown content (first line should be H1)
        lines = content.strip().split("\n")

        if not lines or not lines[0].startswith("# "):
            raise ValueError("Generated content must start with H1 heading (# Title)")

        # Extract title (remove # prefix and whitespace)
        title = lines[0].replace("# ", "").strip()

        if not title:
            raise ValueError("Generated title is empty")

        _logger.info(f"Successfully generated title: '{title}'")
        return title

    except Exception as e:
        _logger.error(f"Failed to generate title: {e}")
        raise


def create_markdown_file() -> str:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings via pathlib.Path.write_text().

    Returns:
        Absolute path to created file

    Raises:
        FileExistsError: If file already exists
        ValueError: If title or prose generation fails
        OSError: If file write operation fails
    """
    _logger.info(f"Creating markdown file: {FILENAME}")

    try:
        # Check file doesn't already exist
        file_path = Path(FILENAME)
        if file_path.exists():
            raise FileExistsError(f"File {FILENAME} already exists")

        # Generate title and prose
        _logger.info("Generating title and prose content")
        title = generate_title()
        prose = generate_prose()

        # Construct markdown content
        content = f"# {title}\n\n{prose}\n"

        # Write file with UTF-8 encoding and LF line endings
        _logger.info(f"Writing file to {file_path}")
        file_path.write_text(content, encoding="utf-8")

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {file_path}")

        file_size = file_path.stat().st_size
        _logger.info(f"Successfully created {FILENAME} ({file_size} bytes)")

        return str(file_path.absolute())

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


if __name__ == "__main__":
    try:
        file_path = create_markdown_file()
        print(f"✓ Successfully created {file_path}")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
