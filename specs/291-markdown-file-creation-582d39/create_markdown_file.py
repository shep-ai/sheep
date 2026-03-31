#!/usr/bin/env python3
"""
Implementation script for feature 291: Create markdown file test-p1rf9x.md

This script orchestrates the complete workflow to create, validate, commit,
and push a markdown file with auto-generated content using the Claude API.

The implementation leverages the proven content_generators.py utility module
which provides complete orchestration of:
1. Content generation via Claude API (H1 heading + 2-3 sentences)
2. File I/O with proper encoding (UTF-8 without BOM)
3. Validation of structure, encoding, and line endings
4. Git commit with conventional message format
5. Remote push with upstream tracking

Usage:
    python create_markdown_file.py

Returns:
    Result dictionary with filepath, content, commit_message, and push_result
"""

import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.content_generators import create_markdown_file


def main():
    """
    Main entry point for feature 291 markdown file creation.

    Creates a markdown file named test-p1rf9x.md with auto-generated content
    using the established pattern from 290+ prior identical implementations.
    """
    filename = "test-p1rf9x.md"
    feature_number = 291

    print(f"Creating markdown file: {filename}")
    print(f"Feature: {feature_number}")
    print("-" * 60)

    try:
        # Call the orchestration function with feature number
        result = create_markdown_file(filename, feature_number=feature_number)

        # Display results
        print(f"\n✓ Successfully created markdown file!")
        print(f"  File path: {result['filepath']}")
        print(f"  Content length: {len(result['content'])} bytes")
        print(f"  Commit message: {result['commit_message']}")
        print(f"  Push result: {result['push_result']}")

        return result

    except Exception as e:
        print(f"\n✗ Error creating markdown file: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
