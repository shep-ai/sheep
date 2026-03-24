"""Tests for markdown file creation and validation functions."""

import os
import tempfile
from pathlib import Path

import pytest

# Import the functions from the script
import sys
script_path = Path(__file__).parent.parent.parent / "create_markdown_file_191.py"
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from create_markdown_file_191 import create_file, validate_file


class TestCreateFile:
    """Tests for create_file() function."""

    def test_creates_file_at_repository_root(self):
        """Test that create_file() creates test-1m1w18.md in the repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                result = create_file("test-1m1w18.md")

                assert result is True, "create_file() should return True on success"
                assert Path("test-1m1w18.md").exists(), "File should exist at repository root"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_h1_heading(self):
        """Test that file contains H1 markdown heading on first line."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                content = Path("test-1m1w18.md").read_text(encoding='utf-8')
                assert content.startswith("# "), "File should start with H1 heading"
            finally:
                os.chdir(original_cwd)

    def test_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                content = Path("test-1m1w18.md").read_text(encoding='utf-8')
                # Count periods to estimate sentence count
                # Should have 2-3 periods (2-3 sentences)
                period_count = content.count('.')
                assert 2 <= period_count <= 3, f"File should contain 2-3 sentences, found {period_count} periods"
            finally:
                os.chdir(original_cwd)

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                # Read as binary
                binary_content = Path("test-1m1w18.md").read_bytes()

                # Verify it can be decoded as UTF-8
                try:
                    decoded = binary_content.decode('utf-8')
                    assert isinstance(decoded, str)
                except UnicodeDecodeError:
                    pytest.fail("File is not valid UTF-8")
            finally:
                os.chdir(original_cwd)

    def test_file_has_no_utf8_bom(self):
        """Test that file does not have UTF-8 BOM (Byte Order Mark)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                binary_content = Path("test-1m1w18.md").read_bytes()
                # UTF-8 BOM is b'\xef\xbb\xbf'
                assert not binary_content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)

    def test_file_uses_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                binary_content = Path("test-1m1w18.md").read_bytes()
                # Should not contain CRLF (\r\n)
                assert b'\r\n' not in binary_content, "File should not have CRLF line endings"
                # Should contain LF (\n)
                assert b'\n' in binary_content, "File should have LF line endings"
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_typical_range(self):
        """Test that file size is approximately 400-600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                file_size = Path("test-1m1w18.md").stat().st_size
                # Spec requires 400-600 bytes
                assert 400 <= file_size <= 600, (
                    f"File size {file_size} bytes outside required range (400-600)"
                )
            finally:
                os.chdir(original_cwd)

    def test_file_contains_blank_line_after_heading(self):
        """Test that file has blank line separating heading from prose."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                content = Path("test-1m1w18.md").read_text(encoding='utf-8')
                # Should contain double newline (blank line)
                assert '\n\n' in content, "File should contain blank line after heading"
            finally:
                os.chdir(original_cwd)

    def test_returns_true_on_success(self):
        """Test that create_file() returns True on successful creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                result = create_file("test-1m1w18.md")

                assert result is True, "create_file() should return True on success"
            finally:
                os.chdir(original_cwd)

    def test_returns_none_if_file_exists(self):
        """Test that create_file() returns None if file already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Create file first time
                result1 = create_file("test-1m1w18.md")
                assert result1 is True, "First create_file() should return True"

                # Try to create same file again
                result2 = create_file("test-1m1w18.md")
                assert result2 is None, "Second create_file() should return None if file exists"
            finally:
                os.chdir(original_cwd)

    def test_does_not_overwrite_existing_file(self):
        """Test that create_file() does not overwrite an existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                # Create initial file
                create_file("test-1m1w18.md")
                original_content = Path("test-1m1w18.md").read_text(encoding='utf-8')
                original_mtime = Path("test-1m1w18.md").stat().st_mtime

                # Small delay to ensure mtime would differ
                import time
                time.sleep(0.01)

                # Try to create same file again
                result = create_file("test-1m1w18.md")
                assert result is None, "Should return None for existing file"

                # Verify content hasn't changed
                new_content = Path("test-1m1w18.md").read_text(encoding='utf-8')
                new_mtime = Path("test-1m1w18.md").stat().st_mtime

                assert new_content == original_content, "File content should not change"
                assert new_mtime == original_mtime, "File modification time should not change"
            finally:
                os.chdir(original_cwd)


