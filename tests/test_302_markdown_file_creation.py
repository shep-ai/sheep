"""Tests for feature 302: Create markdown file test-94uqvv.md with comprehensive validation."""

import os
from pathlib import Path

import pytest

from create_file_302 import (
    FILENAME,
    create_file,
    validate_encoding,
    validate_structure,
)


class TestFile302Encoding:
    """Tests for file encoding validation (task-2: validate_encoding)."""

    def test_file_without_bom(self, tmp_path):
        """Test that file does not contain UTF-8 BOM (0xEF 0xBB 0xBF)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create the file
            filepath = create_file()

            # Validate encoding
            assert validate_encoding(filepath) is True

            # Verify no BOM in file bytes
            content_bytes = filepath.read_bytes()
            assert not content_bytes.startswith(b"\xef\xbb\xbf"), "File should not contain UTF-8 BOM"

        finally:
            os.chdir(original_cwd)

    def test_file_uses_lf_not_crlf(self, tmp_path):
        """Test that file uses Unix LF (0x0A) not CRLF (0x0D 0x0A) line endings."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create the file
            filepath = create_file()

            # Validate encoding
            assert validate_encoding(filepath) is True

            # Verify LF only, no CRLF
            content_bytes = filepath.read_bytes()
            assert b"\r\n" not in content_bytes, "File should not contain CRLF line endings"
            assert b"\n" in content_bytes, "File should contain LF line endings"

        finally:
            os.chdir(original_cwd)

    def test_validate_encoding_detects_bom(self, tmp_path):
        """Test that validate_encoding() detects and rejects files with BOM."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a file with BOM
            filepath = Path(FILENAME)
            content_with_bom = b"\xef\xbb\xbf" + "# Test\n\nContent here.\n".encode("utf-8")
            filepath.write_bytes(content_with_bom)

            # Validation should fail
            with pytest.raises(AssertionError, match="BOM"):
                validate_encoding(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_encoding_detects_crlf(self, tmp_path):
        """Test that validate_encoding() detects and rejects files with CRLF line endings."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a file with CRLF
            filepath = Path(FILENAME)
            content_with_crlf = "# Test\r\n\r\nContent here.\r\n".encode("utf-8")
            filepath.write_bytes(content_with_crlf)

            # Validation should fail
            with pytest.raises(AssertionError, match="CRLF|line ending"):
                validate_encoding(filepath)

        finally:
            os.chdir(original_cwd)


class TestFile302Structure:
    """Tests for file structure validation (task-3: validate_structure)."""

    def test_h1_heading_on_line_1(self, tmp_path):
        """Test that H1 heading exists on line 1."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify H1 heading
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert lines[0].startswith("# "), "First line should start with '# ' (H1 heading)"

        finally:
            os.chdir(original_cwd)

    def test_blank_line_separator(self, tmp_path):
        """Test that blank line exists between heading and prose (line 2)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify blank line
            content = filepath.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert lines[1] == "", "Line 2 should be blank (blank line separator)"

        finally:
            os.chdir(original_cwd)

    def test_sentence_count_2_to_3(self, tmp_path):
        """Test that prose contains 2-3 sentences (detected by period count)."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify sentence count
            content = filepath.read_text(encoding="utf-8")
            # Extract prose (after first blank line)
            parts = content.split("\n\n", 1)
            if len(parts) > 1:
                prose = parts[1].strip()
                sentence_count = prose.count(".")
                assert 2 <= sentence_count <= 3, f"Prose should have 2-3 sentences, found {sentence_count}"

        finally:
            os.chdir(original_cwd)

    def test_file_size_in_range(self, tmp_path):
        """Test that file size is between 300-800 bytes."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()
            assert validate_structure(filepath) is True

            # Verify file size
            file_size = filepath.stat().st_size
            assert 300 < file_size < 800, f"File size {file_size} should be between 300-800 bytes"

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_missing_h1(self, tmp_path):
        """Test that validate_structure() rejects files without H1 heading."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file without H1
            filepath = Path(FILENAME)
            filepath.write_text("No heading here.\n\nJust prose content here.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="H1|heading"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_missing_blank_line(self, tmp_path):
        """Test that validate_structure() rejects files without blank line separator."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file without blank line
            filepath = Path(FILENAME)
            filepath.write_text("# Title\nProse content.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="blank line|line 2"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_too_few_sentences(self, tmp_path):
        """Test that validate_structure() rejects prose with fewer than 2 sentences."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file with only 1 sentence
            filepath = Path(FILENAME)
            filepath.write_text("# Title\n\nOnly one sentence.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="2-3 sentences|sentence"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_too_many_sentences(self, tmp_path):
        """Test that validate_structure() rejects prose with more than 3 sentences."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create file with 4 sentences
            filepath = Path(FILENAME)
            filepath.write_text(
                "# Title\n\nFirst sentence. Second sentence. Third sentence. Fourth sentence.\n",
                encoding="utf-8"
            )

            # Validation should fail
            with pytest.raises(AssertionError, match="2-3 sentences|sentence"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_file_too_small(self, tmp_path):
        """Test that validate_structure() rejects files smaller than 300 bytes."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a small file
            filepath = Path(FILENAME)
            filepath.write_text("# T\n\nA. B.\n", encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="size|bytes"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)

    def test_validate_structure_rejects_file_too_large(self, tmp_path):
        """Test that validate_structure() rejects files larger than 800 bytes."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            # Create a large file with 2-3 sentences to pass sentence count check
            filepath = Path(FILENAME)
            large_content = "# Title\n\n" + ("A " * 250) + ". " + ("B " * 250) + ". " + ("C " * 50) + ".\n"
            filepath.write_text(large_content, encoding="utf-8")

            # Validation should fail
            with pytest.raises(AssertionError, match="size|bytes"):
                validate_structure(filepath)

        finally:
            os.chdir(original_cwd)


class TestFile302IntegrationValidation:
    """Integration tests for validate_encoding and validate_structure together."""

    def test_both_validations_pass_on_created_file(self, tmp_path):
        """Test that both validate_encoding and validate_structure pass on created file."""
        original_cwd = Path.cwd()
        try:
            os.chdir(tmp_path)

            filepath = create_file()

            # Both validations should pass
            assert validate_encoding(filepath) is True
            assert validate_structure(filepath) is True

        finally:
            os.chdir(original_cwd)
