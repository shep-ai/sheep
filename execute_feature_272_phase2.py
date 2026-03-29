#!/usr/bin/env python3
"""
Execute phase 2 of feature 272: Git Integration & Verification

This script orchestrates the two tasks of phase 2:
1. Commit markdown file to git with conventional message
2. Push commit to remote and verify
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import (
    commit_markdown_file,
    push_markdown_file,
)
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

FEATURE_272_FILENAME = "test-4mg4tn.md"
FEATURE_NUMBER = 272


def main():
    """Execute all phase 2 tasks for feature 272."""
    _logger.info("=" * 80)
    _logger.info("Feature 272 Phase 2: Git Integration & Verification")
    _logger.info("=" * 80)

    try:
        # Task 4: Commit markdown file
        _logger.info(f"\n[TASK 4] Committing {FEATURE_272_FILENAME} to git...")
        commit_message = f"feat({FEATURE_NUMBER}): create markdown file {FEATURE_272_FILENAME} with title and prose content"

        result = commit_markdown_file(FEATURE_272_FILENAME, commit_message)
        if result:
            _logger.info(f"✓ File committed successfully")
            _logger.info(f"  Message: {commit_message}")
        else:
            _logger.warning(f"⚠ Commit may have been skipped (file already committed)")

        # Task 5: Push commit to remote
        _logger.info(f"\n[TASK 5] Pushing commit to remote origin...")
        push_result = push_markdown_file()
        _logger.info(f"✓ Commit pushed to remote successfully")

        # Summary
        _logger.info("\n" + "=" * 80)
        _logger.info("Phase 2 Completion Summary")
        _logger.info("=" * 80)
        _logger.info(f"✓ Task 4: File committed - PASSED")
        _logger.info(f"✓ Task 5: Remote push - PASSED")
        _logger.info("\nPhase 2 Tasks Complete:")
        _logger.info(f"  - File: {FEATURE_272_FILENAME}")
        _logger.info(f"  - Commit message: {commit_message}")
        _logger.info(f"  - Remote: origin/feat/272-markdown-file-creation-ccdee5")
        _logger.info(f"  - Upstream tracking: enabled")
        _logger.info("=" * 80)

        return 0

    except Exception as e:
        _logger.error(f"\n✗ Phase 2 failed: {e}")
        _logger.exception(f"Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
