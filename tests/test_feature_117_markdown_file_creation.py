"""Tests for feature 117: markdown file creation (test-vlr6wx.md)."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from sheep.content_generators import (
    generate_markdown_content,
    validate_markdown_file,
    write_markdown_file,
)


class TestTask1GenerateMarkdownContent:
    """Task 1.1: Generate markdown content using Claude API."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_generates_valid_markdown_string(self, mock_get_llm):
        """Test that generate_markdown_content returns a non-empty string."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Astronomy\n\nThe universe contains billions of galaxies. Each galaxy holds millions of stars and planets. Space exploration continues to reveal cosmic mysteries."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert isinstance(content, str)
        assert len(content) > 0

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_contains_h1_heading_marker(self, mock_get_llm):
        """Test that generated content contains exactly one H1 heading."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Photography\n\nPhotography captures moments in time. Modern cameras offer incredible detail and clarity. Photographers preserve memories for future generations."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        # Count H1 headings (lines starting with "# ")
        h1_count = content.count("# ")
        assert h1_count == 1, f"Expected exactly one H1 heading, found {h1_count}"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_has_blank_line_after_heading(self, mock_get_llm):
        """Test that generated content has blank line separating heading from prose."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Jazz Music\n\nJazz originated in New Orleans in the early twentieth century. This genre blends African American and European musical traditions. Jazz continues to influence modern music worldwide."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        # First line should be H1 heading
        assert lines[0].startswith("# "), "First line should be H1 heading"
        # Second line should be blank
        assert lines[1] == "", "Second line should be blank separator"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_contains_2_to_3_sentences(self, mock_get_llm):
        """Test that generated content contains 2-3 sentences (period-based count)."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Mountain Climbing\n\nMountain climbing requires physical preparation and mental determination. Climbers face extreme weather and challenging terrain. Reaching the summit provides an incredible sense of accomplishment."
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
            "content": "# Ocean Life\n\nOceans cover more than seventy percent of Earth's surface. Marine ecosystems support incredible biodiversity and complex food chains. Protecting ocean health is crucial for planetary survival."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        lines = content.split("\n")
        # Prose should be on lines after heading and blank line
        prose = "\n".join(lines[2:]).strip()
        # Prose should have reasonable length (more than 10 words)
        word_count = len(prose.split())
        assert word_count > 10, f"Prose too short: {word_count} words"

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_content_has_trailing_newline(self, mock_get_llm):
        """Test that generated content ends with a newline character."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Digital Art\n\nDigital art uses computers and software to create visual works. Artists employ various digital tools and techniques. This form of art is increasingly recognized in galleries worldwide."
        }
        mock_get_llm.return_value = mock_llm

        content = generate_markdown_content()
        assert content.endswith("\n"), "Content should end with newline"


class TestTask2WriteMarkdownFileToDisk:
    """Task 1.2: Write markdown file with UTF-8 encoding and LF line endings."""

    def test_creates_file_with_correct_name(self):
        """Test that write_markdown_file creates file test-vlr6wx.md in repo root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                assert Path(filepath).exists()
                assert filepath.endswith("test-vlr6wx.md")
            finally:
                os.chdir(original_cwd)

    def test_file_does_not_exist_initially(self):
        """Test that file test-vlr6wx.md does not exist before writing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                assert not Path("test-vlr6wx.md").exists()
            finally:
                os.chdir(original_cwd)

    def test_file_is_readable(self):
        """Test that created file is readable and not corrupted."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

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
                filepath = write_markdown_file(expected_content, "test-vlr6wx.md")

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
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                file_size = Path(filepath).stat().st_size
                assert file_size > 0, "File should not be empty"
                # Content should be at least 50 bytes
                assert file_size > 50, f"File too small: {file_size} bytes"
            finally:
                os.chdir(original_cwd)

    def test_file_is_utf8_encoded(self):
        """Test that file can be successfully opened and decoded as UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# UTF8 Test\n\nThis file uses UTF-8 encoding. It should decode without errors. Special characters work fine.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

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
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                binary_content = Path(filepath).read_bytes()
                # Should have LF line endings, not CRLF
                assert b"\r\n" not in binary_content, "File should not have CRLF line endings"
            finally:
                os.chdir(original_cwd)

    def test_file_does_not_have_utf8_bom(self):
        """Test that file does not start with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                binary_content = Path(filepath).read_bytes()
                # Should not start with UTF-8 BOM (0xEF 0xBB 0xBF)
                assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)


