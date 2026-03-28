#!/usr/bin/env python3
"""
Tests for feature 251: markdown-file-creation-5b29b2

Tests for three tasks:
- Task 1: Create markdown file with proper encoding and line endings
- Task 2: Validate file structure (heading, blank line, sentences)
- Task 3: Validate file encoding (UTF-8) and line endings (LF)
"""

import re
import tempfile
import pytest
from pathlib import Path
from create_markdown_file_251 import (
    create_file,
    validate_structure,
    validate_encoding_and_line_endings,
    validate_file_size,
    FILENAME,
    TITLE,
    PROSE,
    HEADING_PATTERN,
)


class TestTask1FileCreation:
    """Tests for Task 1: Create markdown file with proper encoding and line endings."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file does not exist initially (defensive check)."""
        # Change to temp directory for this test
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            file_path = Path(FILENAME)
            assert not file_path.exists(), "File should not exist before creation"
        finally:
            import os
            os.chdir(original_cwd)

    def test_create_file_returns_path(self, tmp_path):
        """Test that create_file returns a Path object."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            result = create_file()
            assert isinstance(result, Path), "create_file should return Path object"
            assert result.name == FILENAME, f"File name should be {FILENAME}"
        finally:
            import os
            os.chdir(original_cwd)

    def test_create_file_exists_after_creation(self, tmp_path):
        """Test that file exists after creation."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            file_path = Path(FILENAME)
            assert file_path.exists(), "File should exist after creation"
        finally:
            import os
            os.chdir(original_cwd)

    def test_file_contains_heading(self, tmp_path):
        """Test that file contains H1 heading on first line."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            content = Path(FILENAME).read_text(encoding="utf-8")
            lines = content.split("\n")

            assert len(lines) > 0, "File should have content"
            assert lines[0].startswith("# "), "First line should be H1 heading (# )"
            assert TITLE in lines[0], f"Heading should contain title: {TITLE}"
        finally:
            import os
            os.chdir(original_cwd)

    def test_file_contains_blank_line(self, tmp_path):
        """Test that file contains blank line after heading."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            content = Path(FILENAME).read_text(encoding="utf-8")
            lines = content.split("\n")

            assert len(lines) >= 2, "File should have at least 2 lines"
            assert lines[1] == "", "Second line should be blank"
        finally:
            import os
            os.chdir(original_cwd)

    def test_file_contains_prose_content(self, tmp_path):
        """Test that file contains prose content after blank line."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            content = Path(FILENAME).read_text(encoding="utf-8")
            lines = content.split("\n")

            assert len(lines) >= 3, "File should have heading, blank line, and prose"
            prose = "\n".join(lines[2:]).strip()
            assert len(prose) > 0, "Prose content should not be empty"
            assert PROSE in prose, "Prose should contain expected content"
        finally:
            import os
            os.chdir(original_cwd)

    def test_file_is_utf8_encoded(self, tmp_path):
        """Test that file is UTF-8 encoded."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            file_bytes = Path(FILENAME).read_bytes()

            # Should decode without error as UTF-8
            decoded = file_bytes.decode("utf-8")
            assert len(decoded) > 0, "File should contain text"
        finally:
            import os
            os.chdir(original_cwd)

    def test_file_has_lf_line_endings(self, tmp_path):
        """Test that file uses LF line endings (not CRLF)."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            file_bytes = Path(FILENAME).read_bytes()

            # Should not contain CRLF
            assert b"\r\n" not in file_bytes, "File should not contain CRLF"
            # Should contain LF
            assert b"\n" in file_bytes, "File should contain LF line endings"
        finally:
            import os
            os.chdir(original_cwd)

    def test_file_size_in_range(self, tmp_path):
        """Test that file size is approximately 400-600 bytes."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            file_bytes = Path(FILENAME).read_bytes()
            file_size = len(file_bytes)

            assert 400 <= file_size <= 600, f"File size {file_size} should be 400-600 bytes"
        finally:
            import os
            os.chdir(original_cwd)

    def test_create_file_raises_if_exists(self, tmp_path):
        """Test that create_file raises FileExistsError if file already exists."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file once
            create_file()

            # Attempt to create again should raise
            with pytest.raises(FileExistsError):
                create_file()
        finally:
            import os
            os.chdir(original_cwd)


class TestTask2StructureValidation:
    """Tests for Task 2: Validate file structure (heading, blank line, sentences)."""

    def test_validate_structure_nonexistent_file(self, tmp_path):
        """Test that validate_structure returns False for non-existent file."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            result = validate_structure(Path("nonexistent.md"))
            assert result is False, "Should return False for non-existent file"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_structure_valid_file(self, tmp_path):
        """Test that validate_structure returns True for valid file."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            result = validate_structure(Path(FILENAME))
            assert result is True, "Should return True for valid file"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_structure_malformed_heading(self, tmp_path):
        """Test that validate_structure fails if first line is not H1 heading."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file with wrong heading (## instead of #)
            content = "## Wrong Heading\n\nProse content here."
            Path(FILENAME).write_text(content, encoding="utf-8")

            result = validate_structure(Path(FILENAME))
            assert result is False, "Should fail for malformed heading"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_structure_no_blank_line(self, tmp_path):
        """Test that validate_structure fails if there's no blank line after heading."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file without blank line
            content = "# Heading\nProse content here."
            Path(FILENAME).write_text(content, encoding="utf-8")

            result = validate_structure(Path(FILENAME))
            assert result is False, "Should fail if no blank line after heading"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_structure_insufficient_sentences(self, tmp_path):
        """Test that validate_structure fails if prose has fewer than 2 sentences."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file with only 1 sentence
            content = "# Heading\n\nOnly one sentence."
            Path(FILENAME).write_text(content, encoding="utf-8")

            result = validate_structure(Path(FILENAME))
            assert result is False, "Should fail for fewer than 2 sentences"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_structure_too_many_sentences(self, tmp_path):
        """Test that validate_structure fails if prose has more than 3 sentences."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file with 4 sentences
            content = "# Heading\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence."
            Path(FILENAME).write_text(content, encoding="utf-8")

            result = validate_structure(Path(FILENAME))
            assert result is False, "Should fail for more than 3 sentences"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_structure_correct_sentence_count(self, tmp_path):
        """Test that validate_structure passes with exactly 2-3 sentences."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Test with 2 sentences
            content = "# Heading\n\nFirst sentence. Second sentence."
            Path(FILENAME).write_text(content, encoding="utf-8")
            result = validate_structure(Path(FILENAME))
            assert result is True, "Should pass with 2 sentences"

            # Test with 3 sentences
            content = "# Heading\n\nFirst sentence. Second sentence. Third sentence."
            Path(FILENAME).write_text(content, encoding="utf-8")
            result = validate_structure(Path(FILENAME))
            assert result is True, "Should pass with 3 sentences"
        finally:
            import os
            os.chdir(original_cwd)


