"""Tests for markdown file creation and validation for feature 076."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


class TestFileCreation:
    """Tests for file creation using pathlib.Path.write_text()."""

    def test_file_does_not_exist_before_creation(self):
        """Test that file does not exist before creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test-3nslmx.md"
            assert not test_file.exists()

    def test_creates_file_at_correct_path(self):
        """Test that create_markdown_file creates file at correct path."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory for file creation
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                assert path.exists()
                assert path.name == "test-3nslmx.md"
            finally:
                os.chdir(original_cwd)

    def test_file_is_created_with_correct_encoding(self):
        """Test that file is created with UTF-8 encoding."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                # File should be readable as UTF-8
                content = path.read_text(encoding='utf-8')
                assert isinstance(content, str)
                assert len(content) > 0
            finally:
                os.chdir(original_cwd)

    def test_file_contains_hardcoded_prose_content(self):
        """Test that file contains the hardcoded prose content."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                content = path.read_text(encoding='utf-8')
                assert "# The Joy of Discovery" in content
                assert "genuine discovery" in content
            finally:
                os.chdir(original_cwd)


class TestStructureValidation:
    """Tests for markdown structure validation (H1 heading, blank line, sentences)."""

    def test_first_line_is_h1_heading(self):
        """Test that first line is H1 heading."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                text_content = path.read_text(encoding='utf-8')
                lines = text_content.strip().split('\n')
                assert lines[0].startswith('# ')
            finally:
                os.chdir(original_cwd)

    def test_validates_h1_heading_correctly(self):
        """Test that validate_structure correctly identifies H1 heading."""
        import create_test_3nslmx

        # Valid H1 content
        valid_content = "# Heading\n\nSentence one. Sentence two. Sentence three."
        # Should not raise
        create_test_3nslmx.validate_structure(valid_content)

    def test_raises_when_h1_heading_missing(self):
        """Test that validate_structure raises when H1 heading is missing."""
        import create_test_3nslmx

        invalid_content = "Not a heading\n\nSentence one. Sentence two. Sentence three."
        with pytest.raises(ValueError, match="H1 heading"):
            create_test_3nslmx.validate_structure(invalid_content)

    def test_second_line_is_blank_separator(self):
        """Test that second line is blank separator."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                text_content = path.read_text(encoding='utf-8')
                lines = text_content.strip().split('\n')
                assert lines[1] == ''
            finally:
                os.chdir(original_cwd)

    def test_raises_when_blank_line_missing(self):
        """Test that validate_structure raises when blank line is missing."""
        import create_test_3nslmx

        invalid_content = "# Heading\nSentence one. Sentence two. Sentence three."
        with pytest.raises(ValueError, match="blank"):
            create_test_3nslmx.validate_structure(invalid_content)

    def test_prose_contains_two_or_three_sentences(self):
        """Test that prose content has 2-3 sentences."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                text_content = path.read_text(encoding='utf-8')
                lines = text_content.strip().split('\n')
                prose_section = '\n'.join(lines[2:])
                sentence_count = prose_section.count('.')
                assert 2 <= sentence_count <= 3
            finally:
                os.chdir(original_cwd)

    def test_raises_when_sentence_count_too_low(self):
        """Test that validate_structure raises when sentence count is less than 2."""
        import create_test_3nslmx

        invalid_content = "# Heading\n\nOnly one sentence."
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_3nslmx.validate_structure(invalid_content)

    def test_raises_when_sentence_count_too_high(self):
        """Test that validate_structure raises when sentence count exceeds 3."""
        import create_test_3nslmx

        invalid_content = "# Heading\n\nFirst. Second. Third. Fourth."
        with pytest.raises(ValueError, match="2-3 sentences"):
            create_test_3nslmx.validate_structure(invalid_content)


