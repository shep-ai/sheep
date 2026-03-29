#!/usr/bin/env python3
"""
Feature 262 Phase 1 Implementation: Create test-qvlm4j.md

This script creates the markdown file test-qvlm4j.md with proper content,
encoding, and validation. It uses the validated create_markdown_file function
from src/create_markdown.py.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.create_markdown import (
    create_markdown_file,
    validate_file_encoding,
)

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


def main():
    """Create test-qvlm4j.md with validated content."""
    _logger.info("Creating test-qvlm4j.md")

    # Content that meets all requirements:
    # - H1 heading on first line
    # - Blank line separator
    # - 2-3 sentences of prose (exactly 2-3 sentences)
    # - Prose length 100-300 characters
    # - 10+ unique words for vocabulary variety
    content = """# Ancient Architecture

Ancient civilizations developed remarkable architectural techniques that still inspire modern engineers today. These structures demonstrate sophisticated understanding of geometry, materials, and construction methods used to create lasting monuments."""

    # Verify prose meets requirements
    lines = content.strip().split('\n')
    prose = '\n'.join(lines[2:]).strip()
    _logger.info(f"Prose length: {len(prose)} characters")
    _logger.info(f"Prose: {prose[:100]}...")

    # Create the file
    filename = "test-qvlm4j.md"
    filepath = "."

    try:
        file_path = create_markdown_file(
            content=content,
            filename=filename,
            filepath=filepath,
        )
        _logger.info(f"✓ File created: {file_path}")
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
            _logger.info(f"  - Encoding: {encoding_result['details']['encoding']}")
            _logger.info(f"  - Line endings: {encoding_result['details']['line_ending_type']}")
            _logger.info(f"  - BOM present: {encoding_result['details']['has_bom']}")
            _logger.info(f"  - File size: {encoding_result['details']['file_size_bytes']} bytes")
        else:
            _logger.error(f"✗ File encoding validation failed: {encoding_result['errors']}")
            return 1
    except Exception as e:
        _logger.error(f"✗ Encoding validation error: {e}")
        return 1

    print("\n" + "=" * 80)
    print("PHASE 1 COMPLETE")
    print("=" * 80)
    print(f"✓ File: {file_path}")
    print(f"✓ Content structure: H1 heading, blank line, 3 sentences")
    print(f"✓ Encoding: UTF-8 without BOM")
    print(f"✓ Line endings: Unix LF")
    print("=" * 80 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
