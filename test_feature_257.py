#!/usr/bin/env python3
"""Test script to execute feature 257 with mocked API calls.

This script executes the feature 257 markdown file creation workflow
with mocked API calls to avoid needing a real ANTHROPIC_API_KEY.
"""

import sys
from pathlib import Path
from unittest import mock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Sample valid markdown content matching the specification
# Use explicit LF line endings (\n) and ensure no CRLF on Windows
SAMPLE_MARKDOWN_CONTENT = (
    "# The Beauty of Coastal Ecosystems\n"
    "\n"
    "Coastal ecosystems are among the most biodiverse and productive environments on Earth, "
    "supporting countless species and providing essential services to human communities. "
    "These dynamic zones where land meets sea harbor unique adaptations that allow organisms "
    "to thrive in constantly changing conditions.\n"
)

# Normalize line endings to LF only
SAMPLE_MARKDOWN_CONTENT = SAMPLE_MARKDOWN_CONTENT.replace('\r\n', '\n')


def test_feature_257_with_mocks():
    """Execute feature 257 with mocked API calls."""
    # Mock the generate_markdown_content to return sample content
    with mock.patch('sheep.content_generators.generate_markdown_content') as mock_generate, \
         mock.patch('sheep.content_generators.push_markdown_file') as mock_push:

        mock_generate.return_value = SAMPLE_MARKDOWN_CONTENT
        mock_push.return_value = "Pushed to remote feature branch"

        # Import and execute the feature
        from sheep.features.feature_257_markdown_file_creation import create_feature_257_markdown_file

        result = create_feature_257_markdown_file()

        # Verify result structure
        assert result is not None
        assert isinstance(result, dict)
        assert 'filepath' in result
        assert 'content' in result
        assert 'commit_message' in result
        assert 'push_result' in result

        # Verify content
        assert result['content'] == SAMPLE_MARKDOWN_CONTENT
        assert result['commit_message'] == "feat(257): create markdown file test-nm5lr3.md with prose content"
        assert result['push_result'] == "Pushed to remote feature branch"

        print("✓ Feature 257 executed successfully")
        print(f"  File: {result['filepath']}")
        print(f"  Size: {len(result['content'])} bytes")
        print(f"  Message: {result['commit_message']}")

        return result


if __name__ == "__main__":
    try:
        result = test_feature_257_with_mocks()
        sys.exit(0)
    except Exception as e:
        print(f"✗ Feature 257 execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
