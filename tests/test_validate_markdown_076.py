"""Tests for Phase 2 Comprehensive Validation of markdown file for feature 076."""

import tempfile
from pathlib import Path

import pytest
from validate_markdown import (
    ValidationError,
    validate_encoding,
    validate_file,
    validate_file_size,
    validate_line_endings,
    validate_prose_sentences,
    validate_structure,
)


class TestValidateEncoding:
    """Tests for task-2: Validate UTF-8 encoding (no BOM)."""

    def test_validate_encoding_passes_for_utf8_without_bom(self):
        """Test that validate_encoding passes for UTF-8 file without BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nSentence. Sentence. Sentence.", encoding='utf-8')
            # Should not raise
            validate_encoding(test_file)

    def test_validate_encoding_rejects_utf8_with_bom(self):
        """Test that validate_encoding rejects UTF-8 file with BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write file with UTF-8 BOM
            bom_content = b'\xef\xbb\xbf' + b"# Heading\n\nSentence. Sentence. Sentence."
            test_file.write_bytes(bom_content)
            with pytest.raises(ValidationError, match="BOM"):
                validate_encoding(test_file)

    def test_validate_encoding_rejects_invalid_utf8(self):
        """Test that validate_encoding rejects invalid UTF-8 content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write invalid UTF-8 bytes
            test_file.write_bytes(b'\xff\xfe')
            with pytest.raises(ValidationError, match="not valid UTF-8"):
                validate_encoding(test_file)

    def test_validate_encoding_real_file(self):
        """Test validate_encoding against the actual test-3nslmx.md file."""
        test_file = Path("test-3nslmx.md")
        if test_file.exists():
            # Should not raise
            validate_encoding(test_file)


class TestValidateLineEndings:
    """Tests for task-3: Validate line endings (LF, no CRLF)."""

    def test_validate_line_endings_passes_for_unix_lf(self):
        """Test that validate_line_endings passes for Unix LF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nSentence. Sentence. Sentence.", encoding='utf-8')
            # Should not raise
            validate_line_endings(test_file)

    def test_validate_line_endings_rejects_windows_crlf(self):
        """Test that validate_line_endings rejects Windows CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write file with CRLF line endings
            crlf_content = "# Heading\r\n\r\nSentence. Sentence. Sentence.\r\n"
            test_file.write_bytes(crlf_content.encode('utf-8'))
            with pytest.raises(ValidationError, match="CRLF"):
                validate_line_endings(test_file)

    def test_validate_line_endings_detects_mixed_endings(self):
        """Test that validate_line_endings detects mixed CRLF in content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Write file with mixed line endings (has CRLF)
            mixed_content = "# Heading\n\nFirst line\r\nSecond line."
            test_file.write_bytes(mixed_content.encode('utf-8'))
            with pytest.raises(ValidationError, match="CRLF"):
                validate_line_endings(test_file)

    def test_validate_line_endings_real_file(self):
        """Test validate_line_endings against the actual test-3nslmx.md file."""
        test_file = Path("test-3nslmx.md")
        if test_file.exists():
            # Should not raise
            validate_line_endings(test_file)


class TestValidateStructure:
    """Tests for task-4: Validate file structure (H1 heading + blank line)."""

    def test_validate_structure_passes_for_correct_structure(self):
        """Test that validate_structure passes for correct markdown structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nSentence. Sentence. Sentence.", encoding='utf-8')
            # Should not raise
            validate_structure(test_file)

    def test_validate_structure_rejects_missing_h1(self):
        """Test that validate_structure rejects missing H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("Not a heading\n\nSentence. Sentence. Sentence.", encoding='utf-8')
            with pytest.raises(ValidationError, match="must start with"):
                validate_structure(test_file)

    def test_validate_structure_rejects_missing_blank_line(self):
        """Test that validate_structure rejects missing blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\nSentence. Sentence. Sentence.", encoding='utf-8')
            with pytest.raises(ValidationError, match="blank"):
                validate_structure(test_file)

    def test_validate_structure_rejects_missing_prose(self):
        """Test that validate_structure rejects missing prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\n", encoding='utf-8')
            with pytest.raises(ValidationError, match="empty"):
                validate_structure(test_file)

    def test_validate_structure_real_file(self):
        """Test validate_structure against the actual test-3nslmx.md file."""
        test_file = Path("test-3nslmx.md")
        if test_file.exists():
            # Should not raise
            validate_structure(test_file)


