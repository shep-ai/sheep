#!/usr/bin/env python3
"""
Execute phase 1 of feature 272: Content Generation & File Creation

This script orchestrates the three tasks of phase 1:
1. Generate markdown content using Claude API
2. Write markdown file to repository root
3. Validate markdown file format strictly
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
    validate_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

FEATURE_272_FILENAME = "test-4mg4tn.md"


def main():
    """Execute all phase 1 tasks for feature 272."""
    _logger.info("=" * 80)
    _logger.info("Feature 272 Phase 1: Content Generation & File Creation")
    _logger.info("=" * 80)

    try:
        # Task 1: Generate markdown content
        _logger.info("\n[TASK 1] Generating markdown content using Claude API...")
        content = generate_markdown_content()
        _logger.info(f"✓ Content generated successfully ({len(content)} bytes)")
        _logger.debug(f"Content preview: {content[:100]}...")

        # Task 2: Write markdown file
        _logger.info(f"\n[TASK 2] Writing markdown file to {FEATURE_272_FILENAME}...")
        filepath = write_markdown_file(content, FEATURE_272_FILENAME)
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
        _logger.info(f"✓ Task 1: Content generation - PASSED")
        _logger.info(f"✓ Task 2: File creation - PASSED")
        _logger.info(f"✓ Task 3: File validation - PASSED")
        _logger.info("\nPhase 1 Tasks Complete:")
        _logger.info(f"  - Content: H1 heading + 2-3 sentences")
        _logger.info(f"  - File: {FEATURE_272_FILENAME}")
        _logger.info(f"  - Size: {file_size} bytes")
        _logger.info(f"  - Encoding: UTF-8 without BOM")
        _logger.info(f"  - Line endings: Unix LF")
        _logger.info("=" * 80)

        return 0

    except Exception as e:
        _logger.error(f"\n✗ Phase 1 failed: {e}")
        _logger.exception(f"Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