class TestEncodingValidation:
    """Tests for UTF-8 encoding validation (no BOM)."""

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                binary_content = path.read_bytes()
                # Should not have UTF-8 BOM
                assert not binary_content.startswith(b'\xef\xbb\xbf')
            finally:
                os.chdir(original_cwd)

    def test_raises_when_utf8_bom_present(self):
        """Test that validate_encoding_and_line_endings raises when BOM is present."""
        import create_test_3nslmx

        # UTF-8 BOM bytes
        binary_content = b'\xef\xbb\xbf' + b"# Heading\n\nSentence. Sentence. Sentence."
        with pytest.raises(ValueError, match="BOM"):
            create_test_3nslmx.validate_encoding_and_line_endings(binary_content)


class TestLineEndingValidation:
    """Tests for Unix LF line ending validation."""

    def test_file_uses_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                binary_content = path.read_bytes()
                # Should not have CRLF
                assert b'\r\n' not in binary_content
                # Should have LF
                assert b'\n' in binary_content
            finally:
                os.chdir(original_cwd)

    def test_raises_when_crlf_present(self):
        """Test that validate_encoding_and_line_endings raises when CRLF is present."""
        import create_test_3nslmx

        binary_content = b"# Heading\r\n\r\nSentence. Sentence. Sentence.\r\n"
        with pytest.raises(ValueError, match="CRLF"):
            create_test_3nslmx.validate_encoding_and_line_endings(binary_content)


class TestFileSizeValidation:
    """Tests for file size validation (350-650 bytes)."""

    def test_file_size_is_within_expected_range(self):
        """Test that file size is between 350-650 bytes."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                binary_content = path.read_bytes()
                file_size = len(binary_content)
                assert 350 <= file_size <= 650
            finally:
                os.chdir(original_cwd)

    def test_raises_when_file_size_too_small(self):
        """Test that validate_file_size raises when file is too small."""
        import create_test_3nslmx

        binary_content = b"# H\n\nS."
        with pytest.raises(ValueError, match="outside expected range"):
            create_test_3nslmx.validate_file_size(binary_content)

    def test_raises_when_file_size_too_large(self):
        """Test that validate_file_size raises when file is too large."""
        import create_test_3nslmx

        # Create content larger than 650 bytes
        binary_content = ("# Heading\n\n" + "x" * 700).encode('utf-8')
        with pytest.raises(ValueError, match="outside expected range"):
            create_test_3nslmx.validate_file_size(binary_content)


class TestValidateFileIntegration:
    """Integration tests for validate_file function."""

    def test_validate_file_passes_for_created_file(self):
        """Test that validate_file passes for file created by create_markdown_file."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                # Should not raise
                result = create_test_3nslmx.validate_file(path)
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_validate_file_checks_all_properties(self):
        """Test that validate_file checks encoding, size, and structure."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                path = create_test_3nslmx.create_markdown_file()
                # Read binary to verify properties
                binary_content = path.read_bytes()
                text_content = path.read_text(encoding='utf-8')

                # Should pass all validations
                create_test_3nslmx.validate_encoding_and_line_endings(binary_content)
                create_test_3nslmx.validate_file_size(binary_content)
                create_test_3nslmx.validate_structure(text_content)
            finally:
                os.chdir(original_cwd)


class TestMainFunction:
    """Tests for main function."""

    def test_main_returns_0_on_success(self):
        """Test that main returns 0 on successful execution."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                result = create_test_3nslmx.main()
                assert result == 0
                # Verify file was created
                assert (Path(tmpdir) / "test-3nslmx.md").exists()
            finally:
                os.chdir(original_cwd)

    def test_main_returns_1_on_error(self):
        """Test that main returns 1 when an error occurs."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Mock create_markdown_file to raise an error
                with patch.object(create_test_3nslmx, 'create_markdown_file', side_effect=Exception("Test error")):
                    result = create_test_3nslmx.main()
                    assert result == 1
            finally:
                os.chdir(original_cwd)

    def test_main_executes_create_and_validate_in_order(self):
        """Test that main executes file creation followed by validation."""
        import create_test_3nslmx

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                with patch.object(create_test_3nslmx, 'validate_file') as mock_validate:
                    mock_validate.return_value = True
                    result = create_test_3nslmx.main()
                    assert result == 0
                    # Verify validate_file was called
                    assert mock_validate.called
            finally:
                os.chdir(original_cwd)