class TestValidateProSentences:
    """Tests for task-5: Validate prose content (2-3 sentences)."""

    def test_validate_prose_sentences_passes_for_two_sentences(self):
        """Test that validate_prose_sentences passes for 2 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nFirst sentence. Second sentence.", encoding='utf-8')
            # Should not raise
            validate_prose_sentences(test_file)

    def test_validate_prose_sentences_passes_for_three_sentences(self):
        """Test that validate_prose_sentences passes for 3 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nFirst sentence. Second sentence. Third sentence.", encoding='utf-8')
            # Should not raise
            validate_prose_sentences(test_file)

    def test_validate_prose_sentences_rejects_one_sentence(self):
        """Test that validate_prose_sentences rejects 1 sentence."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nOnly one sentence.", encoding='utf-8')
            with pytest.raises(ValidationError, match="2-3 sentences"):
                validate_prose_sentences(test_file)

    def test_validate_prose_sentences_rejects_four_sentences(self):
        """Test that validate_prose_sentences rejects 4 sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text(
                "# Heading\n\nFirst. Second. Third. Fourth.",
                encoding='utf-8'
            )
            with pytest.raises(ValidationError, match="2-3 sentences"):
                validate_prose_sentences(test_file)

    def test_validate_prose_sentences_counts_question_marks(self):
        """Test that validate_prose_sentences counts question marks as sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nQuestion? Statement. Exclamation!", encoding='utf-8')
            # Should not raise (counts as 3 sentences)
            validate_prose_sentences(test_file)

    def test_validate_prose_sentences_counts_exclamation_marks(self):
        """Test that validate_prose_sentences counts exclamation marks as sentences."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nExclamation! Statement.", encoding='utf-8')
            # Should not raise (counts as 2 sentences)
            validate_prose_sentences(test_file)

    def test_validate_prose_sentences_real_file(self):
        """Test validate_prose_sentences against the actual test-3nslmx.md file."""
        test_file = Path("test-3nslmx.md")
        if test_file.exists():
            # Should not raise
            validate_prose_sentences(test_file)


