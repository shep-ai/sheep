#!/usr/bin/env python3
"""
Phase 1 Implementation: Content Generation for Feature 271

This script demonstrates Phase 1 of the feature 271 implementation:
- Call content_generators.generate_markdown_content()
- Generate markdown content with H1 heading + 2-3 sentences
- Validate the generated content structure
- Log the result for verification
"""

import os
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import generate_markdown_content
from sheep.observability.logging import get_logger

logger = get_logger(__name__)


def main():
    """Execute Phase 1: Generate markdown content."""
    logger.info("=" * 80)
    logger.info("PHASE 1: CONTENT GENERATION")
    logger.info("=" * 80)

    try:
        logger.info("\nStep 1: Calling generate_markdown_content()")
        logger.info("-" * 80)

        # Call the content generation function
        content = generate_markdown_content()

        logger.info("✓ Content generation successful")
        logger.info(f"✓ Generated {len(content)} characters ({len(content.encode('utf-8'))} bytes)")

        # Validate basic structure
        logger.info("\nStep 2: Validating generated content structure")
        logger.info("-" * 80)

        lines = content.split("\n")
        logger.info(f"✓ Content has {len(lines)} lines")

        # Check H1 heading
        if lines[0].startswith("# "):
            logger.info(f"✓ H1 heading present: {lines[0][:60]}...")
        else:
            logger.error("✗ H1 heading missing")
            return False

        # Check blank line
        if len(lines) > 1 and lines[1] == "":
            logger.info("✓ Blank line separator present")
        else:
            logger.error("✗ Blank line separator missing")
            return False

        # Check prose content
        prose_lines = [l for l in lines[2:] if l.strip()]
        logger.info(f"✓ Prose content found: {len(prose_lines)} non-empty lines")

        # Count sentences
        sentence_count = content.count(".")
        logger.info(f"✓ Sentence count: {sentence_count}")
        if 2 <= sentence_count <= 3:
            logger.info(f"✓ Sentence count within range (2-3)")
        else:
            logger.warning(f"⚠ Sentence count {sentence_count} outside expected range (2-3)")

        # Check encoding
        try:
            content.encode("utf-8")
            logger.info("✓ Content is valid UTF-8")
        except UnicodeEncodeError as e:
            logger.error(f"✗ UTF-8 encoding error: {e}")
            return False

        # Check for trailing newline
        if content.endswith("\n"):
            logger.info("✓ Content ends with trailing newline")
        else:
            logger.warning("⚠ Content does not end with trailing newline")

        logger.info("\n" + "=" * 80)
        logger.info("PHASE 1: CONTENT GENERATION - COMPLETE")
        logger.info("=" * 80)

        logger.info("\nGenerated Content:")
        logger.info("-" * 80)
        logger.info(content)
        logger.info("-" * 80)

        return True

    except Exception as e:
        logger.error(f"✗ Phase 1 failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
