"""Tests for Feature 203: Create markdown file test-saop27.md with title and prose.

This test suite covers:
- Task 4: create_markdown_file() function
- Task 5: Markdown format validator
- Task 6: Encoding validator
- Task 7: Line endings validator
- Task 8: File size validator
- Task 9: Sentence count validator
- Task 10: Comprehensive validation pipeline
"""

import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Import the feature module
from sheep.features.feature_203_markdown_file_creation import (
    create_markdown_file,
    verify_file_exists,
    validate_markdown_format,
    validate_encoding,
    verify_utf8_encoding,
    validate_line_endings,
    verify_lf_line_endings,
    validate_file_size,
    verify_file_size,
    extract_prose_content,
    count_sentences,
    validate_sentence_count,
    verify_prose_content,
    validate_markdown_file,
    generate_title,
    generate_prose,
    FILENAME,
    FEATURE_NUMBER,
)


class TestTaskFour:
    """Tests for task-4: create_markdown_file() function."""

    def test_create_markdown_file_creates_file(self):
        """Test that create_markdown_file creates a file at specified location."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Test Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="Sentence one. Sentence two. Sentence three."):
                        path = create_markdown_file("test.md")
                        assert Path("test.md").exists()
                        assert "test.md" in path
            finally:
                os.chdir(original_cwd)

    def test_create_markdown_file_raises_on_existing_file(self):
        """Test that create_markdown_file raises FileExistsError if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create a file first
                Path("existing.md").write_text("# Existing\n\nContent.\n")

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Test"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="Content. More. Third."):
                        with pytest.raises(FileExistsError):
                            create_markdown_file("existing.md")
            finally:
                os.chdir(original_cwd)

    def test_created_file_contains_h1_and_prose(self):
        """Test that created file contains H1 heading and prose separated by blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="My Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First sentence. Second sentence. Third sentence."):
                        create_markdown_file("test.md")

                        content = Path("test.md").read_text(encoding="utf-8")
                        lines = content.split("\n")

                        assert lines[0] == "# My Title"
                        assert lines[1] == ""  # blank line
                        assert "First sentence. Second sentence. Third sentence." in content
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_utf8_encoding(self):
        """Test that created file uses UTF-8 encoding without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):
                        create_markdown_file("test.md")

                        binary_content = Path("test.md").read_bytes()
                        assert not binary_content.startswith(b"\xef\xbb\xbf"), "Should not have UTF-8 BOM"

                        # Should be decodable as UTF-8
                        decoded = binary_content.decode("utf-8")
                        assert "# Title" in decoded
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_lf_line_endings(self):
        """Test that created file uses Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):
                        create_markdown_file("test.md")

                        binary_content = Path("test.md").read_bytes()
                        assert b"\r\n" not in binary_content, "Should not have CRLF"
                        assert b"\n" in binary_content, "Should have LF"
            finally:
                os.chdir(original_cwd)

    def test_created_file_returns_absolute_path(self):
        """Test that create_markdown_file returns absolute path as string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with patch("sheep.features.feature_203_markdown_file_creation.generate_title", return_value="Title"):
                    with patch("sheep.features.feature_203_markdown_file_creation.generate_prose", return_value="First. Second. Third."):
                        result = create_markdown_file("test.md")

                        assert isinstance(result, str)
                        assert result.endswith("test.md")
                        assert Path(result).is_absolute()
            finally:
                os.chdir(original_cwd)


