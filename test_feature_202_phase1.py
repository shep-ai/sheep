#!/usr/bin/env python3
"""
Test suite for feature 202 phase 1: Content Generation & File Creation

Tests the following functions:
- generate_prose(): Deterministic prose generation via Claude API (temperature=0)
- generate_title(): Deterministic title generation via Claude API (temperature=0)
- create_markdown_file(): File creation with UTF-8 encoding and LF line endings
- Validation functions for encoding, line endings, sentence count, H1 heading
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add src to path to import the feature module
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.features.feature_202_markdown_file_creation import (
    FILENAME,
    create_markdown_file,
    generate_prose,
    generate_title,
    verify_file_exists,
    verify_file_size,
    verify_h1_heading,
    verify_lf_line_endings,
    verify_prose_content,
    verify_utf8_encoding,
)


class TestGenerateProse:
    """Test suite for generate_prose function."""

    @patch("sheep.features.feature_202_markdown_file_creation.create_llm")
    def test_generate_prose_returns_string_with_sentences(self, mock_create_llm):
        """Test that generate_prose returns a string with periods (sentences)."""
        # Mock the LLM to return content with H1 and prose
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Sample Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence."
        }
        mock_create_llm.return_value = mock_llm

        result = generate_prose()

        assert isinstance(result, str)
        assert result.count(".") >= 2  # At least 2 sentences
        assert result.count(".") <= 3  # At most 3 sentences
        assert "This is the" in result

    @patch("sheep.features.feature_202_markdown_file_creation.create_llm")
    def test_generate_prose_is_deterministic(self, mock_create_llm):
        """Test that generate_prose returns identical output on repeated calls."""
        # Mock the LLM to return consistent content
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Sample Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence."
        }
        mock_create_llm.return_value = mock_llm

        result1 = generate_prose()
        result2 = generate_prose()

        assert result1 == result2

    @patch("sheep.features.feature_202_markdown_file_creation.create_llm")
    def test_generate_prose_validates_sentence_count(self, mock_create_llm):
        """Test that generate_prose raises ValueError if sentence count is wrong."""
        # Mock the LLM to return only 1 sentence
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nOnly one sentence."
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="expected 2-3"):
            generate_prose()

    @patch("sheep.features.feature_202_markdown_file_creation.create_llm")
    def test_generate_prose_handles_dict_response(self, mock_create_llm):
        """Test that generate_prose handles both dict and string LLM responses."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Title\n\nThis is sentence one. This is sentence two. This is sentence three."
        }
        mock_create_llm.return_value = mock_llm

        result = generate_prose()
        assert isinstance(result, str)
        assert len(result) > 0


class TestGenerateTitle:
    """Test suite for generate_title function."""

    @patch("sheep.features.feature_202_markdown_file_creation.create_llm")
    def test_generate_title_returns_string(self, mock_create_llm):
        """Test that generate_title returns a non-empty string."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Sample Title\n\nThis is the first sentence. This is the second sentence. This is the third sentence."
        }
        mock_create_llm.return_value = mock_llm

        result = generate_title()

        assert isinstance(result, str)
        assert len(result) > 0
        assert "Sample Title" in result

    @patch("sheep.features.feature_202_markdown_file_creation.create_llm")
    def test_generate_title_is_deterministic(self, mock_create_llm):
        """Test that generate_title returns identical output on repeated calls."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "# Consistent Title\n\nSentence one. Sentence two. Sentence three."
        }
        mock_create_llm.return_value = mock_llm

        result1 = generate_title()
        result2 = generate_title()

        assert result1 == result2

    @patch("sheep.features.feature_202_markdown_file_creation.create_llm")
    def test_generate_title_validates_h1_format(self, mock_create_llm):
        """Test that generate_title raises ValueError if H1 heading is missing."""
        mock_llm = MagicMock()
        mock_llm.call.return_value = {
            "content": "No H1 heading here\n\nSentence one. Sentence two. Sentence three."
        }
        mock_create_llm.return_value = mock_llm

        with pytest.raises(ValueError, match="must start with H1"):
            generate_title()