class TestTask3ValidateMarkdownFile:
    """Task 1.3: Validate file structure and properties."""

    def test_validates_correct_markdown_file(self):
        """Test that validate_markdown_file returns True for valid markdown file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Sample Title\n\nThis is a test sentence. This is another test sentence. This is the third test sentence.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                result = validate_markdown_file(filepath)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_validates_utf8_encoding(self):
        """Test that validation confirms UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# UTF8 Test\n\nThis file uses UTF-8 encoding. It should decode without errors. Special characters work fine.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                # Should not raise exception for valid UTF-8
                validate_markdown_file(filepath)

                # Verify no BOM is present
                binary_content = Path(filepath).read_bytes()
                assert not binary_content.startswith(b"\xef\xbb\xbf")
            finally:
                os.chdir(original_cwd)

    def test_validates_lf_line_endings(self):
        """Test that validation confirms LF-only line endings (no CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Line Ending Test\n\nThis file should have LF endings. No CRLF here. Just Unix line endings.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                # Should not raise exception for LF line endings
                validate_markdown_file(filepath)

                # Verify no CRLF is present
                binary_content = Path(filepath).read_bytes()
                assert b"\r\n" not in binary_content
            finally:
                os.chdir(original_cwd)

    def test_validates_h1_heading_structure(self):
        """Test that validation confirms exactly one H1 heading at the start."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Valid Heading\n\nThis file has a proper H1 heading. It starts the document correctly. Structure is perfect.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                # Should not raise exception for valid H1 heading
                validate_markdown_file(filepath)
            finally:
                os.chdir(original_cwd)

    def test_rejects_missing_h1_heading(self):
        """Test that validation raises ValueError when H1 heading is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Write file manually without H1 heading, using newline="" to avoid CRLF on Windows
                content = "This file has no H1 heading. It fails validation. This is wrong.\n"
                with open("test-vlr6wx.md", "w", encoding="utf-8", newline="") as f:
                    f.write(content)

                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_file("test-vlr6wx.md")
            finally:
                os.chdir(original_cwd)

    def test_validates_blank_line_separator(self):
        """Test that validation confirms blank line separates heading from prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Proper Format\n\nThis file has proper formatting. Blank line separates heading. Structure is correct.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                # Should not raise exception for proper blank line
                validate_markdown_file(filepath)
            finally:
                os.chdir(original_cwd)

    def test_rejects_missing_blank_line(self):
        """Test that validation raises ValueError when blank line separator is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Write file manually without blank line, using newline="" to avoid CRLF on Windows
                content = "# Missing Blank Line\nThis file has no separator. It fails validation. Wrong format.\n"
                with open("test-vlr6wx.md", "w", encoding="utf-8", newline="") as f:
                    f.write(content)

                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_file("test-vlr6wx.md")
            finally:
                os.chdir(original_cwd)

    def test_validates_2_to_3_sentences(self):
        """Test that validation confirms prose has exactly 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# Three Sentences\n\nFirst sentence about something. Second sentence with more info. Third sentence wrapping up.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                # Should not raise exception for 2-3 sentences
                validate_markdown_file(filepath)
            finally:
                os.chdir(original_cwd)

    def test_rejects_too_few_sentences(self):
        """Test that validation raises ValueError for fewer than 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Write file manually with only one sentence, using newline="" to avoid CRLF on Windows
                content = "# Too Few Sentences\n\nJust one sentence here.\n"
                with open("test-vlr6wx.md", "w", encoding="utf-8", newline="") as f:
                    f.write(content)

                with pytest.raises(ValueError, match="2-3 sentences"):
                    validate_markdown_file("test-vlr6wx.md")
            finally:
                os.chdir(original_cwd)

    def test_rejects_too_many_sentences(self):
        """Test that validation raises ValueError for more than 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Write file manually with four sentences, using newline="" to avoid CRLF on Windows
                content = "# Too Many Sentences\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n"
                with open("test-vlr6wx.md", "w", encoding="utf-8", newline="") as f:
                    f.write(content)

                with pytest.raises(ValueError, match="2-3 sentences"):
                    validate_markdown_file("test-vlr6wx.md")
            finally:
                os.chdir(original_cwd)

    def test_validates_trailing_newline(self):
        """Test that validation confirms file ends with trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                content = "# With Trailing Newline\n\nThis file has a trailing newline. It ends properly. Correct format.\n"
                filepath = write_markdown_file(content, "test-vlr6wx.md")

                # Should not raise exception for trailing newline
                validate_markdown_file(filepath)
            finally:
                os.chdir(original_cwd)

    def test_rejects_missing_trailing_newline(self):
        """Test that validation raises ValueError when trailing newline is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Write file manually without trailing newline
                content = "# Missing Trailing Newline\n\nThis file has no trailing newline. It ends improperly. Wrong format."
                Path("test-vlr6wx.md").write_bytes(content.encode("utf-8"))

                with pytest.raises(ValueError, match="trailing newline"):
                    validate_markdown_file("test-vlr6wx.md")
            finally:
                os.chdir(original_cwd)

    def test_raises_for_nonexistent_file(self):
        """Test that validation raises IOError for nonexistent file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                with pytest.raises(IOError, match="does not exist"):
                    validate_markdown_file("nonexistent.md")
            finally:
                os.chdir(original_cwd)


class TestIntegrationTasksAllThree:
    """Integration tests for all three tasks together."""

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_full_workflow_generate_write_validate(self, mock_get_llm):
        """Test complete workflow: generate content, write to file, validate."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Task 1.1: Generate markdown content
                mock_llm = MagicMock()
                mock_llm.call.return_value = {
                    "content": "# Complete Workflow\n\nThis tests the full workflow from generation to validation. All three tasks work together seamlessly. Integration is successful."
                }
                mock_get_llm.return_value = mock_llm

                generated_content = generate_markdown_content()

                # Task 1.2: Write to file
                filepath = write_markdown_file(generated_content, "test-vlr6wx.md")

                # Task 1.3: Validate file
                result = validate_markdown_file(filepath)

                # Verify all steps succeeded
                assert Path(filepath).exists()
                assert result is True
                file_content = Path(filepath).read_text(encoding="utf-8")
                assert file_content == generated_content
            finally:
                os.chdir(original_cwd)

    @patch("sheep.content_generators.get_reasoning_llm")
    def test_workflow_with_various_topics(self, mock_get_llm):
        """Test workflow with different topic areas to ensure robustness."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                topics = [
                    "# Scientific Discovery\n\nScience advances human knowledge. Research requires patience and dedication. Discovery leads to innovation.",
                    "# Ancient Civilizations\n\nCivilizations shaped history. They developed complex societies. Their legacies endure today.",
                    "# Modern Technology\n\nTechnology transforms daily life. Innovation accelerates progress. The future holds endless possibilities.",
                ]

                for i, topic_content in enumerate(topics):
                    mock_llm = MagicMock()
                    mock_llm.call.return_value = {"content": topic_content}
                    mock_get_llm.return_value = mock_llm

                    generated = generate_markdown_content()
                    filepath = write_markdown_file(
                        generated, f"test-vlr6wx-{i}.md"
                    )
                    result = validate_markdown_file(filepath)

                    assert result is True
            finally:
                os.chdir(original_cwd)