class TestTask3EncodingValidation:
    """Tests for Task 3: Validate file encoding (UTF-8) and line endings (LF)."""

    def test_validate_encoding_nonexistent_file(self, tmp_path):
        """Test that validate_encoding_and_line_endings returns False for non-existent file."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            result = validate_encoding_and_line_endings(Path("nonexistent.md"))
            assert result is False, "Should return False for non-existent file"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_encoding_valid_utf8(self, tmp_path):
        """Test that validate_encoding_and_line_endings returns True for valid UTF-8."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            result = validate_encoding_and_line_endings(Path(FILENAME))
            assert result is True, "Should return True for valid UTF-8 with LF"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_encoding_crlf_line_endings(self, tmp_path):
        """Test that validate_encoding_and_line_endings fails for CRLF line endings."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file with CRLF line endings
            content = "# Heading\r\n\r\nProse content."
            Path(FILENAME).write_bytes(content.encode("utf-8"))

            result = validate_encoding_and_line_endings(Path(FILENAME))
            assert result is False, "Should fail for CRLF line endings"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_encoding_no_utf8_bom(self, tmp_path):
        """Test that validate_encoding_and_line_endings passes without UTF-8 BOM."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            file_bytes = Path(FILENAME).read_bytes()

            # Verify no BOM
            UTF8_BOM = b"\xef\xbb\xbf"
            assert not file_bytes.startswith(UTF8_BOM), "File should not have UTF-8 BOM"

            result = validate_encoding_and_line_endings(Path(FILENAME))
            assert result is True, "Should pass without UTF-8 BOM"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_encoding_contains_lf(self, tmp_path):
        """Test that validate_encoding_and_line_endings verifies LF is present."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            result = validate_encoding_and_line_endings(Path(FILENAME))
            assert result is True, "Should verify LF is present"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_encoding_rejects_non_utf8(self, tmp_path):
        """Test that validate_encoding_and_line_endings fails for non-UTF-8 encoding."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file with Latin-1 encoding containing non-UTF-8 byte sequence
            content = "# Heading\n\nContent with Latin-1: café"
            Path(FILENAME).write_bytes(content.encode("latin-1"))

            result = validate_encoding_and_line_endings(Path(FILENAME))
            assert result is False, "Should fail for non-UTF-8 encoding"
        finally:
            import os
            os.chdir(original_cwd)


class TestFileSizeValidation:
    """Tests for file size validation."""

    def test_validate_file_size_valid(self, tmp_path):
        """Test that validate_file_size returns True for 400-600 byte file."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            create_file()
            result = validate_file_size(Path(FILENAME))
            assert result is True, "Should pass for file in 400-600 byte range"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_file_size_too_small(self, tmp_path):
        """Test that validate_file_size fails for file smaller than 400 bytes."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file smaller than 400 bytes
            content = "# Title\n\nShort."
            Path(FILENAME).write_text(content, encoding="utf-8")

            result = validate_file_size(Path(FILENAME))
            assert result is False, "Should fail for file smaller than 400 bytes"
        finally:
            import os
            os.chdir(original_cwd)

    def test_validate_file_size_too_large(self, tmp_path):
        """Test that validate_file_size fails for file larger than 600 bytes."""
        original_cwd = Path.cwd()
        try:
            import os
            os.chdir(tmp_path)

            # Create file larger than 600 bytes
            large_prose = "Word " * 150  # Create a very long string
            content = f"# Title\n\n{large_prose}"
            Path(FILENAME).write_text(content, encoding="utf-8")

            result = validate_file_size(Path(FILENAME))
            assert result is False, "Should fail for file larger than 600 bytes"
        finally:
            import os
            os.chdir(original_cwd)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
