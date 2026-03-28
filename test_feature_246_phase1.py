#!/usr/bin/env python3
"""
Test suite for feature 246, phase 1: markdown-file-creation-549099
Tests content generation and file creation tasks.
"""

import tempfile
from pathlib import Path
from unittest import mock

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sheep.content_generators import generate_markdown_content, write_markdown_file


class TestGenerateMarkdownContent:
    """Test suite for task-1: Generate markdown content using LLM."""

    @mock.patch('sheep.content_generators.get_reasoning_llm')
    def test_generate_markdown_content_returns_string(self, mock_get_llm):
        """Test that generate_markdown_content returns a non-None string."""
        # Mock the LLM to return valid markdown content
        mock_llm = mock.Mock()
        mock_llm.call.return_value = {
            "content": "# Test Topic\n\nFirst sentence. Second sentence. Third sentence."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert content is not None
        assert isinstance(content, str)
        assert len(content) > 0

    @mock.patch('sheep.content_generators.get_reasoning_llm')
    def test_generated_content_starts_with_h1(self, mock_get_llm):
        """Test that generated content starts with H1 heading."""
        # Mock the LLM to return valid markdown content
        mock_llm = mock.Mock()
        mock_llm.call.return_value = {
            "content": "# Test Topic\n\nFirst sentence. Second sentence. Third sentence."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Remove leading whitespace if any
        stripped = content.lstrip()
        assert stripped.startswith("# "), f"Content should start with '# ', got: {stripped[:20]}"

    @mock.patch('sheep.content_generators.get_reasoning_llm')
    def test_generated_content_has_2_3_sentences(self, mock_get_llm):
        """Test that generated content contains 2-3 sentences."""
        # Mock the LLM to return valid markdown content
        mock_llm = mock.Mock()
        mock_llm.call.return_value = {
            "content": "# Test Topic\n\nFirst sentence. Second sentence. Third sentence."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Count periods as sentence indicators
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @mock.patch('sheep.content_generators.get_reasoning_llm')
    def test_generated_content_has_blank_line_separator(self, mock_get_llm):
        """Test that generated content has blank line separating heading from prose."""
        # Mock the LLM to return valid markdown content
        mock_llm = mock.Mock()
        mock_llm.call.return_value = {
            "content": "# Test Topic\n\nFirst sentence. Second sentence. Third sentence."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        assert len(lines) >= 3, "Content should have at least 3 lines (heading, blank, prose)"
        # First line should be heading
        assert lines[0].startswith("# "), "First line should be H1 heading"
        # Second line should be blank
        assert lines[1] == "", "Second line should be blank separator"

    @mock.patch('sheep.content_generators.get_reasoning_llm')
    def test_generated_content_ends_with_newline(self, mock_get_llm):
        """Test that generated content ends with trailing newline."""
        # Mock the LLM to return valid markdown content
        mock_llm = mock.Mock()
        mock_llm.call.return_value = {
            "content": "# Test Topic\n\nFirst sentence. Second sentence. Third sentence."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert content.endswith("\n"), "Content should end with newline"


class TestWriteMarkdownFile:
    """Test suite for task-2: Write markdown file to repository root."""

    def test_write_markdown_file_creates_file(self):
        """Test that write_markdown_file creates the file."""
        content = "# Test Title\n\nTest sentence one. Test sentence two.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-dgxq7g.md")

                # Verify file exists
                assert Path(filepath).exists(), f"File should exist: {filepath}"
                assert Path("test-dgxq7g.md").exists()
            finally:
                os.chdir(original_dir)

    def test_write_markdown_file_returns_path(self):
        """Test that write_markdown_file returns the file path."""
        content = "# Test Title\n\nTest sentence one. Test sentence two.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = write_markdown_file(content, "test-dgxq7g.md")

                assert result is not None
                assert isinstance(result, str)
                assert "test-dgxq7g.md" in result
            finally:
                os.chdir(original_dir)

    def test_write_markdown_file_content_matches_input(self):
        """Test that written file content matches the input."""
        content = "# Test Title\n\nTest sentence one. Test sentence two.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                write_markdown_file(content, "test-dgxq7g.md")

                # Read file and verify content
                written_content = Path("test-dgxq7g.md").read_text(encoding="utf-8")
                assert written_content == content, "File content should match input"
            finally:
                os.chdir(original_dir)

    def test_write_markdown_file_is_not_empty(self):
        """Test that written file is not empty."""
        content = "# Test Title\n\nTest sentence one. Test sentence two.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = write_markdown_file(content, "test-dgxq7g.md")

                file_size = Path(filepath).stat().st_size
                assert file_size > 0, "File should not be empty"
            finally:
                os.chdir(original_dir)

    def test_write_markdown_file_rejects_path_traversal(self):
        """Test that write_markdown_file rejects dangerous filenames."""
        content = "# Test Title\n\nTest sentence one. Test sentence two.\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Should reject filenames with path separators
                with pytest.raises(ValueError):
                    write_markdown_file(content, "../dangerous.md")

                with pytest.raises(ValueError):
                    write_markdown_file(content, "dir/file.md")

                with pytest.raises(ValueError):
                    write_markdown_file(content, ".hidden.md")
            finally:
                os.chdir(original_dir)


class TestIntegration:
    """Integration tests for phase 1 workflow."""

    @mock.patch('sheep.content_generators.get_reasoning_llm')
    def test_generate_then_write_workflow(self, mock_get_llm):
        """Test the complete workflow: generate content, then write to file."""
        # Mock the LLM to return valid markdown content
        mock_llm = mock.Mock()
        mock_llm.call.return_value = {
            "content": "# Test Topic\n\nFirst sentence. Second sentence. Third sentence."
        }
        mock_get_llm.return_value = mock_llm

        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Task 1: Generate content
                content = generate_markdown_content()
                assert content is not None
                assert len(content) > 0

                # Task 2: Write to file
                filepath = write_markdown_file(content, "test-dgxq7g.md")

                # Verify final file state
                assert Path(filepath).exists()
                written_content = Path(filepath).read_text(encoding="utf-8")
                assert written_content == content
                assert written_content.startswith("# ")
                assert written_content.count(".") >= 2  # at least 2 sentences
            finally:
                os.chdir(original_dir)
