"""Tests for feature 205: Create markdown file test-m6zeml.md with hard-coded content."""

from pathlib import Path
import pytest

from sheep.features.feature_205_markdown_file_creation import (
    FILENAME,
    TITLE_TEXT,
    PROSE_CONTENT,
    create_markdown_file,
    verify_file_exists,
    validate_markdown_format,
    validate_sentence_count,
    validate_encoding,
    validate_line_endings,
    validate_file_size,
    validate_markdown_file,
    extract_prose_content,
    count_sentences,
)


class TestCreateMarkdownFile:
    """Tests for create_markdown_file() function."""

    def test_create_markdown_file_creates_file_on_disk(self, tmp_path):
        """Test that create_markdown_file() creates a file on disk."""
        # Change to temp directory
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # File should not exist before creation
            test_file = Path(FILENAME)
            assert not test_file.exists()

            # Create file
            result = create_markdown_file()

            # File should exist after creation
            assert result.exists()
            assert test_file.exists()

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_returns_path(self, tmp_path):
        """Test that create_markdown_file() returns a Path object."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            result = create_markdown_file()
            assert isinstance(result, Path)
            assert result.name == FILENAME

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_content_format(self, tmp_path):
        """Test that created file has correct markdown structure."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_markdown_file()
            test_file = Path(FILENAME)

            # Read and verify content
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            # First line should be H1 title
            assert lines[0] == f"# {TITLE_TEXT}"

            # Second line should be blank
            assert lines[1] == ""

            # Prose content should be in remaining lines
            prose_content = "\n".join(lines[2:]).strip()
            assert PROSE_CONTENT in prose_content

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_utf8_encoding(self, tmp_path):
        """Test that created file is UTF-8 encoded."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_markdown_file()
            test_file = Path(FILENAME)

            # Should be readable as UTF-8
            content = test_file.read_text(encoding="utf-8")
            assert content is not None

            # Should not have BOM
            binary = test_file.read_bytes()
            assert not binary.startswith(b"\xef\xbb\xbf")

        finally:
            import os
            os.chdir(original_cwd)

    def test_create_markdown_file_size(self, tmp_path):
        """Test that created file is within acceptable size range."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_markdown_file()
            test_file = Path(FILENAME)

            file_size = test_file.stat().st_size
            # Should be between 250-600 bytes
            assert 250 <= file_size <= 600

        finally:
            import os
            os.chdir(original_cwd)


class TestVerifyFileExists:
    """Tests for verify_file_exists() function."""

    def test_verify_file_exists_passes(self, tmp_path):
        """Test verify_file_exists() when file exists."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nContent.")

        # Should not raise
        verify_file_exists(str(test_file))

    def test_verify_file_exists_fails_missing_file(self, tmp_path):
        """Test verify_file_exists() raises FileNotFoundError when file missing."""
        test_file = tmp_path / FILENAME

        with pytest.raises(FileNotFoundError):
            verify_file_exists(str(test_file))


class TestValidateMarkdownFormat:
    """Tests for validate_markdown_format() function."""

    def test_validate_markdown_format_passes_valid_file(self, tmp_path):
        """Test validate_markdown_format() with valid markdown structure."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test Title\n\nFirst sentence. Second sentence.")

        # Should not raise
        validate_markdown_format(str(test_file))

    def test_validate_markdown_format_fails_missing_h1(self, tmp_path):
        """Test validate_markdown_format() fails without H1 heading."""
        test_file = tmp_path / FILENAME
        test_file.write_text("No heading here\n\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="H1"):
            validate_markdown_format(str(test_file))

    def test_validate_markdown_format_fails_missing_blank_line(self, tmp_path):
        """Test validate_markdown_format() fails without blank line separator."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test Title\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="blank"):
            validate_markdown_format(str(test_file))

    def test_validate_markdown_format_fails_multiple_h1(self, tmp_path):
        """Test validate_markdown_format() fails with multiple H1 headings."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test Title\n\n# Another H1\n\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="exactly one"):
            validate_markdown_format(str(test_file))


class TestValidateSentenceCount:
    """Tests for validate_sentence_count() function."""

    def test_validate_sentence_count_passes_two_sentences(self, tmp_path):
        """Test validate_sentence_count() with exactly 2 sentences."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence.")

        # Should not raise
        validate_sentence_count(str(test_file))

    def test_validate_sentence_count_passes_three_sentences(self, tmp_path):
        """Test validate_sentence_count() with exactly 3 sentences."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence. Third sentence.")

        # Should not raise
        validate_sentence_count(str(test_file))

    def test_validate_sentence_count_fails_one_sentence(self, tmp_path):
        """Test validate_sentence_count() fails with 1 sentence."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nOnly one sentence.")

        with pytest.raises(ValueError, match="2-3"):
            validate_sentence_count(str(test_file))

    def test_validate_sentence_count_fails_four_sentences(self, tmp_path):
        """Test validate_sentence_count() fails with 4 sentences."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst. Second. Third. Fourth.")

        with pytest.raises(ValueError, match="2-3"):
            validate_sentence_count(str(test_file))


