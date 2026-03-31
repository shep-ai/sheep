#!/usr/bin/env python3
"""
Implementation script for feature 300: Create markdown file test-tq8wxa.md

This script orchestrates the complete workflow for phase 1:
1. Create the markdown file with H1 heading and prose content
2. Validate file structure, encoding, and line endings
3. Display validation results

Phase 2 (git integration) will follow separately.
"""

import re
import sys
from pathlib import Path

# ============================================================================
# CONTENT AND CONFIGURATION
# ============================================================================

# Prose content: 3 sentences about software testing
# Total prose: ~280 characters (within 100-300 range)
PROSE_CONTENT = """# Understanding Software Testing

Software testing ensures code behaves correctly under various conditions and edge cases. By validating both expected behavior and unusual scenarios, developers build confidence their systems will perform reliably. This discipline prevents costly failures and enables teams to iterate with confidence.
"""

FILENAME = "test-tq8wxa.md"


# ============================================================================
# IMPLEMENTATION FUNCTIONS (from test_markdown_implementation.py)
# ============================================================================


def create_markdown_file(content: str, filepath: str) -> Path:
    """
    Create markdown file at specified path with UTF-8 encoding and LF line endings.

    Args:
        content: Markdown content to write
        filepath: Path where file should be created

    Returns:
        Path object pointing to created file

    Raises:
        FileExistsError: If file already exists
        ValueError: If content is empty or invalid
    """
    path = Path(filepath)

    # Check if file already exists
    if path.exists():
        raise FileExistsError(f"File {filepath} already exists")

    # Validate content is not empty
    if not content or not content.strip():
        raise ValueError("Content cannot be empty")

    # Write file with explicit UTF-8 encoding (no BOM) and LF line endings
    # Use newline='' to prevent Python from converting \n to \r\n on Windows
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    return path


def validate_h1_heading(content: str) -> bool:
    """
    Validate that content contains exactly one H1 markdown heading.

    Args:
        content: Markdown content to validate

    Returns:
        True if exactly one H1 heading is found

    Raises:
        AssertionError: If H1 count is not exactly 1
    """
    # Pattern: line starting with '# ' (single hash, space, text)
    h1_pattern = r'^# [^#]'
    matches = re.findall(h1_pattern, content, re.MULTILINE)

    h1_count = len(matches)
    assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"

    return True


def count_sentences(prose: str) -> int:
    """
    Count sentences in prose using sentence boundary detection.

    Uses regex to split on periods, question marks, and exclamation marks.

    Args:
        prose: Text content to analyze

    Returns:
        Number of sentences found
    """
    # Split on sentence-ending punctuation
    sentence_pattern = r'[.!?]+'
    sentences = re.split(sentence_pattern, prose.strip())

    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]

    return len(sentences)


def validate_prose_structure(content: str) -> bool:
    """
    Validate prose content has 2-3 sentences and 100-300 characters.

    Args:
        content: Markdown content to validate

    Returns:
        True if prose structure is valid

    Raises:
        AssertionError: If sentence count or character length is invalid
    """
    # Extract prose (skip H1 heading and blank line)
    lines = content.split('\n')

    # Find H1 heading (first line)
    if lines[0].startswith('# '):
        prose_lines = lines[2:]  # Skip heading and blank line
    else:
        raise AssertionError("No H1 heading found at start of content")

    # Join prose and strip trailing/leading whitespace and empty lines
    prose = '\n'.join(prose_lines).strip()

    # Remove any trailing newline that might be in content
    if prose.endswith('\n'):
        prose = prose[:-1]

    # Validate sentence count: 2-3 sentences
    sentence_count = count_sentences(prose)
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    # Validate character count: 100-300 characters
    char_count = len(prose)
    assert 100 <= char_count <= 300, f"Expected 100-300 characters, found {char_count}"

    return True


def validate_encoding_and_line_endings(filepath: str) -> bool:
    """
    Validate UTF-8 encoding without BOM and LF-only line endings.

    Args:
        filepath: Path to file to validate

    Returns:
        True if file passes validation

    Raises:
        AssertionError: If encoding or line endings are invalid
    """
    path = Path(filepath)

    # Read file in binary mode
    binary_content = path.read_bytes()

    # Check for UTF-8 BOM (should not be present)
    assert not binary_content.startswith(b'\xef\xbb\xbf'), "File has UTF-8 BOM (should not be present)"

    # Check for CRLF line endings (should use LF instead)
    assert b'\r' not in binary_content, "File uses CRLF line endings (should use LF)"

    # Verify the file is valid UTF-8
    try:
        binary_content.decode('utf-8')
    except UnicodeDecodeError as e:
        raise AssertionError(f"File is not valid UTF-8: {e}")

    return True


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """Main entry point: create file and validate structure."""
    try:
        print("=" * 70)
        print("PHASE 1: File Creation and Validation")
        print(f"Feature: markdown-file-creation-6aea8a (Feature 300)")
        print("=" * 70)
        print()

        # Task 1: Create markdown file
        print("Task 1: Compose and create markdown file")
        print(f"  Creating: {FILENAME}")
        filepath = create_markdown_file(PROSE_CONTENT, FILENAME)
        print(f"  [OK] File created: {filepath}")
        print()

        # Task 2: Validate H1 heading
        print("Task 2: Validate H1 heading (exactly one)")
        validate_h1_heading(PROSE_CONTENT)
        print("  [OK] H1 heading validation passed (exactly 1 heading found)")
        print()

        # Task 3: Validate prose structure
        print("Task 3: Validate prose structure (2-3 sentences, 100-300 characters)")
        validate_prose_structure(PROSE_CONTENT)

        # Get sentence count for reporting
        lines = PROSE_CONTENT.split('\n')
        prose = '\n'.join(lines[2:]).strip().rstrip('\n')
        sentence_count = count_sentences(prose)
        char_count = len(prose)
        print(f"  [OK] Prose validation passed")
        print(f"    - Sentence count: {sentence_count} (expected 2-3)")
        print(f"    - Character count: {char_count} (expected 100-300)")
        print()

        # Task 4: Validate encoding and line endings
        print("Task 4: Validate encoding and line endings")
        validate_encoding_and_line_endings(FILENAME)
        file_size = Path(FILENAME).stat().st_size
        print(f"  [OK] Encoding and line ending validation passed")
        print(f"    - UTF-8 without BOM: Yes")
        print(f"    - LF-only line endings: Yes")
        print(f"    - File size: {file_size} bytes")
        print()

        # Summary
        print("=" * 70)
        print("[OK] PHASE 1 COMPLETE: All validations passed")
        print("=" * 70)
        print()
        print("File ready for git integration (Phase 2):")
        print(f"  - File: {FILENAME}")
        print(f"  - Location: {Path(FILENAME).resolve()}")
        print(f"  - Next steps: git add, commit, push (Phase 2)")
        print()

        return 0

    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
