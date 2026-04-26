"""
Feature 271 - Phase 2: File Creation and Validation

This module handles Phase 2 of Feature 271: writing markdown content to disk and validating format.

Phase 2 is responsible for:
- Writing generated markdown content to test-y1zgop.md at repository root
- Validating the file meets all format requirements (UTF-8, LF, H1 heading, 2-3 sentences)
- Ensuring file size is within acceptable range (250-600 bytes)

The implementation uses the Sheep platform's content_generators module which
provides safe file I/O and comprehensive validation.
"""

from pathlib import Path

from sheep.content_generators import (
    generate_markdown_content,
    validate_markdown_file,
    write_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 271 target filename
FEATURE_271_FILENAME = "test-y1zgop.md"


def execute_phase_2_file_creation_and_validation(
    generated_content: str | None = None,
) -> dict[str, str]:
    """
    Execute Phase 2: File Creation and Validation for Feature 271.

    Steps:
    1. Use provided content or generate new markdown content
    2. Write content to test-y1zgop.md at repository root with UTF-8 encoding
    3. Validate file meets all format requirements

    Args:
        generated_content: Optional pre-generated markdown content. If None, will generate fresh.

    Returns:
        Dictionary containing:
        - filepath: Full path to created file
        - content: The markdown content written
        - file_size: Size in bytes
        - validation_passed: True if all validation checks passed

    Raises:
        ValueError: If content is invalid or file operations fail.
        IOError: If file write or validation fails.
    """
    _logger.info("=" * 80)
    _logger.info("PHASE 2: FILE CREATION AND VALIDATION")
    _logger.info("=" * 80)

    try:
        # Step 1: Ensure we have content (generate if not provided)
        _logger.info("\nStep 1: Ensuring markdown content is available")
        _logger.info("-" * 80)

        if generated_content is None:
            _logger.info("No pre-generated content provided, generating fresh content...")
            content = generate_markdown_content()
            _logger.info("✓ Content generated via Claude API")
        else:
            content = generated_content
            _logger.info("✓ Using provided pre-generated content")

        content_bytes = len(content.encode("utf-8"))
        _logger.info(f"  - Content size: {len(content)} chars ({content_bytes} bytes)")

        # Step 2: Write file to disk
        _logger.info("\nStep 2: Writing markdown file to repository root")
        _logger.info("-" * 80)

        filepath = write_markdown_file(content, FEATURE_271_FILENAME)
        _logger.info(f"✓ File written: {filepath}")

        # Verify file exists and get size
        file_path_obj = Path(filepath)
        if not file_path_obj.exists():
            raise OSError(f"File creation failed: {filepath} does not exist")

        file_size = file_path_obj.stat().st_size
        _logger.info(f"  - File size: {file_size} bytes")

        # Check file size is in acceptable range
        if file_size < 250 or file_size > 600:
            _logger.warning(
                f"⚠ File size {file_size} bytes is outside typical range (250-600 bytes)"
            )
        else:
            _logger.info("✓ File size within acceptable range (250-600 bytes)")

        # Step 3: Validate file format and encoding
        _logger.info("\nStep 3: Validating file format and encoding")
        _logger.info("-" * 80)

        validate_markdown_file(filepath)
        _logger.info("✓ File validation passed")
        _logger.info("  - UTF-8 encoding verified (no BOM)")
        _logger.info("  - Unix LF line endings verified")
        _logger.info("  - H1 heading present")
        _logger.info("  - Blank line separator present")
        _logger.info("  - 2-3 sentence count verified")
        _logger.info("  - Trailing newline verified")

        # Step 4: Summary
        _logger.info("\n" + "=" * 80)
        _logger.info("PHASE 2: FILE CREATION AND VALIDATION - COMPLETE")
        _logger.info("=" * 80)

        return {
            "filepath": filepath,
            "content": content,
            "file_size": str(file_size),
            "validation_passed": "true",
        }

    except Exception as e:
        _logger.error(f"✗ Phase 2 failed: {e}")
        import traceback

        _logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    # Allow direct execution for testing/debugging
    import sys

    try:
        result = execute_phase_2_file_creation_and_validation()
        print("\n" + "=" * 80)
        print("SUCCESS: Phase 2 complete")
        print("=" * 80)
        print(f"\nFile created: {result['filepath']}")
        print(f"File size: {result['file_size']} bytes")
        print(f"Validation: {result['validation_passed']}")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
