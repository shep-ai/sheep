"""Implementation for feature 202: Create markdown file test-1u4gfg.md with title and prose content.

This module orchestrates phases 1-2 (content generation and file creation & validation) of feature 202.
Phase 1 generates deterministic markdown content using Claude API with feature number 202 seeding.
Phase 2 creates the markdown file with UTF-8 encoding and Unix LF line endings, then validates it.
Phase 3 (git integration & push) will be handled separately.
"""

import subprocess
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from create_markdown import (
    generate_markdown_content_for_feature,
    create_markdown_file,
    validate_markdown_file,
)

# Feature 202 constants
FILENAME = "test-1u4gfg.md"
FEATURE_NUMBER = 202
BRANCH_NAME = "feat/markdown-file-creation-05a473"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with title and prose content"


def generate_content() -> dict[str, str]:
    """Phase 1: Generate markdown content for feature 202.

    Uses Claude API with deterministic seeding based on feature number 202
    to generate a meaningful title (H1 heading) and 2-3 sentences of thematically
    coherent prose content.

    Returns:
        Dictionary with keys:
        - 'title': The H1 heading text (without # prefix)
        - 'prose': The 2-3 sentences of prose content
        - 'full_content': The complete markdown including heading

    Raises:
        ValueError: If content generation fails or content validation fails.
        Exception: If Claude API is unavailable.
    """
    print(f"Phase 1: Content Generation for Feature {FEATURE_NUMBER}")
    print("=" * 60)

    try:
        content_result = generate_markdown_content_for_feature(feature_number=FEATURE_NUMBER)

        print(f"✓ Content generated successfully")
        print(f"  Title: {content_result['title']}")
        print(f"  Prose length: {len(content_result['prose'])} characters")
        print()

        return content_result

    except Exception as e:
        print(f"✗ Content generation failed: {e}", file=sys.stderr)
        raise


def create_file(content: str) -> str:
    """Phase 2a: Create markdown file with proper encoding and line endings.

    Creates the markdown file at repository root using pathlib.Path.write_text()
    with explicit encoding='utf-8' and newline='\n' parameters to guarantee
    UTF-8 encoding without BOM and Unix LF line endings.

    Args:
        content: The markdown content to write to file

    Returns:
        Path to the created file as a string

    Raises:
        ValueError: If filename is invalid
        IOError: If file write operation fails
    """
    print(f"Phase 2a: File Creation")
    print("=" * 60)

    try:
        file_path = create_markdown_file(content, filename=FILENAME)

        print(f"✓ File created successfully")
        print(f"  Path: {file_path}")
        print(f"  Size: {Path(file_path).stat().st_size} bytes")
        print()

        return file_path

    except Exception as e:
        print(f"✗ File creation failed: {e}", file=sys.stderr)
        raise


def validate_file(file_path: str) -> bool:
    """Phase 2b: Validate created markdown file.

    Performs comprehensive validation of the created file:
    - Markdown syntax (exactly one H1 heading at start, blank line after)
    - Prose content (exactly 2-3 sentences)
    - UTF-8 encoding without BOM
    - Unix LF line endings only
    - File size within 250-600 bytes
    - CommonMark format compliance

    Args:
        file_path: Path to the markdown file to validate

    Returns:
        True if all validation checks pass

    Raises:
        ValueError: If validation fails
    """
    print(f"Phase 2b: File Validation")
    print("=" * 60)

    try:
        validation = validate_markdown_file(file_path)

        if not validation['is_valid']:
            errors = validation.get('errors', [])
            error_msg = "\n  ".join(errors)
            raise ValueError(f"Validation failed:\n  {error_msg}")

        # Log validation results
        structure = validation.get('structure', {})
        encoding = validation.get('encoding', {})

        print(f"✓ File validation passed")
        print(f"  Structure: {structure.get('message', 'Valid')}")
        print(f"  Encoding: {encoding.get('message', 'Valid')}")
        print()

        return True

    except Exception as e:
        print(f"✗ File validation failed: {e}", file=sys.stderr)
        raise


def verify_file_exists(filename: str = FILENAME) -> None:
    """Verify that the markdown file exists at repository root.

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
    """Main orchestration function for feature 202 phases 1-2.

    Executes:
    1. Phase 1: Content generation via Claude API with deterministic seeding
    2. Phase 2a: File creation with proper encoding and line endings
    2. Phase 2b: Comprehensive file validation

    Raises:
        Exception: If any phase fails
    """
    try:
        print()
        print("=" * 60)
        print(f"Feature 202: Markdown File Creation (test-1u4gfg.md)")
        print("=" * 60)
        print()

        # Phase 1: Generate content
        content_result = generate_content()

        # Phase 2a: Create file
        file_path = create_file(content_result['full_content'])

        # Phase 2b: Validate file
        validate_file(file_path)

        # Additional verification checks
        print(f"Phase 2c: Additional Verification")
        print("=" * 60)

        verify_file_exists()
        print(f"✓ File exists at repository root")

        verify_h1_heading()
        print(f"✓ File contains H1 heading at start")

        verify_prose_content()
        print(f"✓ File contains 2-3 sentences of prose")

        verify_utf8_encoding()
        print(f"✓ File is UTF-8 encoded without BOM")

        verify_lf_line_endings()
        print(f"✓ File uses Unix LF line endings")

        verify_file_size()
        print(f"✓ File size within acceptable range (250-600 bytes)")

        print()
        print("=" * 60)
        print("✓ Feature 202 Phases 1-2 Complete!")
        print("=" * 60)
        print()
        print("Summary:")
        print(f"  File: {FILENAME}")
        print(f"  Title: {content_result['title']}")
        print(f"  Location: {file_path}")
        print(f"  Ready for Phase 3: Git Integration")
        print()

    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Verification failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
