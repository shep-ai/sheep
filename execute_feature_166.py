#!/usr/bin/env python
"""Execute feature 166 with mocked LLM calls for testing."""

import sys
from pathlib import Path
from unittest.mock import patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Mock content - realistic markdown for testing
MOCK_CONTENT = """# The Art of Continuous Learning

Continuous learning is the cornerstone of personal and professional growth in a rapidly changing world. By embracing new ideas, skills, and perspectives, individuals can adapt to challenges and unlock their full potential. The commitment to lifelong learning transforms careers, strengthens communities, and builds a foundation for lasting success.
"""

def main():
    """Execute feature 166 with mocked generate_markdown_content."""
    from sheep.features.feature_166_markdown_file_creation import (
        create_feature_166_markdown_file,
    )

    # Patch the generate_markdown_content to return our mock content
    with patch("sheep.features.feature_166_markdown_file_creation.generate_markdown_content") as mock_gen:
        mock_gen.return_value = MOCK_CONTENT

        try:
            result = create_feature_166_markdown_file()
            print("✓ Feature 166 created successfully:")
            print(f"  File: {result['filepath']}")
            print(f"  Size: {len(result['content'])} bytes")
            print(f"  Message: {result['commit_message']}")
            return 0
        except Exception as e:
            print(f"✗ Failed to create feature 166: {e}")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == "__main__":
    sys.exit(main())