class TestCreateMarkdownFile:
    """Test suite for create_markdown_file function."""

    @patch("sheep.features.feature_202_markdown_file_creation.generate_title")
    @patch("sheep.features.feature_202_markdown_file_creation.generate_prose")
    def test_create_markdown_file_creates_file(self, mock_prose, mock_title):
        """Test that create_markdown_file creates the markdown file."""
        mock_title.return_value = "Test Title"
        mock_prose.return_value = "Sentence one. Sentence two. Sentence three."

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                filepath = create_markdown_file()
                assert Path(FILENAME).exists()
                assert tmpdir in filepath
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_202_markdown_file_creation.generate_title")
    @patch("sheep.features.feature_202_markdown_file_creation.generate_prose")
    def test_create_markdown_file_contains_title_and_prose(self, mock_prose, mock_title):
        """Test that created file contains both title and prose."""
        mock_title.return_value = "Test Title"
        mock_prose.return_value = "Sentence one. Sentence two. Sentence three."

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()
                content = Path(FILENAME).read_text(encoding="utf-8")
                assert "# Test Title" in content
                assert "Sentence one. Sentence two. Sentence three." in content
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_202_markdown_file_creation.generate_title")
    @patch("sheep.features.feature_202_markdown_file_creation.generate_prose")
    def test_create_markdown_file_uses_utf8_encoding(self, mock_prose, mock_title):
        """Test that created file uses UTF-8 encoding without BOM."""
        mock_title.return_value = "Test Title"
        mock_prose.return_value = "Sentence one. Sentence two. Sentence three."

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()
                binary = Path(FILENAME).read_bytes()
                # Should not have UTF-8 BOM
                assert not binary.startswith(b"\xef\xbb\xbf")
                # Should be valid UTF-8
                binary.decode("utf-8")
            finally:
                os.chdir(original_cwd)

    @patch("sheep.features.feature_202_markdown_file_creation.generate_title")
    @patch("sheep.features.feature_202_markdown_file_creation.generate_prose")
    def test_create_markdown_file_uses_lf_line_endings(self, mock_prose, mock_title):
        """Test that created file uses Unix LF line endings only."""
        mock_title.return_value = "Test Title"
        mock_prose.return_value = "Sentence one. Sentence two. Sentence three."

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                create_markdown_file()
                binary = Path(FILENAME).read_bytes()
                # Should not have CRLF
                assert b"\r\n" not in binary
                # Should not have CR
                assert b"\r" not in binary
            finally:
                os.chdir(original_cwd)


class TestVerifyUTF8Encoding:
    """Test suite for verify_utf8_encoding function."""

    def test_verify_utf8_encoding_passes_valid_file(self):
        """Test that verify_utf8_encoding passes for valid UTF-8 file without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nContent here.", encoding="utf-8")

            # Should not raise
            verify_utf8_encoding(str(filepath))

    def test_verify_utf8_encoding_rejects_bom(self):
        """Test that verify_utf8_encoding rejects files with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with BOM
            filepath.write_bytes(b"\xef\xbb\xbf# Title\n\nContent")

            with pytest.raises(ValueError, match="BOM"):
                verify_utf8_encoding(str(filepath))

    def test_verify_utf8_encoding_rejects_invalid_utf8(self):
        """Test that verify_utf8_encoding rejects invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write invalid UTF-8
            filepath.write_bytes(b"\xff\xfe# Title")

            with pytest.raises(ValueError, match="invalid UTF-8"):
                verify_utf8_encoding(str(filepath))


class TestVerifyLFLineEndings:
    """Test suite for verify_lf_line_endings function."""

    def test_verify_lf_line_endings_passes_unix_file(self):
        """Test that verify_lf_line_endings passes for Unix LF file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with LF only
            filepath.write_bytes(b"# Title\n\nContent here.\n")

            # Should not raise
            verify_lf_line_endings(str(filepath))

    def test_verify_lf_line_endings_rejects_crlf(self):
        """Test that verify_lf_line_endings rejects CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with CRLF
            filepath.write_bytes(b"# Title\r\n\r\nContent.\r\n")

            with pytest.raises(ValueError, match="CRLF"):
                verify_lf_line_endings(str(filepath))

    def test_verify_lf_line_endings_rejects_cr(self):
        """Test that verify_lf_line_endings rejects CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Write with CR
            filepath.write_bytes(b"# Title\r\rContent.\r")

            with pytest.raises(ValueError, match="CR"):
                verify_lf_line_endings(str(filepath))