class TestTaskFive:
    """Tests for task-5: Markdown format validator."""

    def test_verify_file_exists_raises_on_missing_file(self):
        """Test that verify_file_exists raises FileNotFoundError if file missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with pytest.raises(FileNotFoundError):
                    verify_file_exists("nonexistent.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_file_exists_succeeds_if_file_exists(self):
        """Test that verify_file_exists succeeds if file exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                Path("test.md").write_text("# Title\n\nContent. More.\n")

                # Should not raise
                verify_file_exists("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_accepts_valid_structure(self):
        """Test that validate_markdown_format accepts valid markdown structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                valid_content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
                Path("test.md").write_text(valid_content, encoding="utf-8")

                # Should not raise
                validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_missing_h1(self):
        """Test that validate_markdown_format rejects content without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                invalid_content = "No heading here\n\nJust prose. More prose. And more.\n"
                Path("test.md").write_text(invalid_content, encoding="utf-8")

                with pytest.raises(ValueError, match="H1 heading"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_missing_blank_line(self):
        """Test that validate_markdown_format rejects missing blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                invalid_content = "# Title\nDirect prose. No blank line. Missing space.\n"
                Path("test.md").write_text(invalid_content, encoding="utf-8")

                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_format_rejects_multiple_h1(self):
        """Test that validate_markdown_format rejects multiple H1 headings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                invalid_content = "# First\n\nContent. More. Third.\n\n# Second\n\nMore content.\n"
                Path("test.md").write_text(invalid_content, encoding="utf-8")

                with pytest.raises(ValueError, match="one H1"):
                    validate_markdown_format("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskSix:
    """Tests for task-6: Encoding validator."""

    def test_validate_encoding_accepts_valid_utf8(self):
        """Test that validate_encoding accepts valid UTF-8 without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nContent with special chars: é, ñ, 中文. More. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should not raise
                validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_rejects_bom(self):
        """Test that validate_encoding rejects UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write content with BOM
                content = "# Title\n\nContent. More. Third.\n"
                binary_content = b"\xef\xbb\xbf" + content.encode("utf-8")
                Path("test.md").write_bytes(binary_content)

                with pytest.raises(ValueError, match="BOM"):
                    validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that validate_encoding rejects invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write invalid UTF-8
                Path("test.md").write_bytes(b"\xff\xfe invalid utf8")

                with pytest.raises(ValueError, match="UTF-8"):
                    validate_encoding("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_utf8_encoding_wrapper(self):
        """Test that verify_utf8_encoding is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nFirst. Second. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should work like validate_encoding
                verify_utf8_encoding("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskSeven:
    """Tests for task-7: Line endings validator."""

    def test_validate_line_endings_accepts_lf_only(self):
        """Test that validate_line_endings accepts Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with LF only
                Path("test.md").write_bytes(b"# Title\n\nFirst. Second. Third.\n")

                # Should not raise
                validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_crlf(self):
        """Test that validate_line_endings rejects CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with CRLF
                Path("test.md").write_bytes(b"# Title\r\n\r\nFirst. Second. Third.\r\n")

                with pytest.raises(ValueError, match="CRLF"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_line_endings_rejects_cr(self):
        """Test that validate_line_endings rejects CR line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Write with CR only (old Mac style)
                Path("test.md").write_bytes(b"# Title\r\rFirst. Second. Third.\r")

                with pytest.raises(ValueError, match="CR"):
                    validate_line_endings("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_lf_line_endings_wrapper(self):
        """Test that verify_lf_line_endings is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                Path("test.md").write_bytes(b"# Title\n\nFirst. Second. Third.\n")

                # Should work like validate_line_endings
                verify_lf_line_endings("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskEight:
    """Tests for task-8: File size validator."""

    def test_validate_file_size_accepts_in_range(self):
        """Test that validate_file_size accepts files within range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file in valid range (250-600 bytes)
                content = "# Technology and Innovation\n\n" + "This is an important sentence. " * 10 + "\n"  # ~300+ bytes
                Path("test.md").write_text(content, encoding="utf-8")

                # Verify it's in range before testing
                file_size = Path("test.md").stat().st_size
                assert 250 <= file_size <= 600, f"Test content is {file_size} bytes, outside test range"

                # Should not raise
                validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_rejects_too_small(self):
        """Test that validate_file_size rejects files too small."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file too small
                Path("test.md").write_text("# T\n\nSmall.\n", encoding="utf-8")

                with pytest.raises(ValueError, match="outside range"):
                    validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_file_size_rejects_too_large(self):
        """Test that validate_file_size rejects files too large."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create file too large
                content = "# Title\n\n" + "Word. " * 150 + "\n"  # Approx 1000+ bytes
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="outside range"):
                    validate_file_size("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_file_size_wrapper(self):
        """Test that verify_file_size is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Technology and Innovation\n\n" + "This is an important sentence. " * 10 + "\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should work like validate_file_size
                verify_file_size("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskNine:
    """Tests for task-9: Sentence count validator."""

    def test_extract_prose_content_returns_text_after_blank_line(self):
        """Test that extract_prose_content returns prose after blank line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                prose = extract_prose_content("test.md")
                assert prose == "First sentence. Second sentence. Third sentence."
            finally:
                os.chdir(original_cwd)

    def test_count_sentences_counts_periods(self):
        """Test that count_sentences counts periods correctly."""
        prose = "First sentence. Second sentence. Third sentence."
        assert count_sentences(prose) == 3

        prose = "One. Two."
        assert count_sentences(prose) == 2

        prose = "Just one."
        assert count_sentences(prose) == 1

    def test_validate_sentence_count_accepts_2_to_3(self):
        """Test that validate_sentence_count accepts 2-3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Test with 2 sentences
                content = "# Title\n\nFirst. Second.\n"
                Path("test.md").write_text(content, encoding="utf-8")
                validate_sentence_count("test.md")

                # Test with 3 sentences
                Path("test.md").write_text("# Title\n\nFirst. Second. Third.\n", encoding="utf-8")
                validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_rejects_too_few(self):
        """Test that validate_sentence_count rejects sentences < 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nJust one.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="2-3"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_sentence_count_rejects_too_many(self):
        """Test that validate_sentence_count rejects sentences > 3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nOne. Two. Three. Four.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError, match="2-3"):
                    validate_sentence_count("test.md")
            finally:
                os.chdir(original_cwd)

    def test_verify_prose_content_wrapper(self):
        """Test that verify_prose_content is a working backward-compatibility wrapper."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                content = "# Title\n\nFirst. Second. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Should work like validate_sentence_count
                verify_prose_content("test.md")
            finally:
                os.chdir(original_cwd)


class TestTaskTen:
    """Tests for task-10: Comprehensive validation pipeline."""

    def test_validate_markdown_file_passes_on_valid_file(self):
        """Test that validate_markdown_file passes on fully valid file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Create fully valid file with sufficient content (250-600 bytes)
                # Must have exactly 2-3 sentences and be 250-600 bytes
                # Using padding without periods to reach 250+ bytes while keeping sentence count at 3
                padding = " This is additional filler text to increase the byte count of this file without adding periods to the sentence count" * 2
                content = f"# Technology and Innovation\n\nTechnology shapes modern society in important ways. Progress continues steadily through innovation and development{padding}. The future looks bright.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                # Verify size is in valid range
                file_size = Path("test.md").stat().st_size
                assert 250 <= file_size <= 600, f"Test content is {file_size} bytes, outside valid range"

                # Verify it has 2-3 sentences before testing
                sentences = content.count(".")
                assert 2 <= sentences <= 3, f"Test content has {sentences} sentences, need 2-3"

                # Should not raise
                validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_fails_on_missing_file(self):
        """Test that validate_markdown_file fails if file missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                with pytest.raises(FileNotFoundError):
                    validate_markdown_file("nonexistent.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_stops_on_first_error(self):
        """Test that validate_markdown_file fails fast on first error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # File with no H1 heading - should fail at format check
                content = "No heading\n\nFirst. Second. Third.\n"
                Path("test.md").write_text(content, encoding="utf-8")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_invalid_encoding(self):
        """Test that validate_markdown_file rejects invalid UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Valid structure but invalid encoding
                Path("test.md").write_bytes(b"# Title\n\n\xff\xfe invalid\n")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_crlf_endings(self):
        """Test that validate_markdown_file rejects CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Valid structure but CRLF endings
                Path("test.md").write_bytes(b"# Title\r\n\r\nFirst. Second. Third.\r\n")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_markdown_file_rejects_wrong_size(self):
        """Test that validate_markdown_file rejects files outside size range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)

                # Valid structure but too small
                Path("test.md").write_text("# A\n\nSmall.\n", encoding="utf-8")

                with pytest.raises(ValueError):
                    validate_markdown_file("test.md")
            finally:
                os.chdir(original_cwd)
