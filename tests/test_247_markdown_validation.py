"""Tests for feature 247: Structural validation and error handling for markdown file creation."""

from pathlib import Path

import pytest


class TestValidationFileExists:
    """Tests for file existence validation."""

    def test_file_not_exists_raises_exception(self, tmp_path):
        """Test that validation raises FileNotFoundError when file does not exist."""
        from src.create_markdown import validate_markdown_file

        nonexistent_file = tmp_path / "nonexistent.md"
        with pytest.raises(FileNotFoundError):
            validate_markdown_file(str(nonexistent_file))

    def test_file_exists_passes_initial_check(self, tmp_path):
        """Test that validation accepts existing file for further checks."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nSentence one. Sentence two.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise FileNotFoundError
        try:
            validate_markdown_file(str(test_file))
        except FileNotFoundError:
            pytest.fail("Should not raise FileNotFoundError for existing file")


class TestValidationHeadingFormat:
    """Tests for H1 heading format validation."""

    def test_heading_missing_raises_exception(self, tmp_path):
        """Test that validation raises exception when H1 heading is missing."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "This file has no heading.\n\nJust prose. Another sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="heading|missing"):
            validate_markdown_file(str(test_file))

    def test_heading_h2_instead_of_h1_raises_exception(self, tmp_path):
        """Test that validation rejects H2 (##) when H1 (#) is required."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "## Wrong Level Heading\n\nSentence one. Sentence two.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="heading|H1"):
            validate_markdown_file(str(test_file))

    def test_heading_missing_space_raises_exception(self, tmp_path):
        """Test that validation rejects #Heading (missing space after #)."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "#NoSpaceHeading\n\nSentence one. Sentence two.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="heading|format"):
            validate_markdown_file(str(test_file))

    def test_valid_h1_heading_passes(self, tmp_path):
        """Test that validation accepts valid H1 heading."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nSentence one. Sentence two.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise exception for heading check
        try:
            validate_markdown_file(str(test_file))
        except ValueError as e:
            if "heading" in str(e).lower():
                pytest.fail(f"Should accept valid H1 heading: {e}")


class TestValidationSentenceCount:
    """Tests for prose sentence count validation."""

    def test_zero_sentences_raises_exception(self, tmp_path):
        """Test that validation raises exception when prose has 0 sentences."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nNo sentences here just words\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="sentence|found 0"):
            validate_markdown_file(str(test_file))

    def test_one_sentence_raises_exception(self, tmp_path):
        """Test that validation raises exception when prose has only 1 sentence."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nOnly one sentence here.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="sentence|found 1"):
            validate_markdown_file(str(test_file))

    def test_four_sentences_raises_exception(self, tmp_path):
        """Test that validation raises exception when prose has 4 sentences."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError, match="sentence|found 4"):
            validate_markdown_file(str(test_file))

    def test_two_sentences_passes(self, tmp_path):
        """Test that validation accepts exactly 2 sentences."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nFirst sentence. Second sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise sentence count exception
        try:
            validate_markdown_file(str(test_file))
        except ValueError as e:
            if "sentence" in str(e).lower():
                pytest.fail(f"Should accept 2 sentences: {e}")

    def test_three_sentences_passes(self, tmp_path):
        """Test that validation accepts exactly 3 sentences."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise sentence count exception
        try:
            validate_markdown_file(str(test_file))
        except ValueError as e:
            if "sentence" in str(e).lower():
                pytest.fail(f"Should accept 3 sentences: {e}")

    def test_sentence_detection_with_exclamation_mark(self, tmp_path):
        """Test that sentence detection counts exclamation marks as sentence endings."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nFirst sentence! Second sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise sentence count exception
        try:
            validate_markdown_file(str(test_file))
        except ValueError as e:
            if "sentence" in str(e).lower():
                pytest.fail(f"Should count exclamation marks as sentence endings: {e}")

    def test_sentence_detection_with_question_mark(self, tmp_path):
        """Test that sentence detection counts question marks as sentence endings."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nIs this a question? This is a statement.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise sentence count exception
        try:
            validate_markdown_file(str(test_file))
        except ValueError as e:
            if "sentence" in str(e).lower():
                pytest.fail(f"Should count question marks as sentence endings: {e}")


class TestValidationEncoding:
    """Tests for UTF-8 encoding validation without BOM."""

    def test_utf8_without_bom_passes(self, tmp_path):
        """Test that file with UTF-8 encoding (no BOM) passes validation."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nFirst sentence. Second sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise encoding exception
        try:
            validate_markdown_file(str(test_file))
        except ValueError as e:
            if "encoding" in str(e).lower() or "bom" in str(e).lower():
                pytest.fail(f"Should accept UTF-8 without BOM: {e}")

    def test_utf8_with_bom_raises_exception(self, tmp_path):
        """Test that file with UTF-8 BOM signature is rejected."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nFirst sentence. Second sentence.\n"
        # Write with UTF-8-SIG encoding which adds BOM
        test_file.write_bytes(b'\xef\xbb\xbf' + content.encode('utf-8'))

        with pytest.raises(ValueError, match="encoding|BOM"):
            validate_markdown_file(str(test_file))


class TestValidationLineEndings:
    """Tests for Unix LF line ending validation."""

    def test_lf_line_endings_pass(self, tmp_path):
        """Test that file with LF line endings passes validation."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# Valid Heading\n\nFirst sentence. Second sentence.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise line ending exception
        try:
            validate_markdown_file(str(test_file))
        except ValueError as e:
            if "line ending" in str(e).lower() or "crlf" in str(e).lower():
                pytest.fail(f"Should accept LF line endings: {e}")

    def test_crlf_line_endings_raise_exception(self, tmp_path):
        """Test that file with CRLF line endings is rejected."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        # Write with CRLF line endings
        content = b"# Valid Heading\r\n\r\nFirst sentence. Second sentence.\r\n"
        test_file.write_bytes(content)

        with pytest.raises(ValueError, match="line ending|CRLF"):
            validate_markdown_file(str(test_file))


class TestValidationComplete:
    """Tests for complete file validation with all checks passing."""

    def test_valid_complete_file_passes_all_checks(self, tmp_path):
        """Test that a completely valid file passes all validation checks."""
        from src.create_markdown import validate_markdown_file

        test_file = tmp_path / "test.md"
        content = "# The Art of Meaningful Communication\n\nEffective communication is the foundation of human connection, enabling us to share ideas and understand different perspectives. When we listen carefully and express ourselves with clarity and empathy, we transform interactions from mere exchanges of information into genuine moments of understanding. This simple yet powerful practice creates lasting bonds between people.\n"
        test_file.write_text(content, encoding="utf-8")

        # Should not raise any exception
        result = validate_markdown_file(str(test_file))
        assert result is True

    def test_actual_test_440dhk_file_passes(self):
        """Test that the actual test-440dhk.md file passes validation."""
        from src.create_markdown import validate_markdown_file

        test_file = Path("test-440dhk.md")
        if test_file.exists():
            result = validate_markdown_file(str(test_file))
            assert result is True