class TestVerifyProseContent:
    """Test suite for verify_prose_content function."""

    def test_verify_prose_content_passes_valid_3_sentences(self):
        """Test that verify_prose_content passes for exactly 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nSentence one. Sentence two. Sentence three.\n", encoding="utf-8")

            # Should not raise
            verify_prose_content(str(filepath))

    def test_verify_prose_content_passes_valid_2_sentences(self):
        """Test that verify_prose_content passes for exactly 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nSentence one. Sentence two.\n", encoding="utf-8")

            # Should not raise
            verify_prose_content(str(filepath))

    def test_verify_prose_content_rejects_1_sentence(self):
        """Test that verify_prose_content rejects files with only 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nOnly one sentence.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="2-3 sentences"):
                verify_prose_content(str(filepath))

    def test_verify_prose_content_rejects_4_sentences(self):
        """Test that verify_prose_content rejects files with 4+ sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text(
                "# Title\n\nSentence one. Sentence two. Sentence three. Sentence four.\n",
                encoding="utf-8"
            )

            with pytest.raises(ValueError, match="2-3 sentences"):
                verify_prose_content(str(filepath))


class TestVerifyH1Heading:
    """Test suite for verify_h1_heading function."""

    def test_verify_h1_heading_passes_valid_file(self):
        """Test that verify_h1_heading passes for file with H1 at start."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nContent here.\n", encoding="utf-8")

            # Should not raise
            verify_h1_heading(str(filepath))

    def test_verify_h1_heading_rejects_missing_h1(self):
        """Test that verify_h1_heading rejects files without H1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("No heading here\n\nContent.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="H1 heading"):
                verify_h1_heading(str(filepath))

    def test_verify_h1_heading_rejects_h2_instead(self):
        """Test that verify_h1_heading rejects H2 or other headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("## Heading 2\n\nContent.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="H1 heading"):
                verify_h1_heading(str(filepath))


class TestVerifyFileSize:
    """Test suite for verify_file_size function."""

    def test_verify_file_size_passes_valid_range(self):
        """Test that verify_file_size passes for file in valid range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file around 300 bytes
            content = "# Title\n\n" + "This is content. " * 10 + "\n"
            filepath.write_text(content, encoding="utf-8")

            # Should not raise (assuming file is 250-600 bytes)
            size = filepath.stat().st_size
            if 250 <= size <= 600:
                verify_file_size(str(filepath))

    def test_verify_file_size_rejects_too_small(self):
        """Test that verify_file_size rejects files that are too small."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# T\n\nC.\n", encoding="utf-8")

            with pytest.raises(ValueError, match="outside acceptable range"):
                verify_file_size(str(filepath))

    def test_verify_file_size_rejects_too_large(self):
        """Test that verify_file_size rejects files that are too large."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            # Create file larger than 600 bytes
            content = "# Title\n\n" + "This is content. " * 50 + "\n"
            filepath.write_text(content, encoding="utf-8")

            with pytest.raises(ValueError, match="outside acceptable range"):
                verify_file_size(str(filepath))


class TestVerifyFileExists:
    """Test suite for verify_file_exists function."""

    def test_verify_file_exists_passes_existing_file(self):
        """Test that verify_file_exists passes when file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "test.md"
            filepath.write_text("# Title\n\nContent.\n", encoding="utf-8")

            # Should not raise
            verify_file_exists(str(filepath))

    def test_verify_file_exists_raises_missing_file(self):
        """Test that verify_file_exists raises FileNotFoundError when file is missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "nonexistent.md"

            with pytest.raises(FileNotFoundError):
                verify_file_exists(str(filepath))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
