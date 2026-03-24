#!/usr/bin/env python3
"""
Feature 195 Phase 2: File Creation & Validation

This script implements:
- Task 2: Write markdown file with correct encoding and line endings
- Task 3: Validate markdown file (structure, encoding, content)
"""

import sys
from pathlib import Path

from sheep.content_generators import (
    generate_markdown_content,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

FILENAME = "test-2xz0x5.md"


def main():
    """Execute phase 2: File creation and validation."""
    _logger.info("=== Feature 195 Phase 2: File Creation & Validation ===")

    try:
        # Step 1: Generate markdown content (from phase 1)
        _logger.info("Step 1: Generating markdown content")
        content = generate_markdown_content()
        _logger.info(f"✓ Generated {len(content)} bytes of content")

        # Step 2: Write file with correct encoding and line endings (task-2)
        _logger.info("\nStep 2: Writing markdown file with correct encoding/line endings")
        filepath = write_markdown_file(content, FILENAME)
        _logger.info(f"✓ File created: {filepath}")

        # Verify file properties
        file_path = Path(filepath)
        file_size = file_path.stat().st_size
        _logger.info(f"  File size: {file_size} bytes (expected 250-600)")

        # Step 3: Validate markdown file (task-3)
        _logger.info("\nStep 3: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info(f"✓ Validation passed for {FILENAME}")

        _logger.info("\n=== Phase 2 Complete ===")
        _logger.info(f"File: {FILENAME}")
        _logger.info(f"Path: {filepath}")
        _logger.info(f"Size: {file_size} bytes")
        _logger.info("Next: Phase 3 - Git Integration & Push")

        return 0

    except Exception as e:
        _logger.error(f"Phase 2 failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
