#!/usr/bin/env python3
"""
Feature 201 - Main orchestration script for markdown file creation and git integration.

This script executes the complete workflow:
1. Generate markdown content using Claude API
2. Create markdown file with UTF-8 encoding and LF line endings
3. Validate file encoding and structure
4. Stage file with git add
5. Commit with conventional commit format
6. Push to feature branch on origin

Target file: test-y9go1c.md
Branch: feat/201-markdown-file-creation-04332b
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.create_markdown import create_and_commit_markdown_file

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


def main():
    """Execute Feature 201 complete workflow."""
    _logger.info("Starting Feature 201: Markdown File Creation Workflow")
    _logger.info("=" * 80)

    # Execute the full workflow
    result = create_and_commit_markdown_file(
        filename="test-y9go1c.md",
        filepath=None,  # Use current working directory
        branch_name="feat/201-markdown-file-creation-04332b",
    )

    # Print results
    print("\n" + "=" * 80)
    print("WORKFLOW RESULTS")
    print("=" * 80)
    print(f"Success: {result['success']}")
    print(f"Steps Completed: {', '.join(result['steps_completed'])}")
    if result['steps_failed']:
        print(f"Steps Failed: {', '.join(result['steps_failed'])}")
    if result['file_path']:
        print(f"File: {result['file_path']}")
    if result['commit_hash']:
        print(f"Commit: {result['commit_hash']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")
    print("=" * 80)

    return 0 if result['success'] else 1


if __name__ == "__main__":
    sys.exit(main())