class TestValidateFileSize:
    """Tests for task-6: Validate file size (320-600 bytes)."""

    def test_validate_file_size_passes_for_valid_size(self):
        """Test that validate_file_size passes for file within range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Create content with 3 long sentences matching real test file pattern (~450 bytes)
            content = ("# Interesting Topic\n\n"
                      "Every moment of genuine discovery carries with it a sense of wonder and awakening that "
                      "transforms how we see the world and challenges our existing assumptions. "
                      "When we embrace curiosity and allow ourselves to explore new ideas without fear of failure, "
                      "we unlock creative possibilities and deepen our understanding of ourselves and others around us. "
                      "This feeling of discovery reminds us that growth happens not through passive acceptance, "
                      "but through active engagement with the unfamiliar and unknown.")
            test_file.write_text(content, encoding='utf-8')
            # Should not raise
            validate_file_size(test_file)

    def test_validate_file_size_rejects_too_small(self):
        """Test that validate_file_size rejects file smaller than 300 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# H\n\nS.", encoding='utf-8')
            with pytest.raises(ValidationError, match="outside acceptable range"):
                validate_file_size(test_file)

    def test_validate_file_size_rejects_too_large(self):
        """Test that validate_file_size rejects file larger than 600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Create content larger than 600 bytes
            large_content = "# Heading\n\n" + ("x" * 620)
            test_file.write_text(large_content, encoding='utf-8')
            with pytest.raises(ValidationError, match="outside acceptable range"):
                validate_file_size(test_file)

    def test_validate_file_size_boundary_at_320_bytes(self):
        """Test that validate_file_size accepts file at 320 byte boundary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Create content with 3 sentences that's around 320-350 bytes
            content = ("# Interesting Topic\n\n"
                      "Every moment of genuine discovery carries with it a profound sense of wonder and awakening that transforms how we see the world. "
                      "When we embrace curiosity and allow ourselves to explore new ideas without fear of failure, we unlock creative possibilities. "
                      "This feeling of discovery reminds us that growth happens through active engagement with the unknown.")
            test_file.write_text(content, encoding='utf-8')
            # Verify it's at least 320 bytes
            file_size = len(test_file.read_bytes())
            assert file_size >= 320, f"File size {file_size} is less than 320"
            # Should not raise
            validate_file_size(test_file)

    def test_validate_file_size_boundary_at_600_bytes(self):
        """Test that validate_file_size accepts file at 600 byte boundary."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Create content approximately 600 bytes
            content = "# Heading\n\n" + ("x" * 580)
            test_file.write_text(content, encoding='utf-8')
            # Should not raise
            validate_file_size(test_file)

    def test_validate_file_size_real_file(self):
        """Test validate_file_size against the actual test-3nslmx.md file."""
        test_file = Path("test-3nslmx.md")
        if test_file.exists():
            # Should not raise
            validate_file_size(test_file)


class TestValidateFileIntegration:
    """Integration tests for validate_file function."""

    def test_validate_file_passes_for_valid_file(self):
        """Test that validate_file passes for file with all valid properties."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Create content with 3 sentences that's around 400+ bytes (matching real test file)
            content = ("# Interesting Topic\n\n"
                      "Every moment of genuine discovery carries with it a sense of wonder and awakening that "
                      "transforms how we see the world and challenges our existing assumptions. "
                      "When we embrace curiosity and allow ourselves to explore new ideas without fear of failure, "
                      "we unlock creative possibilities and deepen our understanding of ourselves and others around us. "
                      "This feeling of discovery reminds us that growth happens not through passive acceptance, "
                      "but through active engagement with the unfamiliar and unknown.")
            test_file.write_text(content, encoding='utf-8')
            # Should not raise
            validate_file(test_file)

    def test_validate_file_runs_all_checks(self):
        """Test that validate_file runs all validation checks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            # Create content with 3 sentences that's around 400+ bytes (matching real test file)
            content = ("# Interesting Topic\n\n"
                      "Every moment of genuine discovery carries with it a sense of wonder and awakening that "
                      "transforms how we see the world and challenges our existing assumptions. "
                      "When we embrace curiosity and allow ourselves to explore new ideas without fear of failure, "
                      "we unlock creative possibilities and deepen our understanding of ourselves and others around us. "
                      "This feeling of discovery reminds us that growth happens not through passive acceptance, "
                      "but through active engagement with the unfamiliar and unknown.")
            test_file.write_text(content, encoding='utf-8')
            # This should execute all 5 validation checks without raising
            validate_file(test_file)

    def test_validate_file_raises_on_encoding_error(self):
        """Test that validate_file raises when encoding is invalid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            bom_content = b'\xef\xbb\xbf' + b"# Heading\n\nSentence. Sentence. Sentence."
            test_file.write_bytes(bom_content)
            with pytest.raises(ValidationError):
                validate_file(test_file)

    def test_validate_file_raises_on_line_ending_error(self):
        """Test that validate_file raises when line endings are wrong."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            crlf_content = "# Heading\r\n\r\nSentence. Sentence. Sentence.\r\n"
            test_file.write_bytes(crlf_content.encode('utf-8'))
            with pytest.raises(ValidationError):
                validate_file(test_file)

    def test_validate_file_raises_on_structure_error(self):
        """Test that validate_file raises when structure is invalid."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("Not a heading\n\nSentence. Sentence. Sentence.", encoding='utf-8')
            with pytest.raises(ValidationError):
                validate_file(test_file)

    def test_validate_file_raises_on_sentence_count_error(self):
        """Test that validate_file raises when sentence count is wrong."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# Heading\n\nOnly one sentence.", encoding='utf-8')
            with pytest.raises(ValidationError):
                validate_file(test_file)

    def test_validate_file_raises_on_size_error(self):
        """Test that validate_file raises when file size is wrong."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.md"
            test_file.write_text("# H\n\nS.", encoding='utf-8')
            with pytest.raises(ValidationError):
                validate_file(test_file)

    def test_validate_file_real_file(self):
        """Test validate_file against the actual test-3nslmx.md file."""
        test_file = Path("test-3nslmx.md")
        if test_file.exists():
            # Should pass all validation checks without raising
            validate_file(test_file)
            print(f"✓ {test_file.name} passed all validation checks")
