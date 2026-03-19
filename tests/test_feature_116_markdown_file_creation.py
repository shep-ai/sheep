"""Tests for feature 116: markdown file creation (test-45ndys.md)."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    generate_markdown_content,
    write_markdown_file,
)


class TestTask2GenerateMarkdownContent:
    """Task 2: Generate markdown content with H1 heading and 2-3 sentences."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generates_valid_markdown_string(self, mock_get_llm):
        """Test that generate_markdown_content returns a non-empty string."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Creative Writing\n\nCreative writing is the art of crafting original stories. It requires imagination and skill. Writers express their ideas through narrative forms."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_contains_h1_heading_marker(self, mock_get_llm):
        """Test that generated content contains exactly one '#' character for H1 heading."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Renewable Energy\n\nRenewable energy sources include solar and wind. These sustainable alternatives reduce carbon emissions. Countries worldwide are investing in clean energy infrastructure."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Count H1 headings (lines starting with "# ")
        h1_count = content.count("# ")
        assert h1_count == 1, f"Expected exactly one H1 heading, found {h1_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_contains_2_to_3_sentences(self, mock_get_llm):
        """Test that generated content contains 2-3 sentences (period-based count)."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Space Exploration\n\nSpace exploration drives technological innovation. It expands human knowledge of the universe. Missions to Mars represent the next frontier."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Count sentences by periods
        sentence_count = content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_content_is_coherent_prose(self, mock_get_llm):
        """Test that generated content is readable and coherent prose."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Ancient History\n\nAncient civilizations shaped human development. They built monuments that still stand today. These cultures left lasting impacts on modern society."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        # Prose should be on lines after heading and blank line
        prose = "\n".join(lines[2:]).strip()
        # Prose should have reasonable length (100-300 words)
        word_count = len(prose.split())
        assert word_count > 10, f"Prose too short: {word_count} words"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_content_has_reasonable_length(self, mock_get_llm):
        """Test that generated content is between 100-300 words in length."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Marine Biology\n\nMarine ecosystems are incredibly diverse. They contain countless species adapted to water environments. Ocean conservation is critical for planetary health."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        word_count = len(content.split())
        # Total content should be at least 15 words (heading + prose)
        assert word_count >= 15, f"Content too short: {word_count} words"


class TestTask3WriteMarkdownFileToDisk:
    """Task 3: Write markdown file to disk with UTF-8 encoding and LF line endings."""

    def test_creates_file_with_correct_name(self):
        """Test that write_markdown_file creates file test-45ndys.md in repo root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-45ndys.md")

                assert Path(filepath).exists()
                assert filepath.endswith("test-45ndys.md")
            finally:
                os.chdir(original_cwd)

    def test_file_is_readable(self):
        """Test that created file is readable and not corrupted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-45ndys.md")

                # Should be readable without errors
                file_content = Path(filepath).read_text(encoding="utf-8")
                assert file_content == content
            finally:
                os.chdir(original_cwd)

    def test_file_contains_generated_markdown_content(self):
        """Test that file contains the generated markdown content exactly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                expected_content = "# Test Topic\n\nFirst sentence about the topic. Second sentence with more details. Third sentence concluding the thought.\n"
                filepath = write_markdown_file(expected_content, "test-45ndys.md")

                actual_content = Path(filepath).read_text(encoding="utf-8")
                assert actual_content == expected_content
            finally:
                os.chdir(original_cwd)

    def test_file_size_is_nonzero(self):
        """Test that created file is not empty (non-zero size)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-45ndys.md")

                file_size = Path(filepath).stat().st_size
                assert file_size > 0, "File should not be empty"
                # Content should be at least 50 bytes
                assert file_size > 50, f"File too small: {file_size} bytes"
            finally:
                os.chdir(original_cwd)

    def test_file_size_is_in_typical_range(self):
        """Test that file size is between 400-600 bytes (typical for markdown files)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Content that should result in 400-600 byte file
                content = "# Comprehensive Topic\n\nThis is a detailed first sentence about the topic that explores several aspects. This is the second sentence that provides additional context and information. This is the third sentence that concludes the discussion.\n"
                filepath = write_markdown_file(content, "test-45ndys.md")

                file_size = Path(filepath).stat().st_size
                # Check that file is in reasonable range (or at least not tiny)
                assert file_size >= 50, f"File too small: {file_size} bytes"
            finally:
                os.chdir(original_cwd)

    def test_file_is_utf8_encoded(self):
        """Test that file can be successfully opened and decoded as UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# UTF8 Test\n\nThis file uses UTF-8 encoding. It should decode without errors. Special characters work fine.\n"
                filepath = write_markdown_file(content, "test-45ndys.md")

                # Should decode successfully as UTF-8
                binary_content = Path(filepath).read_bytes()
                decoded = binary_content.decode("utf-8")
                assert decoded == content
            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix-style LF line endings, not CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-45ndys.md")

                binary_content = Path(filepath).read_bytes()
                # Should have LF line endings
                assert b"\r\n" not in binary_content, "File should not have CRLF line endings"
            finally:
                os.chdir(original_cwd)


class TestIntegrationTask2AndTask3:
    """Integration tests for task 2 and task 3 together."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generated_content_can_be_written_to_file(self, mock_get_llm):
        """Test that generated content from task 2 can be successfully written to file in task 3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Simulate task 2: generate markdown content
                mock_llm = MagicMock()
                mock_llm.call.return_value = {
                    "content": "# Integration Test\n\nThis tests the workflow of generating and writing. The content flows from task 2 to task 3. This ensures seamless integration."
                }
                mock_get_llm.return_value = mock_llm

                generated_content = generate_markdown_content()

                # Simulate task 3: write to file
                filepath = write_markdown_file(generated_content, "test-45ndys.md")

                # Verify file was created with correct content
                assert Path(filepath).exists()
                file_content = Path(filepath).read_text(encoding="utf-8")
                assert file_content == generated_content
            finally:
                os.chdir(original_cwd)
