"""Implementation for feature 202: Create markdown file test-b1weep.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-b1weep.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations
"""

import subprocess
import sys
from pathlib import Path

from sheep.config.llm import create_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 202 constants
FILENAME = "test-b1weep.md"
FEATURE_NUMBER = 202
BRANCH_NAME = "feat/202-markdown-file-creation-4dbea6"
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
        feature_number: Feature number to seed generation (default: 202)

    Returns:
        String containing 2-3 sentences of meaningful, coherent prose

    Raises:
        ValueError: If generated prose is invalid or doesn't meet requirements
        Exception: If Claude API call fails
    """
    _logger.info(f"Generating prose content using Claude API (temperature=0)")

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
        feature_number: Feature number to seed generation (default: 202)

    Returns:
        String containing H1 markdown heading (without # prefix)

    Raises:
        ValueError: If generated title is invalid
        Exception: If Claude API call fails
    """
    _logger.info(f"Generating title using Claude API (temperature=0)")

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


def verify_file_exists(filename: str = FILENAME) -> None:
    """Verify that the markdown file exists.

    Args:
        filename: Path to file to verify (defaults to FILENAME)

    Raises:
        FileNotFoundError: If file does not exist
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")


def verify_h1_heading(filename: str = FILENAME) -> None:
    """Verify file contains exactly one H1 heading at start.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If H1 heading is missing or not at start
    """
    file_path = Path(filename)
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    if not lines or not lines[0].startswith("# "):
        raise ValueError("File must start with H1 heading (# Title)")


def verify_prose_content(filename: str = FILENAME) -> None:
    """Verify file contains exactly 2-3 sentences of prose.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If sentence count is not 2-3
    """
    file_path = Path(filename)
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Get prose content (lines after heading and blank line)
    prose_lines = []
    if len(lines) > 2:
        prose_lines = lines[2:]

    prose_text = "\n".join(prose_lines).strip()
    sentence_count = prose_text.count(".")

    if not (2 <= sentence_count <= 3):
        raise ValueError(
            f"Expected 2-3 sentences, found {sentence_count}"
        )


def verify_utf8_encoding(filename: str = FILENAME) -> None:
    """Verify file is UTF-8 encoded without BOM.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If file has BOM or is not valid UTF-8
    """
    file_path = Path(filename)
    binary_content = file_path.read_bytes()

    # Check for UTF-8 BOM
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File contains UTF-8 BOM (byte order mark)")

    # Verify UTF-8 encoding
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File contains invalid UTF-8 encoding: {e}") from e


def verify_lf_line_endings(filename: str = FILENAME) -> None:
    """Verify file uses Unix LF line endings exclusively.

    Args:
        filename: Path to file to verify

    Raises:
        ValueError: If file contains CRLF or CR line endings
    """
    file_path = Path(filename)
    binary_content = file_path.read_bytes()

    if b"\r\n" in binary_content:
        raise ValueError("File contains Windows CRLF (\\r\\n) line endings")

    if b"\r" in binary_content:
        raise ValueError("File contains Mac CR (\\r) line endings")


def verify_file_size(filename: str = FILENAME, min_bytes: int = 250, max_bytes: int = 600) -> None:
    """Verify file size is within acceptable range.

    Args:
        filename: Path to file to verify
        min_bytes: Minimum acceptable file size in bytes
        max_bytes: Maximum acceptable file size in bytes

    Raises:
        ValueError: If file size is outside the acceptable range
    """
    file_path = Path(filename)
    file_size = file_path.stat().st_size

    if not (min_bytes <= file_size <= max_bytes):
        raise ValueError(
            f"File size {file_size} bytes outside acceptable range {min_bytes}-{max_bytes} bytes"
        )


def main() -> None:
    """Main orchestration function for feature 202 phase 1.

    Executes the complete workflow:
    1. Generate markdown content (title + prose)
    2. Create markdown file with UTF-8 encoding and LF line endings
    3. Validate all success criteria before committing

    Raises:
        ValueError: If any generation or validation check fails
        OSError: If file operations fail
    """
    try:
        print("Phase 1: Content Generation & File Creation")
        print("=" * 60)

        # Step 1: Create markdown file
        _logger.info("Step 1: Creating markdown file with generated content")
        filepath = create_markdown_file()
        print(f"✓ File created: {filepath}")

        # Step 2: Verify file exists
        _logger.info("Step 2: Verifying file exists")
        verify_file_exists()
        print(f"✓ File {FILENAME} exists in repo root")

        # Step 3: Verify markdown structure
        _logger.info("Step 3: Verifying markdown structure")
        verify_h1_heading()
        print("✓ File contains exactly one H1 heading")

        verify_prose_content()
        print("✓ File contains 2-3 sentences of prose")

        # Step 4: Verify encoding
        _logger.info("Step 4: Verifying file encoding")
        verify_utf8_encoding()
        print("✓ File is UTF-8 encoded without BOM")

        # Step 5: Verify line endings
        _logger.info("Step 5: Verifying line endings")
        verify_lf_line_endings()
        print("✓ File uses Unix LF line endings")

        # Step 6: Verify file size
        _logger.info("Step 6: Verifying file size")
        verify_file_size()
        print("✓ File size within valid range (250-600 bytes)")

        print()
        print("=" * 60)
        print("✓ Feature 202 Phase 1 Complete!")
        print("  File created and all validations passed.")
        print(f"  Ready for Phase 2 (Validation) and Phase 3 (Git Integration)")

    except FileExistsError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"✗ File operation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
