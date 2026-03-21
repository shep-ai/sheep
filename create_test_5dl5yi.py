#!/usr/bin/env python3
"""
Create markdown file test-5dl5yi.md for feature 145.

Uses the established create_markdown_file() orchestration function from
sheep.content_generators to handle the complete workflow:
1. Generate markdown content via Claude API (temperature 0.2)
2. Write file to disk with UTF-8 encoding
3. Validate file structure and encoding
4. Stage and commit with conventional message
5. Push to remote origin
"""

import sys
from pathlib import Path

# Add src to path so we can import sheep modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.content_generators import create_markdown_file


def main():
    """Create test-5dl5yi.md markdown file."""
    filename = "test-5dl5yi.md"

    try:
        print("Creating markdown file: test-5dl5yi.md")
        print("=" * 60)

        result = create_markdown_file(filename)

        print("\n✓ Successfully created markdown file!")
        print(f"  Filepath: {result['filepath']}")
        print(f"  Content length: {len(result['content'])} bytes")
        print(f"  Commit message: {result['commit_message']}")
        print(f"  Push result: {result['push_result']}")

    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
