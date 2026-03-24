#!/usr/bin/env python3
"""
Feature 201 - Phase 2: File Creation & Comprehensive Validation

This script executes Phase 2 of the feature workflow:
1. Takes the content generated in Phase 1 (task-1-2)
2. Creates the markdown file using the file writing function (task-2-1)
3. Validates the file using the comprehensive validation function (task-2-2)
4. Reports results for Phase 3 (git integration)

Target file: test-y9go1c.md
Branch: feat/201-markdown-file-creation-04332b
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.create_markdown import (
    create_markdown_file,
    validate_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


def execute_phase_2():
    """Execute Phase 2: File Creation & Comprehensive Validation."""
    _logger.info("=" * 80)
    _logger.info("PHASE 2: FILE CREATION & COMPREHENSIVE VALIDATION")
    _logger.info("=" * 80)

    # Phase 1 Output: Content generated via Claude API
    # Title: "Automated Implementation Excellence"
    # Prose: 262 characters, 3 sentences, meaningful content
    title = "Automated Implementation Excellence"
    prose = (
        "Automated systems achieve excellence through systematic design and careful validation. "
        "The Sheep platform demonstrates how agents can generate high-quality artifacts consistently. "
        "Every implementation follows strict standards for reliability and maintainability."
    )

    # Construct full content as it would be created by Phase 1
    full_content = f"# {title}\n\n{prose}\n"

    # Task 2-1: File Writing
    _logger.info("\nTask 2-1: Creating markdown file with pathlib...")
    _logger.info(f"  Filename: test-y9go1c.md")
    _logger.info(f"  Title: {title}")
    _logger.info(f"  Prose length: {len(prose)} characters")

    try:
        file_path = create_markdown_file(
            content=full_content,
            filename="test-y9go1c.md",
            filepath=None,  # Use current working directory (repo root)
        )
        _logger.info(f"✓ File created successfully: {file_path}")
    except Exception as e:
        _logger.error(f"✗ File creation failed: {e}")
        return {
            'success': False,
            'file_path': None,
            'validation': None,
            'error': str(e),
        }

    # Task 2-2: Comprehensive Validation
    _logger.info("\nTask 2-2: Validating file structure and encoding...")

    try:
        validation_result = validate_markdown_file(file_path)
        _logger.info(f"  Encoding check: {'✓' if validation_result['encoding']['is_valid'] else '✗'}")
        _logger.info(f"  Structure check: {'✓' if validation_result['structure']['is_valid'] else '✗'}")

        if not validation_result['is_valid']:
            _logger.warning("File validation encountered issues:")
            for error in validation_result['errors']:
                _logger.warning(f"  - {error}")
        else:
            _logger.info("✓ File validation passed all checks")
    except Exception as e:
        _logger.error(f"✗ File validation failed: {e}")
        return {
            'success': False,
            'file_path': file_path,
            'validation': None,
            'error': str(e),
        }

    # Task 2-3: Report results
    _logger.info("\n" + "=" * 80)
    _logger.info("PHASE 2 RESULTS")
    _logger.info("=" * 80)

    result = {
        'success': validation_result['is_valid'],
        'file_path': file_path,
        'validation': validation_result,
        'error': None,
    }

    if validation_result['is_valid']:
        _logger.info(f"✓ Phase 2 completed successfully")
        _logger.info(f"  File: {file_path}")
        _logger.info(f"  Validation: PASSED")
        _logger.info(f"  Ready for Phase 3 (Git Integration)")
    else:
        _logger.warning(f"Phase 2 completed with validation warnings")
        _logger.info(f"  File: {file_path}")
        _logger.warning(f"  Validation: WARNINGS")
        _logger.warning(f"  Issues: {len(validation_result['errors'])} error(s)")

    _logger.info("=" * 80)

    return result


def main():
    """Main entry point for Phase 2 execution."""
    result = execute_phase_2()

    print("\n" + "=" * 80)
    print("PHASE 2 EXECUTION RESULTS")
    print("=" * 80)
    print(f"Success: {result['success']}")
    print(f"File: {result['file_path']}")
    if result['validation']:
        print(f"Validation Result:")
        print(f"  - is_valid: {result['validation']['is_valid']}")
        print(f"  - errors: {len(result['validation']['errors'])} error(s)")
        if result['validation']['errors']:
            for error in result['validation']['errors']:
                print(f"    - {error}")
    if result['error']:
        print(f"Error: {result['error']}")
    print("=" * 80)

    return 0 if result['success'] else 1


if __name__ == "__main__":
    sys.exit(main())
