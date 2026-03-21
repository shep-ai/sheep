"""Tests for markdown file creation and validation for feature 134."""

import os
import tempfile
from pathlib import Path

import pytest


class TestFileCreation:
    """Tests for file creation using pathlib.Path.write_text()."""

    def test_file_does_not_exist_before_creation(self):
        """Test that file does not exist before creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test-an35bo.md"
            assert not test_file.exists()

    def test_creates_file_at_correct_path(self):
        """Test that create_markdown_file creates file at correct path."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory for file creation
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_an35bo.create_markdown_file()
                assert path.exists()
                assert path.name == "test-an35bo.md"
            finally:
                os.chdir(original_cwd)

    def test_file_is_created_with_correct_encoding(self):
        """Test that file is created with UTF-8 encoding."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_an35bo.create_markdown_file()
                # File should be readable as UTF-8
                content = path.read_text(encoding='utf-8')
                assert isinstance(content, str)
                assert len(content) > 0
            finally:
                os.chdir(original_cwd)

    def test_file_contains_hardcoded_prose_content(self):
        """Test that file contains the hardcoded prose content."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_an35bo.create_markdown_file()
                content = path.read_text(encoding='utf-8')
                assert "# Feature 134 Implementation" in content
                assert "Feature 134" in content
                assert "markdown file creation" in content.lower()
            finally:
                os.chdir(original_cwd)


class TestStructureValidation:
    """Tests for markdown structure validation (H1 heading, blank line, sentences)."""

    def test_first_line_is_h1_heading(self):
        """Test that first line is H1 heading."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_an35bo.create_markdown_file()
                text_content = path.read_text(encoding='utf-8')
                lines = text_content.strip().split('\n')
                assert lines[0].startswith('# ')
            finally:
                os.chdir(original_cwd)

    def test_validates_h1_heading_correctly(self):
        """Test that validate_structure correctly identifies H1 heading."""
        import create_test_an35bo

        # Valid H1 content
        valid_content = "# Heading\n\nSentence one. Sentence two. Sentence three."
        # Should not raise
        create_test_an35bo.validate_structure(valid_content)

    def test_raises_when_h1_heading_missing(self):
        """Test that validate_structure raises when H1 heading is missing."""
        import create_test_an35bo

        # Invalid: no H1 heading
        invalid_content = "No heading\n\nSentence one. Sentence two. Sentence three."
        with pytest.raises(ValueError, match="First line must be H1 heading"):
            create_test_an35bo.validate_structure(invalid_content)

    def test_raises_when_blank_line_missing(self):
        """Test that validate_structure raises when blank line is missing."""
        import create_test_an35bo

        # Invalid: no blank line between heading and prose
        invalid_content = "# Heading\nSentence one. Sentence two. Sentence three."
        with pytest.raises(ValueError):
            create_test_an35bo.validate_structure(invalid_content)

    def test_validates_two_sentence_minimum(self):
        """Test that validate_structure requires at least 2 sentences."""
        import create_test_an35bo

        # Invalid: only 1 sentence
        invalid_content = "# Heading\n\nSentence one."
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_an35bo.validate_structure(invalid_content)

    def test_validates_three_sentence_maximum(self):
        """Test that validate_structure enforces 3 sentence maximum."""
        import create_test_an35bo

        # Invalid: 4 sentences
        invalid_content = "# Heading\n\nSentence one. Sentence two. Sentence three. Sentence four."
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_an35bo.validate_structure(invalid_content)

    def test_validates_valid_two_sentence_content(self):
        """Test that validate_structure accepts 2-sentence content."""
        import create_test_an35bo

        valid_content = "# Heading\n\nSentence one. Sentence two."
        result = create_test_an35bo.validate_structure(valid_content)
        assert result is True

    def test_validates_valid_three_sentence_content(self):
        """Test that validate_structure accepts 3-sentence content."""
        import create_test_an35bo

        valid_content = "# Heading\n\nSentence one. Sentence two. Sentence three."
        result = create_test_an35bo.validate_structure(valid_content)
        assert result is True


class TestEncodingAndLineEndings:
    """Tests for UTF-8 encoding and Unix LF line ending validation."""

    def test_validates_utf8_encoding(self):
        """Test that validate_encoding_and_line_endings accepts valid UTF-8."""
        import create_test_an35bo

        # Valid UTF-8 without BOM
        valid_binary = "# Heading\n\nContent.".encode('utf-8')
        result = create_test_an35bo.validate_encoding_and_line_endings(valid_binary)
        assert result is True

    def test_rejects_utf8_bom(self):
        """Test that validate_encoding_and_line_endings rejects UTF-8 BOM."""
        import create_test_an35bo

        # UTF-8 BOM prefix
        invalid_binary = b"\xef\xbb\xbf" + "# Heading\n\nContent.".encode('utf-8')
        with pytest.raises(ValueError, match="UTF-8 BOM"):
            create_test_an35bo.validate_encoding_and_line_endings(invalid_binary)

    def test_rejects_crlf_line_endings(self):
        """Test that validate_encoding_and_line_endings rejects CRLF."""
        import create_test_an35bo

        # CRLF line endings (Windows style)
        invalid_binary = "# Heading\r\n\r\nContent.".encode('utf-8')
        with pytest.raises(ValueError, match="CRLF line endings"):
            create_test_an35bo.validate_encoding_and_line_endings(invalid_binary)

    def test_accepts_lf_line_endings(self):
        """Test that validate_encoding_and_line_endings accepts LF."""
        import create_test_an35bo

        # LF line endings (Unix style)
        valid_binary = "# Heading\n\nContent.".encode('utf-8')
        result = create_test_an35bo.validate_encoding_and_line_endings(valid_binary)
        assert result is True

    def test_rejects_invalid_utf8(self):
        """Test that validate_encoding_and_line_endings rejects invalid UTF-8."""
        import create_test_an35bo

        # Invalid UTF-8 sequence
        invalid_binary = b"\x80\x81\x82"
        with pytest.raises(ValueError, match="not valid UTF-8"):
            create_test_an35bo.validate_encoding_and_line_endings(invalid_binary)


class TestFileSizeValidation:
    """Tests for file size validation (400-600 bytes)."""

    def test_accepts_valid_file_size_at_min_boundary(self):
        """Test that validate_file_size accepts file at 400 byte minimum."""
        import create_test_an35bo

        # Exactly 400 bytes
        binary_content = b"x" * 400
        result = create_test_an35bo.validate_file_size(binary_content)
        assert result is True

    def test_accepts_valid_file_size_at_max_boundary(self):
        """Test that validate_file_size accepts file at 600 byte maximum."""
        import create_test_an35bo

        # Exactly 600 bytes
        binary_content = b"x" * 600
        result = create_test_an35bo.validate_file_size(binary_content)
        assert result is True

    def test_accepts_valid_file_size_in_middle(self):
        """Test that validate_file_size accepts file in middle of range."""
        import create_test_an35bo

        # 500 bytes (middle of range)
        binary_content = b"x" * 500
        result = create_test_an35bo.validate_file_size(binary_content)
        assert result is True

    def test_rejects_file_size_below_minimum(self):
        """Test that validate_file_size rejects file below 400 bytes."""
        import create_test_an35bo

        # 399 bytes (just below minimum)
        binary_content = b"x" * 399
        with pytest.raises(ValueError, match="outside expected range"):
            create_test_an35bo.validate_file_size(binary_content)

    def test_rejects_file_size_above_maximum(self):
        """Test that validate_file_size rejects file above 600 bytes."""
        import create_test_an35bo

        # 601 bytes (just above maximum)
        binary_content = b"x" * 601
        with pytest.raises(ValueError, match="outside expected range"):
            create_test_an35bo.validate_file_size(binary_content)


class TestFullFileValidation:
    """Integration tests for complete file validation."""

    def test_validates_correctly_created_file(self):
        """Test that validate_file passes for correctly created file."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_an35bo.create_markdown_file()
                # Should not raise any exceptions
                result = create_test_an35bo.validate_file(path)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_rejects_nonexistent_file(self):
        """Test that validate_file rejects nonexistent file."""
        import create_test_an35bo

        nonexistent_path = Path("nonexistent.md")
        with pytest.raises(ValueError, match="does not exist"):
            create_test_an35bo.validate_file(nonexistent_path)

    def test_rejects_file_with_invalid_encoding(self):
        """Test that validate_file rejects file with invalid encoding."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write file with invalid UTF-8 sequence
            test_file.write_bytes(b"\x80\x81\x82")

            with pytest.raises(ValueError):
                create_test_an35bo.validate_file(test_file)

    def test_rejects_file_with_crlf_line_endings(self):
        """Test that validate_file rejects file with CRLF line endings."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write file with CRLF line endings
            content = "# Heading\r\n\r\nContent. More content."
            test_file.write_bytes(content.encode('utf-8'))

            with pytest.raises(ValueError, match="CRLF"):
                create_test_an35bo.validate_file(test_file)

    def test_rejects_file_too_small(self):
        """Test that validate_file rejects file below 400 bytes."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write file that's too small
            test_file.write_text("# Heading\n\nToo short.", encoding='utf-8', newline='\n')

            with pytest.raises(ValueError, match="outside expected range"):
                create_test_an35bo.validate_file(test_file)

    def test_rejects_file_too_large(self):
        """Test that validate_file rejects file above 600 bytes."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write file that's too large
            long_content = "# Heading\n\n" + "x" * 600
            test_file.write_text(long_content, encoding='utf-8', newline='\n')

            with pytest.raises(ValueError, match="outside expected range"):
                create_test_an35bo.validate_file(test_file)


