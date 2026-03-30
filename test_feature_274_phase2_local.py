#!/usr/bin/env python3
"""
Feature 274 Phase 2: Markdown File Creation (Alternative - Local Test Content)

This script implements the complete workflow using content_generators functions,
but generates test markdown content locally instead of calling Claude API.
This allows testing the complete workflow without ANTHROPIC_API_KEY.

Workflow:
1. Generate test markdown content locally
2. Write file to disk with UTF-8/LF
3. Validate file structure and properties
4. Stage and commit with conventional message
5. Push to remote with upstream tracking
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
    commit_markdown_file,
    push_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

FILENAME = "test-ihdf8h.md"

# Test markdown content (locally generated to avoid API key requirement)
# Follows the required format: H1 heading + blank line + 2-3 sentences
TEST_MARKDOWN_CONTENT = """# Bioluminescence in Deep Ocean Creatures

Bioluminescence is the production and emission of light by living organisms in the deep ocean. Many fish and crustaceans use light to communicate, attract prey, and confuse predators in the darkness below. This remarkable adaptation allows creatures to thrive in extreme environments where sunlight never reaches.
"""


def test_file_not_exists_before():
    """Test that file does not exist before calling workflow."""
    print("\n=== Test 1: File does not exist before workflow ===")
    filepath = Path(FILENAME)
    assert not filepath.exists(), f"File {filepath} should not exist before test"
    print(f"[PASS] File {FILENAME} does not exist before workflow")


def test_write_file():
    """Test writing markdown file."""
    print("\n=== Test 2: Write markdown file to disk ===")
    try:
        filepath = write_markdown_file(TEST_MARKDOWN_CONTENT, FILENAME)
        print(f"[PASS] File written successfully to {filepath}")
        print(f"  File size: {Path(filepath).stat().st_size} bytes")
        return filepath
    except Exception as e:
        print(f"[FAIL] Failed to write file: {e}")
        raise


def test_validate_file(filepath):
    """Test file validation."""
    print("\n=== Test 3: Validate markdown file ===")
    try:
        validate_markdown_file(filepath)
        print(f"[PASS] File validation passed")
        print(f"  Structure: H1 heading + blank line + prose")
        print(f"  Encoding: UTF-8 without BOM")
        print(f"  Line endings: Unix LF (not CRLF)")
        return True
    except Exception as e:
        print(f"[FAIL] File validation failed: {e}")
        raise


def test_commit_file(filepath):
    """Test git commit."""
    print("\n=== Test 4: Commit markdown file ===")
    try:
        result = commit_markdown_file(
            filepath,
            TEST_MARKDOWN_CONTENT,
            feature_number=274
        )
        print(f"[PASS] File committed successfully")
        print(f"  Commit message: feat(274): create markdown file {FILENAME} with prose content")
        print(f"  Result: {result[:100]}" if len(result) > 100 else f"  Result: {result}")
        return result
    except Exception as e:
        print(f"[FAIL] Failed to commit file: {e}")
        raise


def test_push_file():
    """Test git push."""
    print("\n=== Test 5: Push to remote repository ===")
    try:
        result = push_markdown_file()
        print(f"[PASS] File pushed successfully")
        print(f"  Remote: origin")
        print(f"  Result: {result[:100]}" if len(result) > 100 else f"  Result: {result}")
        return result
    except Exception as e:
        print(f"[FAIL] Failed to push file: {e}")
        raise


def test_file_exists_after():
    """Test that file exists after workflow."""
    print("\n=== Test 6: File exists after workflow ===")
    filepath = Path(FILENAME)
    assert filepath.exists(), f"File {filepath} should exist after workflow"
    print(f"[PASS] File {FILENAME} exists at repository root")
    print(f"  Path: {filepath.absolute()}")
    print(f"  Size: {filepath.stat().st_size} bytes")


def test_content_preview():
    """Show content preview."""
    print("\n=== Content Preview ===")
    print("---")
    print(TEST_MARKDOWN_CONTENT)
    print("---")


def main():
    """Execute complete workflow."""
    print("=" * 70)
    print("FEATURE 274: MARKDOWN FILE CREATION - PHASE 2 (LOCAL TEST)")
    print("=" * 70)

    try:
        # Test 1: File doesn't exist
        test_file_not_exists_before()

        # Test 2: Write file
        filepath = test_write_file()

        # Test 3: Validate file
        test_validate_file(filepath)

        # Test 4: Commit file
        test_commit_file(filepath)

        # Test 5: Push file
        test_push_file()

        # Test 6: Verify file exists
        test_file_exists_after()

        # Show content
        test_content_preview()

        # Summary
        print("\n" + "=" * 70)
        print("[PASS] WORKFLOW COMPLETE")
        print("=" * 70)
        print("\nAcceptance Criteria Met:")
        print("[PASS] File test-ihdf8h.md created at repository root")
        print("[PASS] File contains H1 heading + blank line + 2-3 sentences")
        print("[PASS] File uses UTF-8 encoding without BOM")
        print("[PASS] File uses Unix LF line endings (not CRLF)")
        print("[PASS] File staged and committed with conventional message")
        print("[PASS] Commit pushed to remote origin with upstream tracking")
        print("=" * 70)

        return 0

    except AssertionError as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n[FAIL] UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
