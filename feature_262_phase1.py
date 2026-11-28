#!/usr/bin/env python3
"""
Feature 262 Phase 1: Content Generation & File Creation

Creates markdown file test-qvlm4j.md at repository root with H1 heading and 2-3 sentences
of prose content. Implements proper encoding (UTF-8, no BOM), line endings (Unix LF),
and comprehensive validation.

Tasks:
1. Generate markdown content via Claude API with validation and retry logic
2. Create file with UTF-8/LF encoding validation
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.create_markdown import (
    generate_markdown_content,
    create_markdown_file,
    validate_file_encoding,
)

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


def main():
    """Execute Feature 262 Phase 1: Content Generation & File Creation."""
    _logger.info("Starting Feature 262 Phase 1: Content Generation & File Creation")
    _logger.info("=" * 80)

    filename = "test-qvlm4j.md"
    filepath = "."

    # Task 1: Generate markdown content with validation
    _logger.info("Task 1: Generate markdown content with validation")
    try:
        content_result = generate_markdown_content(max_retries=3)
        _logger.info(f"✓ Generated markdown with title: '{content_result['title']}'")
        content = content_result['full_content']
    except ValueError as e:
        _logger.error(f"✗ Content generation failed: {e}")
        return 1

    # Task 2: Create file with UTF-8/LF encoding validation
    _logger.info("Task 2: Create file with UTF-8/LF encoding validation")
    try:
        file_path = create_markdown_file(
            content=content,
            filename=filename,
            filepath=filepath,
        )
        _logger.info(f"✓ Created markdown file: {file_path}")
    except FileExistsError as e:
        _logger.error(f"✗ File already exists: {e}")
        return 1
    except Exception as e:
        _logger.error(f"✗ File creation failed: {e}")
        return 1

    # Validate file encoding
    try:
        encoding_result = validate_file_encoding(file_path)
        if encoding_result['is_valid']:
            _logger.info("✓ File encoding validation passed")
        else:
            _logger.error(f"✗ File encoding validation failed: {encoding_result['errors']}")
            return 1
    except Exception as e:
        _logger.error(f"✗ Encoding validation failed: {e}")
        return 1

    # Print summary
    print("\n" + "=" * 80)
    print("PHASE 1 SUMMARY")
    print("=" * 80)
    print(f"✓ File created: {file_path}")
    print(f"✓ Encoding: {encoding_result['details']['encoding']}")
    print(f"✓ Line endings: {encoding_result['details']['line_ending_type']}")
    print(f"✓ File size: {encoding_result['details']['file_size_bytes']} bytes")
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())
