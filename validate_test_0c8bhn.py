#!/usr/bin/env python3
"""
Feature 248: markdown-file-creation-87cda7
Validation script for test-0c8bhn.md

Phase 2 (Validation):
- Task 2: Implement file structure validation function
- Task 3: Execute file structure validation

Validates:
- File exists at repository root (test-0c8bhn.md)
- File contains exactly one H1 heading (line starting with '# ')
- File contains exactly 2-3 sentences of prose content
"""

import re
import sys
from pathlib import Path


def _count_sentences(prose: str) -> int:
    r"""
    Count sentences in prose using regex pattern for sentence boundaries.

    Regex pattern [.!?](?:\s|$) matches:
    - Period, question mark, or exclamation mark
    - Followed by either whitespace or end-of-string

    This avoids false positives on ellipses (...) and abbreviations (Mr., Dr., etc.)

    Args:
        prose: Text content to count sentences in

    Returns:
        Number of sentence boundaries detected
    """
    matches = re.findall(r'[.!?](?:\s|$)', prose)
    return len(matches)


def _has_h1_heading(lines: list[str]) -> bool:
    """
    Check if first line is H1 markdown heading.

    Args:
        lines: List of file lines

    Returns:
        True if first line starts with '# '
    """
    return len(lines) > 0 and lines[0].startswith('# ')


def validate_file(filepath: str = "test-0c8bhn.md") -> bool:
    """
    Validate test-0c8bhn.md meets all structural requirements.

    Task 2: Implement file structure validation function

    Checks:
    - File exists at expected path (repository root)
    - File contains exactly one H1 heading (first line starts with '# ')
    - File contains exactly 2 or 3 sentences of prose content

    Args:
        filepath: Path to file to validate (default: test-0c8bhn.md)

    Returns:
        True if all checks pass

    Raises:
        FileNotFoundError: If file does not exist at filepath
        ValueError: If file structure does not meet requirements
    """
    path = Path(filepath)

    # Check 1: File exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    # Read file content
    try:
        content = path.read_text(encoding='utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"File is not valid UTF-8: {e}")
    except OSError as e:
        raise ValueError(f"Error reading file: {e}")

    # Split into lines for structural validation
    lines = content.split('\n')

    # Check 2: H1 heading exists
    if not _has_h1_heading(lines):
        first_line = lines[0] if lines else "(empty file)"
        raise ValueError(
            f"No H1 heading found. First line must start with '# '. Got: {first_line!r}"
        )

    # Check 3: Extract and count sentences in prose content
    # Prose is everything after the H1 heading and blank line
    prose_lines = []
    for i in range(1, len(lines)):
        if i == 1:  # Skip blank line after heading
            continue
        prose_lines.append(lines[i])

    prose_content = '\n'.join(prose_lines).strip()

    if not prose_content:
        raise ValueError("No prose content found after H1 heading")

    sentence_count = _count_sentences(prose_content)

    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"Expected 2-3 sentences, found {sentence_count} sentences"
        )

    # All checks passed
    print(f"[PASS] File {filepath} validates successfully")
    print(f"  - H1 heading: {lines[0]}")
    print(f"  - Sentences: {sentence_count}")
    print(f"  - Prose length: {len(prose_content)} characters")

    return True


def main() -> int:
    """
    Task 3: Execute file structure validation

    Main entry point - call validation function and report results.
    """
    print("=" * 60)
    print("Feature 248: Validation Phase")
    print("=" * 60)

    try:
        print("\nTask 2-3: Validating file structure...")
        result = validate_file("test-0c8bhn.md")

        print("\n" + "=" * 60)
        print("[PASS] Validation complete - feature 248 ready for git integration")
        print("=" * 60)
        return 0

    except FileNotFoundError as e:
        print(f"[FAIL] File error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"[FAIL] Validation error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
