#!/usr/bin/env python3
"""
Verification script for markdown file creation - feature 224, phase 1.

This script verifies that the markdown file creation works correctly.
"""

import os
import tempfile
from pathlib import Path


def create_markdown_file():
    """
    Create test-pz9pb9.md at repository root with proper structure.

    Returns:
        Path: Path to the created markdown file
    """
    heading = "# The Power of Continuous Learning"
    prose = (
        "Continuous learning is essential for personal and professional growth "
        "in an ever-changing world where knowledge and skills rapidly evolve. "
        "By embracing a mindset of curiosity and lifelong development, individuals "
        "can adapt to new challenges and unlock greater opportunities for success. "
        "Investing time in learning new technologies, methodologies, and perspectives "
        "ensures we remain relevant and effective in our endeavors."
    )

    # Construct content with explicit \n (LF line endings)
    content = f"{heading}\n\n{prose}\n"

    # Write file with UTF-8 encoding (no BOM)
    filepath = Path("test-pz9pb9.md")
    filepath.write_text(content, encoding="utf-8")

    return filepath


def verify_markdown_file(filepath):
    """
    Verify that markdown file meets all requirements.

    Args:
        filepath (Path): Path to the markdown file to verify

    Raises:
        AssertionError: If verification fails
    """
    print(f"Verifying {filepath}...")

    # File must exist
    assert filepath.exists(), f"File {filepath} does not exist"
    print("✓ File exists")

    # Read binary content to check encoding and line endings
    binary_content = filepath.read_bytes()

    # Check UTF-8 without BOM
    assert not binary_content.startswith(b'\xef\xbb\xbf'), \
        "File should not have UTF-8 BOM"
    print("✓ UTF-8 encoding without BOM")

    # Check for CRLF (should not be present)
    assert b'\r\n' not in binary_content, \
        "File should use LF line endings, not CRLF"
    print("✓ Unix LF line endings (no CRLF)")

    # Check for LF line endings
    assert b'\n' in binary_content, \
        "File should have LF line endings"
    print("✓ Has LF line endings")

    # Decode as UTF-8 text
    text_content = filepath.read_text(encoding='utf-8')

    # Check for H1 heading on first line
    lines = text_content.split('\n')
    assert lines[0].startswith('# '), \
        "File must start with H1 heading (# )"
    print(f"✓ H1 heading: {lines[0]}")

    # Check for blank line after heading
    assert len(lines) > 1 and lines[1] == '', \
        "File must have blank line after heading"
    print("✓ Blank line after heading")

    # Check for prose content (lines 2+)
    prose = '\n'.join(lines[2:]).strip()
    assert prose, "File must contain prose content"
    print(f"✓ Prose content: {prose[:50]}...")

    # Count sentences (periods)
    period_count = prose.count('.')
    assert period_count >= 2, \
        f"Prose should contain at least 2 sentences, found {period_count}"
    print(f"✓ Sentence count: {period_count} (minimum 2)")

    # Check file size (should be in 400-600 byte range, tolerance 300-800)
    file_size = filepath.stat().st_size
    assert 300 < file_size < 800, \
        f"File size {file_size} bytes outside typical range (300-800 bytes)"
    print(f"✓ File size: {file_size} bytes (target 400-600, tolerance 300-800)")

    # Check trailing newline
    assert binary_content.endswith(b'\n'), \
        "File should end with newline"
    print("✓ Ends with newline")

    print(f"\n✓ All verifications passed for {filepath}")


def main():
    """Run verification."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            print(f"Working directory: {Path.cwd()}")

            # Create file
            filepath = create_markdown_file()
            print(f"Created file: {filepath}")

            # Verify file
            verify_markdown_file(filepath)

            print("\n" + "=" * 60)
            print("SUCCESS: test-pz9pb9.md created and verified!")
            print("=" * 60)

            # Show file content
            print("\nFile content:")
            print("-" * 60)
            print(filepath.read_text(encoding='utf-8'))
            print("-" * 60)

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    main()
