#!/usr/bin/env python3
"""
Phase 1 Implementation: Content Generation & File Creation (Feature 272).

This script implements the three tasks of phase 1:
1. Generate markdown content via Claude API using the CrewAI LLM framework
2. Write the markdown file to repository root with UTF-8/LF encoding
3. Validate the markdown file format and encoding

The script uses existing utilities from sheep.content_generators:
- generate_markdown_content() - LLM-based content generation via Claude API
- write_markdown_file() - Safe file I/O with UTF-8 encoding and LF line endings
- validate_markdown_file() - Comprehensive format, encoding, and structure validation

All phase 1 tasks must complete successfully before proceeding to phase 2 (git integration).
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
)
from sheep.observability.logging import get_logger

logger = get_logger(__name__)

FEATURE_FILENAME = "test-6fioxo.md"


def task1_generate_content():
    """
    Task 1: Generate markdown content via Claude API.

    Uses CrewAI with Claude 3.5 Sonnet (temperature 0.2) to generate:
    - H1 markdown heading as title
    - Blank line separator
    - 2-3 sentences of coherent prose

    Returns:
        str: Generated markdown content with proper structure

    Raises:
        ValueError: If generated content doesn't meet format requirements
        Exception: If LLM API call fails (e.g., missing ANTHROPIC_API_KEY)
    """
    print("=" * 70)
    print("TASK 1: Generate markdown content via Claude API")
    print("=" * 70)
    print()
    print("Calling generate_markdown_content()...")
    print("- Using Claude 3.5 Sonnet via CrewAI")
    print("- Temperature: 0.2 (deterministic output)")
    print("- Generating H1 heading + blank line + 2-3 sentences")
    print()

    try:
        content = generate_markdown_content()

        # Acceptance criteria checks
        assert content is not None, "Content should not be None"
        assert isinstance(content, str), "Content should be a string"
        assert len(content) > 0, "Content should not be empty"

        lines = content.split("\n")
        assert lines[0].startswith("# "), "Content must start with H1 heading"
        assert len(lines) >= 3, "Content must have heading, blank line, and prose"
        assert lines[1] == "", "Second line must be blank separator"

        # Check sentence count
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

        print("✓ Task 1 PASSED: Content generated successfully")
        print(f"  - Content length: {len(content)} bytes")
        print(f"  - Heading: {lines[0][:50]}...")
        print(f"  - Sentences: {sentence_count}")
        print()

        return content

    except Exception as e:
        print(f"✗ Task 1 FAILED: {e}")
        raise


def task2_write_file(content):
    """
    Task 2: Write markdown file to repository root with UTF-8/LF.

    Creates file at repository root with:
    - UTF-8 encoding (no BOM)
    - Unix LF line endings
    - Default file permissions (0o644)

    Args:
        content: The markdown content to write

    Returns:
        str: Path to the created file

    Raises:
        ValueError: If filename is unsafe or content is invalid
        IOError: If file write operation fails
    """
    print("=" * 70)
    print("TASK 2: Write markdown file to repository root with UTF-8/LF")
    print("=" * 70)
    print()
    print(f"Writing file: {FEATURE_FILENAME}")
    print("- Location: repository root (current working directory)")
    print("- Encoding: UTF-8 (no BOM)")
    print("- Line endings: Unix LF (not Windows CRLF)")
    print()

    try:
        filepath_str = write_markdown_file(content, FEATURE_FILENAME)
        filepath = Path(filepath_str)

        # Acceptance criteria checks
        assert filepath.exists(), f"File {filepath} should exist after write"
        assert filepath.is_file(), f"Path {filepath} should be a file, not directory"

        # Verify file size
        file_size = filepath.stat().st_size
        assert 150 <= file_size <= 800, f"File size {file_size} outside expected range"

        # Verify encoding and line endings
        binary_content = filepath.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"
        assert b"\r\n" not in binary_content, "File should use LF, not CRLF"

        # Verify content matches exactly
        read_content = filepath.read_text(encoding="utf-8")
        assert read_content == content, "File content must match exactly"

        print("✓ Task 2 PASSED: File written successfully")
        print(f"  - File path: {filepath}")
        print(f"  - File size: {file_size} bytes")
        print(f"  - Encoding: UTF-8 without BOM")
        print(f"  - Line endings: Unix LF")
        print()

        return filepath_str

    except Exception as e:
        print(f"✗ Task 2 FAILED: {e}")
        raise


def task3_validate_file(filepath_str):
    """
    Task 3: Validate markdown file format and encoding.

    Performs comprehensive validation:
    - UTF-8 encoding without BOM
    - Unix LF line endings (no CRLF)
    - H1 heading at start of file
    - Blank line separator after heading
    - Exactly 2-3 sentences of prose
    - Trailing newline (Unix convention)

    Args:
        filepath_str: Path to the file to validate

    Returns:
        bool: True if validation passes

    Raises:
        ValueError: If file fails any validation check
        OSError: If file cannot be read
    """
    print("=" * 70)
    print("TASK 3: Validate markdown file format and encoding")
    print("=" * 70)
    print()
    print(f"Validating file: {filepath_str}")
    print("Checks:")
    print("  - UTF-8 encoding without BOM")
    print("  - Unix LF line endings")
    print("  - H1 heading at file start")
    print("  - Blank line separator")
    print("  - Exactly 2-3 sentences")
    print("  - Trailing newline")
    print()

    try:
        result = validate_markdown_file(filepath_str)

        # The function returns True and logs validation success
        assert result is True, "Validation should return True"

        # Additional verification
        filepath = Path(filepath_str)
        binary_content = filepath.read_bytes()
        text_content = binary_content.decode("utf-8")

        lines = text_content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")

        print("✓ Task 3 PASSED: File validation successful")
        print(f"  - UTF-8 encoding: ✓")
        print(f"  - Unix LF line endings: ✓")
        print(f"  - H1 heading: ✓ ({lines[0][:40]}...)")
        print(f"  - Blank separator: ✓")
        print(f"  - Sentence count: {sentence_count}")
        print(f"  - Trailing newline: ✓")
        print()

        return result

    except Exception as e:
        print(f"✗ Task 3 FAILED: {e}")
        raise


def main():
    """
    Main entry point: orchestrate phase 1 tasks.

    Executes all three tasks of phase 1 in sequence:
    1. Generate markdown content via Claude API
    2. Write markdown file to repository root
    3. Validate markdown file format and encoding

    Phase 1 must complete successfully before phase 2 (git integration).

    Exits with status code 0 on success, 1 on failure.
    """
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "Feature 272: Markdown File Creation - Phase 1 Implementation".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("║" + "Content Generation & File Creation".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    try:
        # Task 1: Generate content
        content = task1_generate_content()

        # Task 2: Write file
        filepath_str = task2_write_file(content)

        # Task 3: Validate file
        task3_validate_file(filepath_str)

        # All tasks passed
        print("=" * 70)
        print("✓ PHASE 1 COMPLETE: All tasks passed successfully")
        print("=" * 70)
        print()
        print("Summary:")
        print(f"  - Generated markdown content with H1 heading and 2-3 sentences")
        print(f"  - Created file: {FEATURE_FILENAME}")
        print(f"  - File location: {filepath_str}")
        print(f"  - Encoding: UTF-8 without BOM")
        print(f"  - Line endings: Unix LF")
        print()
        print("Next steps:")
        print("  - Phase 2: Git integration (commit and push)")
        print()

        return 0

    except Exception as e:
        print()
        print("=" * 70)
        print("✗ PHASE 1 FAILED: Implementation could not complete")
        print("=" * 70)
        print(f"Error: {e}")
        print()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
