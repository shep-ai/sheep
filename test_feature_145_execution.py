#!/usr/bin/env python
"""Test script for feature 145 execution and validation."""

from pathlib import Path
from unittest import mock

# Mock the LLM to avoid requiring ANTHROPIC_API_KEY
sample_markdown_content = """# The Power of Comprehensive Documentation

Effective documentation is the cornerstone of successful software development, enabling teams to collaborate seamlessly and maintain code quality over extended periods. Well-structured markdown files provide clear guidance to developers, establish consistent patterns across projects, and serve as crucial references during maintenance and evolution of codebases. Through systematic organization and thoughtful composition of documentation, we create lasting value that benefits both current team members and future developers who will build upon our work.
"""


def test_feature_145_execution():
    """Test that feature 145 creates the markdown file correctly."""
    repo_path = Path.cwd()

    # Mock the generate_markdown_content function
    with mock.patch(
        "sheep.content_generators.generate_markdown_content",
        return_value=sample_markdown_content,
    ):
        from sheep.features.feature_145_markdown_file_creation import (
            create_feature_145_markdown_file,
        )

        result = create_feature_145_markdown_file(repo_path=str(repo_path))

        # Verify the returned dictionary
        assert "filepath" in result
        assert "content" in result
        assert "commit_message" in result
        assert "push_result" in result

        # Verify the file was created
        filepath = Path(result["filepath"])
        assert filepath.exists(), f"File {filepath} does not exist"
        assert filepath.name == "test-rtj7cz.md"

        # Verify file content
        file_content = filepath.read_text(encoding="utf-8")
        assert file_content.startswith("# "), "File should start with H1 heading"
        assert file_content.endswith("\n"), "File should end with newline"

        # Verify the file has blank line separator
        lines = file_content.split("\n")
        assert lines[0].startswith("# "), "First line should be H1"
        assert lines[1] == "", "Second line should be blank"

        # Verify sentence count (2-3 periods)
        period_count = file_content.count(".")
        assert 2 <= period_count <= 3, f"Should have 2-3 sentences, found {period_count}"

        # Verify UTF-8 encoding without BOM
        binary_content = filepath.read_bytes()
        assert not binary_content.startswith(
            b"\xef\xbb\xbf"
        ), "File should not have UTF-8 BOM"

        # Verify no CRLF line endings
        assert b"\r\n" not in binary_content, "File should not have CRLF line endings"

        # Verify file size is in reasonable range
        file_size = len(binary_content)
        assert (
            400 <= file_size <= 600
        ), f"File size should be 400-600 bytes, got {file_size}"

        print("✓ Feature 145 execution test passed")
        print(f"  File created: {filepath}")
        print(f"  File size: {file_size} bytes")
        print(f"  Content preview: {file_content[:80]}...")

        return result


if __name__ == "__main__":
    result = test_feature_145_execution()
    print("\nFeature 145 successfully created and validated!")
