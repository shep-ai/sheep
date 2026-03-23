"""
Test suite for markdown file creation feature 175.

Tests cover file creation, validation, and git operations.
Uses tempfile for isolated testing without affecting the repository.
"""
import tempfile
from pathlib import Path
import pytest
import create_markdown_file


class TestFileCreation:
    """Tests for file creation with correct structure and encoding."""

    def test_file_created(self):
        """Test that markdown file is created in the repository root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                # Change to temp directory for isolated test
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                assert (tmpdir_path / create_markdown_file.FILENAME).exists()
            finally:
                os.chdir(original_cwd)

    def test_file_has_heading(self):
        """Test that file has H1 heading on line 1."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                assert lines[0].startswith('# ')
                assert len(lines[0]) > 2  # Title is not empty
            finally:
                os.chdir(original_cwd)

    def test_file_has_blank_line(self):
        """Test that file has blank line on line 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                assert lines[1] == ''
            finally:
                os.chdir(original_cwd)

    def test_file_has_prose(self):
        """Test that file has prose content starting on line 3."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_text()
                lines = content.split('\n')

                # Lines 3+ should have content
                prose_lines = lines[2:]
                prose_content = '\n'.join(prose_lines).strip()
                assert len(prose_content) > 0
            finally:
                os.chdir(original_cwd)

    def test_file_ends_with_newline(self):
        """Test that file ends with newline character."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert content.endswith(b'\n')
            finally:
                os.chdir(original_cwd)

    def test_file_utf8_encoding(self):
        """Test that file uses UTF-8 encoding (can be read as UTF-8)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Should not raise UnicodeDecodeError
                (tmpdir_path / create_markdown_file.FILENAME).read_text(encoding='utf-8')
            finally:
                os.chdir(original_cwd)

    def test_file_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert b'\r\n' not in content, "File should use LF, not CRLF"
            finally:
                os.chdir(original_cwd)


class TestValidation:
    """Tests for file validation logic."""

    def test_validate_accepts_valid_file(self):
        """Test that validation accepts a properly created file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                # Should not raise any exception
                create_markdown_file.validate_file(create_markdown_file.FILENAME)
            finally:
                os.chdir(original_cwd)

    def test_no_utf8_bom(self):
        """Test that file does not have UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert not content.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_bom(self):
        """Test that validation rejects files with UTF-8 BOM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a file with BOM
                test_file = tmpdir_path / "test-bom.md"
                content = f"# {create_markdown_file.TITLE}\n\n{create_markdown_file.PROSE}\n"
                # Write with BOM by using utf-8-sig encoding
                test_file.write_text(content, encoding='utf-8-sig', newline='\n')

                # Validation should raise ValueError
                with pytest.raises(ValueError, match="UTF-8 BOM"):
                    create_markdown_file.validate_file("test-bom.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_crlf(self):
        """Test that validation rejects files with CRLF line endings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a file with CRLF
                test_file = tmpdir_path / "test-crlf.md"
                content = f"# {create_markdown_file.TITLE}\r\n\r\n{create_markdown_file.PROSE}\r\n"
                test_file.write_bytes(content.encode('utf-8'))

                # Validation should raise ValueError
                with pytest.raises(ValueError, match="CRLF"):
                    create_markdown_file.validate_file("test-crlf.md")
            finally:
                os.chdir(original_cwd)

    def test_lf_line_endings(self):
        """Test that file uses Unix LF line endings (no CRLF)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                content = (tmpdir_path / create_markdown_file.FILENAME).read_bytes()

                assert b'\r\n' not in content, "File should use LF, not CRLF"
            finally:
                os.chdir(original_cwd)


class TestStructureValidation:
    """Tests for file structure and size validation."""

    def test_validate_has_heading(self):
        """Test that validation checks for H1 heading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without heading
                test_file = tmpdir_path / "test-no-heading.md"
                test_file.write_text("No heading here\n\nSome content.\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="H1 heading"):
                    create_markdown_file.validate_file("test-no-heading.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_has_blank_line(self):
        """Test that validation checks for blank line on line 2."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without blank line after heading
                test_file = tmpdir_path / "test-no-blank.md"
                test_file.write_text("# Title\nContent without blank line.\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="blank line"):
                    create_markdown_file.validate_file("test-no-blank.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_has_prose(self):
        """Test that validation checks for prose content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without prose content
                test_file = tmpdir_path / "test-no-prose.md"
                test_file.write_text("# Title\n\n\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="prose"):
                    create_markdown_file.validate_file("test-no-prose.md")
            finally:
                os.chdir(original_cwd)

    def test_file_size_in_range(self):
        """Test that validation checks file size within 300-800 byte range."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                create_markdown_file.create_file()

                file_size = (tmpdir_path / create_markdown_file.FILENAME).stat().st_size

                assert 300 <= file_size <= 800, f"File size {file_size} not in range 300-800"
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_too_small(self):
        """Test that validation rejects files under 300 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a small file with valid structure but still under 300 bytes
                # This is hard to achieve with real prose, so test with a minimal but valid structure
                test_file = tmpdir_path / "test-tiny.md"
                small_content = "# Title\n\nFirst. Second. Third.\n"
                test_file.write_text(small_content, encoding='utf-8', newline='\n')

                file_size = test_file.stat().st_size
                if file_size < 300:
                    # If it's still under 300, expect size error
                    with pytest.raises(ValueError, match="minimum is 300"):
                        create_markdown_file.validate_file("test-tiny.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_too_large(self):
        """Test that validation rejects files over 800 bytes."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create a large file with exactly 3 sentences but over 800 bytes
                test_file = tmpdir_path / "test-huge.md"
                # Use 3 long sentences to exceed 800 bytes
                sentence1 = "This is the first very long sentence " * 8  # ~280 bytes
                sentence2 = "This is the second very long sentence " * 8  # ~280 bytes
                sentence3 = "This is the third very long sentence " * 8  # ~280 bytes
                large_prose = f"{sentence1}. {sentence2}. {sentence3}."
                large_content = f"# A Title\n\n{large_prose}\n"
                test_file.write_text(large_content, encoding='utf-8', newline='\n')

                file_size = test_file.stat().st_size
                # Only test if file is actually over 800 bytes
                if file_size > 800:
                    with pytest.raises(ValueError, match="maximum is 800"):
                        create_markdown_file.validate_file("test-huge.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_wrong_sentence_count(self):
        """Test that validation rejects files with wrong sentence count."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file with only 1 sentence
                test_file = tmpdir_path / "test-one-sentence.md"
                test_file.write_text("# Title\n\nOnly one sentence.\n", encoding='utf-8', newline='\n')

                with pytest.raises(ValueError, match="1 sentences.*expected 2-3"):
                    create_markdown_file.validate_file("test-one-sentence.md")
            finally:
                os.chdir(original_cwd)

    def test_validate_rejects_no_trailing_newline(self):
        """Test that validation rejects files without trailing newline."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            original_cwd = Path.cwd()
            try:
                import os
                os.chdir(tmpdir_path)

                # Create file without trailing newline
                test_file = tmpdir_path / "test-no-newline.md"
                # Use write_bytes to avoid automatic newline addition
                content = "# Title\n\nFirst sentence. Second sentence. Third sentence."
                test_file.write_bytes(content.encode('utf-8'))

                with pytest.raises(ValueError, match="does not end with newline"):
                    create_markdown_file.validate_file("test-no-newline.md")
            finally:
                os.chdir(original_cwd)
