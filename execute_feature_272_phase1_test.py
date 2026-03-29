#!/usr/bin/env python3
"""
Test execution for feature 272 phase 1 without requiring API key.

This script tests phases 1 & 2 using pre-generated content to validate
the file creation and validation pipeline without needing Anthropic API access.
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import (
    write_markdown_file,
    validate_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

FEATURE_272_FILENAME = "test-4mg4tn.md"

# Pre-generated test content (realistic example)
TEST_CONTENT = """# The Evolution of Renewable Energy Technologies

Renewable energy sources have become increasingly cost-effective and essential for combating climate change and reducing dependence on fossil fuels. Solar and wind technologies have advanced dramatically over the past decade, with improvements in efficiency and storage capabilities making them viable alternatives for large-scale power generation. The transition to renewable energy represents a fundamental shift in how societies approach energy production and sustainability.
"""


def main():
    """Execute phase 1 tests using pre-generated content."""
    _logger.info("=" * 80)
    _logger.info("Feature 272 Phase 1: File Creation & Validation (Test Mode)")
    _logger.info("=" * 80)

    try:
        # Verify the test content is valid
        _logger.info("\n[PRE-CHECK] Validating test content format...")
        lines = TEST_CONTENT.split("\n")

        if not lines[0].startswith("# "):
            raise ValueError("Test content must start with H1 heading")

        if lines[1] != "":
            raise ValueError("Test content must have blank line after heading")

        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")
        if not (2 <= sentence_count <= 3):
            raise ValueError(f"Test content must have 2-3 sentences, found {sentence_count}")

        _logger.info(f"✓ Test content is valid ({len(TEST_CONTENT)} bytes)")

        # Task 2: Write markdown file
        _logger.info(f"\n[TASK 2] Writing markdown file to {FEATURE_272_FILENAME}...")
        filepath = write_markdown_file(TEST_CONTENT, FEATURE_272_FILENAME)
        _logger.info(f"✓ File written successfully: {filepath}")

        # Verify file exists
        file_path_obj = Path(filepath)
        if not file_path_obj.exists():
            raise OSError(f"File was not created: {filepath}")

        file_size = file_path_obj.stat().st_size
        _logger.info(f"  File size: {file_size} bytes")

        # Task 3: Validate markdown file format
        _logger.info(f"\n[TASK 3] Validating markdown file format...")
        result = validate_markdown_file(filepath)
        _logger.info(f"✓ File validation passed")

        # Summary
        _logger.info("\n" + "=" * 80)
        _logger.info("Phase 1 Completion Summary")
        _logger.info("=" * 80)
        _logger.info(f"✓ Task 2: File creation - PASSED")
        _logger.info(f"✓ Task 3: File validation - PASSED")
        _logger.info("\nPhase 1 Demonstration Complete:")
        _logger.info(f"  - File: {FEATURE_272_FILENAME}")
        _logger.info(f"  - Size: {file_size} bytes")
        _logger.info(f"  - Encoding: UTF-8 without BOM")
        _logger.info(f"  - Line endings: Unix LF")
        _logger.info(f"\nNote: Task 1 (content generation via Claude API) requires:")
        _logger.info(f"  - ANTHROPIC_API_KEY environment variable to be set")
        _logger.info("=" * 80)

        return 0

    except Exception as e:
        _logger.error(f"\n✗ Phase 1 failed: {e}")
        _logger.exception(f"Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