class TestIntegration:
    """Integration tests for complete workflow."""

    def test_create_and_validate_end_to_end(self):
        """Test complete workflow: create file and validate it."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create the file
                path = create_test_an35bo.create_markdown_file()
                assert path is not False
                assert path.exists()

                # Validate the created file
                result = create_test_an35bo.validate_file(path)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_created_file_has_correct_properties(self):
        """Test that created file has all expected properties."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                path = create_test_an35bo.create_markdown_file()

                # Check file exists
                assert path.exists()

                # Check file size is in range
                binary_content = path.read_bytes()
                assert 400 <= len(binary_content) <= 600

                # Check encoding and line endings
                content = path.read_text(encoding='utf-8')
                assert "\r\n" not in content  # No CRLF

                # Check structure
                lines = content.split("\n")
                assert lines[0].startswith("# ")
                assert lines[1] == ""

                # Check prose exists and has correct sentence count
                prose = "\n".join(lines[2:]).strip()
                sentence_count = prose.count(".") + prose.count("!") + prose.count("?")
                assert 2 <= sentence_count <= 3
            finally:
                os.chdir(original_cwd)

    def test_file_with_multiple_validations(self):
        """Test that file passes multiple validation rounds."""
        import create_test_an35bo

        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create file
                path = create_test_an35bo.create_markdown_file()
                assert path.exists()

                # Validate multiple times to ensure consistency
                for i in range(3):
                    result = create_test_an35bo.validate_file(path)
                    assert result is True, f"Validation failed on iteration {i+1}"
            finally:
                os.chdir(original_cwd)
