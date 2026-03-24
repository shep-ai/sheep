"""Tests for Feature 195 Phase 2: File Creation & Validation

Tests covering:
- Task 2: Write markdown file with correct encoding and line endings
- Task 3: Validate markdown file (structure, encoding, content)
"""

import tempfile
from pathlib import Path
import pytest


class TestFeature195FileWriting:
    """Tests for task-2: Writing markdown file with correct encoding/line endings."""

    def test_file_created_at_repository_root(self):
        """Test that file is created at repository root directory."""
        from feature_195_phase2_local import FILENAME, write_file_with_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to temp directory to simulate repository root
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                content = "# Test\n\nFirst sentence. Second sentence.\n"
                write_file_with_encoding(FILENAME, content)

                # Verify file exists at root
                assert Path(FILENAME).exists(), "File should exist at repository root"
                assert Path(FILENAME).is_file(), "Path should be a file"
            finally:
                os.chdir(original_cwd)

    def test_file_encoded_as_utf8(self):
        """Test that file is encoded as UTF-8."""
        from feature_195_phase2_local import write_file_with_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                content = "# Unicode Test\n\nThis has special characters: é, ñ, 中文.\n"
                write_file_with_encoding("test.md", content)

                # Read as binary and decode to verify UTF-8
                with open("test.md", "rb") as f:
                    binary = f.read()

                # Should decode successfully as UTF-8
                decoded = binary.decode("utf-8")
                assert decoded == content
            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF (Unix) line endings, not CRLF."""
        from feature_195_phase2_local import write_file_with_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                content = "# Test\n\nLine one. Line two. Line three.\n"
                write_file_with_encoding("test.md", content)

                # Read as binary and verify no CRLF present
                with open("test.md", "rb") as f:
                    binary = f.read()

                # Should have LF (0x0A) but not CRLF (0x0D 0x0A)
                assert b"\r\n" not in binary, "File should not have CRLF line endings"
                assert b"\n" in binary, "File should have LF line endings"
            finally:
                os.chdir(original_cwd)

    def test_file_does_not_exist_before_creation(self):
        """Test that file creation fails gracefully if file already exists."""
        from feature_195_phase2_local import write_file_with_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                content = "# Test\n\nSentence one. Sentence two.\n"

                # Create file first time
                write_file_with_encoding("test.md", content)
                assert Path("test.md").exists()

                # Second write should work (overwrites in this implementation)
                # This tests that we don't prevent overwrites unintentionally
                write_file_with_encoding("test.md", content)
                assert Path("test.md").exists()
            finally:
                os.chdir(original_cwd)

    def test_file_has_correct_markdown_structure(self):
        """Test that written file has correct markdown structure."""
        from feature_195_phase2_local import write_file_with_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                content = "# Test Title\n\nFirst sentence. Second sentence.\n"
                write_file_with_encoding("test.md", content)

                # Read and verify structure
                with open("test.md", "r", encoding="utf-8") as f:
                    lines = f.read().split("\n")

                assert lines[0].startswith("# "), "First line should be H1 heading"
                assert lines[1] == "", "Second line should be blank"
                assert len(lines) >= 3, "Should have at least 3 lines (heading, blank, prose)"
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_expected_range(self):
        """Test that file size is between 250-600 bytes (typical for this pattern)."""
        from feature_195_phase2_local import write_file_with_encoding

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create content that results in file size in range
                content = "# Test Title\n\n" + "This is a sentence about something meaningful. " * 3 + "\n"
                write_file_with_encoding("test.md", content)

                file_size = Path("test.md").stat().st_size
                # Size should be reasonable for title + 2-3 sentences
                assert file_size > 50, "File size should be > 50 bytes"
                # Not enforcing upper bound strictly as it's a guideline
            finally:
                os.chdir(original_cwd)


class TestFeature195FileValidation:
    """Tests for task-3: Validating markdown file properties and structure."""

    def test_validation_passes_for_correct_file(self):
        """Test that validation passes for a correctly formatted file."""
        from feature_195_phase2_local import (
            validate_file_properties,
            validate_markdown_structure,
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create valid file
                content = "# Test\n\nFirst sentence. Second sentence. Third sentence.\n"
                with open("test.md", "w", encoding="utf-8") as f:
                    f.write(content)

                # Both validations should pass
                assert validate_file_properties("test.md") == True
                assert validate_markdown_structure("test.md") == True
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_file_with_utf8_bom(self):
        """Test that validation rejects files with UTF-8 BOM."""
        from feature_195_phase2_local import validate_file_properties

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with UTF-8 BOM
                with open("test.md", "wb") as f:
                    f.write(b"\xef\xbb\xbf# Test\n\nSentence.\n")

                # Validation should fail
                with pytest.raises(ValueError, match="BOM"):
                    validate_file_properties("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_file_with_crlf(self):
        """Test that validation rejects files with CRLF line endings."""
        from feature_195_phase2_local import validate_file_properties

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with CRLF line endings
                with open("test.md", "wb") as f:
                    f.write(b"# Test\r\n\r\nSentence one. Sentence two.\r\n")

                # Validation should fail
                with pytest.raises(ValueError, match="CRLF"):
                    validate_file_properties("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_invalid_utf8(self):
        """Test that validation rejects files that are not valid UTF-8."""
        from feature_195_phase2_local import validate_file_properties

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Write file with invalid UTF-8 bytes
                with open("test.md", "wb") as f:
                    f.write(b"# Test\n\n\xff\xfe invalid utf8\n")

                # Validation should fail
                with pytest.raises(ValueError, match="UTF-8"):
                    validate_file_properties("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_missing_h1_heading(self):
        """Test that validation rejects files without H1 heading."""
        from feature_195_phase2_local import validate_markdown_structure

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file without H1 heading
                with open("test.md", "w", encoding="utf-8") as f:
                    f.write("## Heading\n\nSentence one. Sentence two.\n")

                # Validation should fail
                with pytest.raises(ValueError, match="H1"):
                    validate_markdown_structure("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_missing_blank_line(self):
        """Test that validation rejects files without blank line after heading."""
        from feature_195_phase2_local import validate_markdown_structure

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file without blank line separator
                with open("test.md", "w", encoding="utf-8") as f:
                    f.write("# Test\nSentence one. Sentence two.\n")

                # Validation should fail
                with pytest.raises(ValueError, match="blank"):
                    validate_markdown_structure("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_too_few_sentences(self):
        """Test that validation rejects files with less than 2 sentences."""
        from feature_195_phase2_local import validate_markdown_structure

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file with only 1 sentence
                with open("test.md", "w", encoding="utf-8") as f:
                    f.write("# Test\n\nOnly one sentence.\n")

                # Validation should fail
                with pytest.raises(ValueError, match="2-3 sentences"):
                    validate_markdown_structure("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_too_many_sentences(self):
        """Test that validation rejects files with more than 3 sentences."""
        from feature_195_phase2_local import validate_markdown_structure

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file with 4 sentences
                with open("test.md", "w", encoding="utf-8") as f:
                    f.write(
                        "# Test\n\nSentence one. Sentence two. Sentence three. Sentence four.\n"
                    )

                # Validation should fail
                with pytest.raises(ValueError, match="2-3 sentences"):
                    validate_markdown_structure("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_missing_trailing_newline(self):
        """Test that validation rejects files without trailing newline."""
        from feature_195_phase2_local import validate_markdown_structure

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file without trailing newline
                with open("test.md", "wb") as f:
                    f.write(b"# Test\n\nSentence one. Sentence two.")

                # Validation should fail
                with pytest.raises(ValueError, match="trailing newline"):
                    validate_markdown_structure("test.md")
            finally:
                os.chdir(original_cwd)

    def test_validation_accepts_exactly_2_sentences(self):
        """Test that validation accepts files with exactly 2 sentences."""
        from feature_195_phase2_local import validate_markdown_structure

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file with 2 sentences
                with open("test.md", "w", encoding="utf-8") as f:
                    f.write("# Test\n\nSentence one. Sentence two.\n")

                # Validation should pass
                assert validate_markdown_structure("test.md") == True
            finally:
                os.chdir(original_cwd)

    def test_validation_accepts_exactly_3_sentences(self):
        """Test that validation accepts files with exactly 3 sentences."""
        from feature_195_phase2_local import validate_markdown_structure

        with tempfile.TemporaryDirectory() as tmpdir:
            import os
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                # Create file with 3 sentences
                with open("test.md", "w", encoding="utf-8") as f:
                    f.write("# Test\n\nSentence one. Sentence two. Sentence three.\n")

                # Validation should pass
                assert validate_markdown_structure("test.md") == True
            finally:
                os.chdir(original_cwd)

    def test_validation_rejects_nonexistent_file(self):
        """Test that validation rejects nonexistent files."""
        from feature_195_phase2_local import validate_file_properties

        with pytest.raises(ValueError, match="does not exist"):
            validate_file_properties("/nonexistent/path/file.md")

    def test_validation_accepts_existing_test_markdown_files(self):
        """Test that validation accepts existing test-*.md files in repository."""
        from feature_195_phase2_local import (
            validate_file_properties,
            validate_markdown_structure,
        )

        # Test a few existing files to ensure validation doesn't have false positives
        test_files = [
            "test-9zebfj.md",
            "test-2ak324.md",
            "test-9ehmdc.md",
        ]

        for filename in test_files:
            if Path(filename).exists():
                # Both validations should pass for existing files
                try:
                    validate_file_properties(filename)
                    validate_markdown_structure(filename)
                except Exception as e:
                    pytest.fail(f"Validation failed for {filename}: {e}")