class TestValidateFile:
    """Tests for validate_file() function."""

    def test_validates_correctly_created_file(self):
        """Test that validate_file() passes for a correctly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)
                create_file("test-1m1w18.md")

                result = validate_file("test-1m1w18.md")
                assert result is True
            finally:
                os.chdir(original_cwd)

    def test_rejects_missing_file(self):
        """Test that validate_file() raises error for non-existent file."""
        with pytest.raises(ValueError, match="does not exist"):
            validate_file("nonexistent.md")

    def test_rejects_file_without_h1_heading(self):
        """Test that validate_file() rejects file without H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # No heading
            content = "## Second Level\n\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(ValueError, match="H1 heading"):
                validate_file(path)

    def test_rejects_file_without_blank_line(self):
        """Test that validate_file() rejects file without blank line after heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # No blank line between heading and prose
            content = "# Title\nProse content. More content. Final content.\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(ValueError, match="must be blank"):
                validate_file(path)

    def test_rejects_file_with_wrong_sentence_count(self):
        """Test that validate_file() rejects file with wrong sentence count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Only 1 sentence
            content = "# Title\n\nOnly one sentence.\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(ValueError, match="2-3 sentences"):
                validate_file(path)

    def test_rejects_file_with_utf8_bom(self):
        """Test that validate_file() rejects file with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file with BOM
            content = "# Title\n\nFirst sentence. Second sentence. Third sentence.\n"
            path.write_bytes(b'\xef\xbb\xbf' + content.encode('utf-8'))

            with pytest.raises(ValueError, match="BOM"):
                validate_file(path)

    def test_rejects_file_with_crlf_line_endings(self):
        """Test that validate_file() rejects file with CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create file with CRLF
            content = "# Title\r\n\r\nFirst sentence. Second sentence. Third sentence.\r\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(ValueError, match="CRLF"):
                validate_file(path)

    def test_rejects_file_too_small(self):
        """Test that validate_file() rejects file smaller than 400 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create very small file
            content = "# Title\n\nSmall. Content. Here.\n"
            path.write_bytes(content.encode('utf-8'))

            with pytest.raises(ValueError, match="400-600 byte"):
                validate_file(path)

    def test_rejects_file_too_large(self):
        """Test that validate_file() rejects file larger than 600 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.md"
            # Create very large file with exactly 3 sentences but long content
            # Make each sentence very long to exceed 600 bytes while keeping sentence count at 3
            long_sentence_part = "x" * 200
            prose = f"This is the first sentence about {long_sentence_part}. This is the second sentence about {long_sentence_part}. This is the third sentence about {long_sentence_part}."
            content = f"# Title\n\n{prose}\n"
            path.write_bytes(content.encode('utf-8'))

            file_size = path.stat().st_size
            assert file_size > 600, f"Test file must be > 600 bytes, got {file_size}"

            with pytest.raises(ValueError, match="400-600 byte"):
                validate_file(path)


class TestIntegration:
    """Integration tests for file creation and validation."""

    def test_create_and_validate_workflow(self):
        """Test complete workflow: create file and validate it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                # Create file
                result = create_file("test-1m1w18.md")
                assert result is True, "File creation should succeed"
                assert Path("test-1m1w18.md").exists(), "File should exist"

                # Validate file
                validation_result = validate_file("test-1m1w18.md")
                assert validation_result is True, "Validation should pass"
            finally:
                os.chdir(original_cwd)

    def test_multiple_validations_pass(self):
        """Test that a created file passes validation multiple times."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                create_file("test-1m1w18.md")

                # Validate multiple times
                for i in range(3):
                    result = validate_file("test-1m1w18.md")
                    assert result is True, f"Validation failed on attempt {i+1}"
            finally:
                os.chdir(original_cwd)

    def test_file_structure_matches_specification(self):
        """Test that created file matches specification requirements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_cwd = Path.cwd()
            try:
                os.chdir(tmpdir)

                create_file("test-1m1w18.md")
                content = Path("test-1m1w18.md").read_text(encoding='utf-8')

                # Specification: # Heading\n\n<3 sentences>
                lines = content.split('\n')

                # First line should be heading
                assert lines[0].startswith('# '), "First line should be H1 heading"

                # Second line should be empty (blank line)
                assert lines[1] == '', "Second line should be empty (blank line separator)"

                # Remaining lines should contain prose
                prose_lines = lines[2:]
                prose = '\n'.join(prose_lines).strip()
                assert len(prose) > 0, "Prose content should be present"

                # Should have exactly 3 sentences (3 periods)
                period_count = content.count('.')
                assert period_count == 3, f"Should have exactly 3 sentences, found {period_count}"

                # Validate overall file passes validation
                assert validate_file("test-1m1w18.md") is True
            finally:
                os.chdir(original_cwd)