class TestValidateEncoding:
    """Tests for validate_encoding() function."""

    def test_validate_encoding_passes_utf8(self, tmp_path):
        """Test validate_encoding() with valid UTF-8."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence.", encoding="utf-8")

        # Should not raise
        validate_encoding(str(test_file))

    def test_validate_encoding_fails_utf8_bom(self, tmp_path):
        """Test validate_encoding() fails with UTF-8 BOM."""
        test_file = tmp_path / FILENAME
        # Write with BOM
        test_file.write_bytes(b"\xef\xbb\xbf# Test\n\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="BOM"):
            validate_encoding(str(test_file))


class TestValidateLineEndings:
    """Tests for validate_line_endings() function."""

    def test_validate_line_endings_passes_lf(self, tmp_path):
        """Test validate_line_endings() with LF endings."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nFirst sentence. Second sentence.", encoding="utf-8")

        # Should not raise
        validate_line_endings(str(test_file))

    def test_validate_line_endings_fails_crlf(self, tmp_path):
        """Test validate_line_endings() fails with CRLF."""
        test_file = tmp_path / FILENAME
        test_file.write_bytes(b"# Test\r\n\r\nFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="CRLF"):
            validate_line_endings(str(test_file))

    def test_validate_line_endings_fails_cr(self, tmp_path):
        """Test validate_line_endings() fails with CR."""
        test_file = tmp_path / FILENAME
        test_file.write_bytes(b"# Test\r\rFirst sentence. Second sentence.")

        with pytest.raises(ValueError, match="CR"):
            validate_line_endings(str(test_file))


class TestValidateFileSize:
    """Tests for validate_file_size() function."""

    def test_validate_file_size_passes_valid_size(self, tmp_path):
        """Test validate_file_size() with valid file size."""
        test_file = tmp_path / FILENAME
        content = "# Test\n\n" + "X" * 300  # Create file > 250 bytes
        test_file.write_text(content)

        # Should not raise
        validate_file_size(str(test_file))

    def test_validate_file_size_fails_too_small(self, tmp_path):
        """Test validate_file_size() fails with file too small."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Test\n\nSmall.")

        with pytest.raises(ValueError, match="outside acceptable"):
            validate_file_size(str(test_file))

    def test_validate_file_size_fails_too_large(self, tmp_path):
        """Test validate_file_size() fails with file too large."""
        test_file = tmp_path / FILENAME
        content = "# Test\n\n" + "X" * 600
        test_file.write_text(content)

        with pytest.raises(ValueError, match="outside acceptable"):
            validate_file_size(str(test_file))


class TestValidateMarkdownFileOrchestration:
    """Tests for validate_markdown_file() orchestration function."""

    def test_validate_markdown_file_passes_valid_file(self, tmp_path):
        """Test validate_markdown_file() with completely valid file."""
        test_file = tmp_path / FILENAME
        # Create a valid file
        content = "# Test\n\n" + "X" * 100 + ". " + "Y" * 100 + ". " + "Z" * 50 + "."
        test_file.write_text(content, encoding="utf-8")

        # Should not raise
        validate_markdown_file(str(test_file))

    def test_validate_markdown_file_fails_on_missing_file(self, tmp_path):
        """Test validate_markdown_file() fails if file doesn't exist."""
        test_file = tmp_path / FILENAME

        with pytest.raises(FileNotFoundError):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_fails_format_error(self, tmp_path):
        """Test validate_markdown_file() fails on format error."""
        test_file = tmp_path / FILENAME
        test_file.write_text("No heading\n\nFirst. Second.")

        with pytest.raises(ValueError):
            validate_markdown_file(str(test_file))

    def test_validate_markdown_file_fails_encoding_error(self, tmp_path):
        """Test validate_markdown_file() fails on encoding error."""
        test_file = tmp_path / FILENAME
        # Create with BOM (invalid)
        test_file.write_bytes(b"\xef\xbb\xbf# Test\n\n" + b"X" * 200 + b". " + b"Y" * 100 + b".")

        with pytest.raises(ValueError):
            validate_markdown_file(str(test_file))


class TestExtractProseContent:
    """Tests for extract_prose_content() helper function."""

    def test_extract_prose_content_valid(self, tmp_path):
        """Test extracting prose from valid markdown."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Title\n\nProse content here.")

        prose = extract_prose_content(str(test_file))
        assert prose == "Prose content here."

    def test_extract_prose_content_multiline(self, tmp_path):
        """Test extracting multiline prose."""
        test_file = tmp_path / FILENAME
        test_file.write_text("# Title\n\nFirst line.\nSecond line.")

        prose = extract_prose_content(str(test_file))
        assert "First line." in prose
        assert "Second line." in prose


class TestCountSentences:
    """Tests for count_sentences() helper function."""

    def test_count_sentences_two(self):
        """Test counting 2 sentences."""
        prose = "First sentence. Second sentence."
        count = count_sentences(prose)
        assert count == 2

    def test_count_sentences_three(self):
        """Test counting 3 sentences."""
        prose = "First sentence. Second sentence. Third sentence."
        count = count_sentences(prose)
        assert count == 3

    def test_count_sentences_empty_raises(self):
        """Test that empty prose raises ValueError."""
        with pytest.raises(ValueError):
            count_sentences("")
