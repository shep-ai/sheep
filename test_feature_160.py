"""
Tests for Feature 160: Create markdown file test-9ehmdc.md with prose content
TDD approach: Tests are written first, then implementation follows
"""

import pytest
from pathlib import Path


class TestFileCreation:
    """Task 1: Create markdown file with H1 heading and prose content"""

    def test_file_does_not_exist_initially(self):
        """Test that test-9ehmdc.md does not exist yet"""
        file_path = Path("test-9ehmdc.md")
        if file_path.exists():
            file_path.unlink()  # Clean up for test isolation
        assert not file_path.exists()

    def test_file_exists_after_creation(self):
        """Test that file exists after creation"""
        from implementation_160 import create_markdown_file
        create_markdown_file()
        assert Path("test-9ehmdc.md").exists()

    def test_file_contains_h1_heading_on_first_line(self):
        """Test that first line contains exactly one H1 heading"""
        content = Path("test-9ehmdc.md").read_text(encoding="utf-8")
        lines = content.split("\n")
        first_line = lines[0]
        assert first_line.startswith("# "), "First line should start with '# '"
        assert first_line.count("#") == 1, "First line should contain exactly one '#'"

    def test_second_line_is_blank(self):
        """Test that second line is blank"""
        content = Path("test-9ehmdc.md").read_text(encoding="utf-8")
        lines = content.split("\n")
        assert len(lines) > 1, "File should have at least 2 lines"
        assert lines[1] == "", "Second line should be blank"

    def test_prose_content_follows_blank_line(self):
        """Test that 2-3 sentences of prose follow the blank line"""
        content = Path("test-9ehmdc.md").read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = lines[2]

        # Count sentences (roughly by periods)
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"
        assert len(prose) > 0, "Prose content should not be empty"

    def test_file_is_utf8_encoded(self):
        """Test that file is UTF-8 encoded without BOM"""
        file_path = Path("test-9ehmdc.md")
        raw_bytes = file_path.read_bytes()
        # UTF-8 BOM is bytes EF BB BF
        assert not raw_bytes.startswith(b'\xef\xbb\xbf'), "File should not have UTF-8 BOM"
        # Should be decodable as UTF-8
        try:
            raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File should be valid UTF-8")


class TestFileValidation:
    """Task 2: Validate file meets all technical requirements"""

    def test_file_size_in_range(self):
        """Test that file size is between 300-600 bytes"""
        file_path = Path("test-9ehmdc.md")
        size = len(file_path.read_bytes())
        assert 300 <= size <= 600, f"File size {size} should be between 300-600 bytes"

    def test_line_endings_are_lf(self):
        """Test that file uses LF (\\n) line endings, not CRLF"""
        file_path = Path("test-9ehmdc.md")
        raw_bytes = file_path.read_bytes()
        # Check for CRLF (\\r\\n = bytes 0x0D 0x0A)
        assert b"\r\n" not in raw_bytes, "File should use LF (\\n), not CRLF (\\r\\n)"
        # Verify it contains LF
        assert b"\n" in raw_bytes, "File should contain LF line endings"

    def test_no_bom_bytes(self):
        """Test that file does not have UTF-8 BOM (EF BB BF)"""
        file_path = Path("test-9ehmdc.md")
        raw_bytes = file_path.read_bytes()
        assert not raw_bytes.startswith(b'\xef\xbb\xbf'), "File should not start with UTF-8 BOM"

    def test_markdown_format_compliance(self):
        """Test that file structure matches spec (H1 + blank + prose)"""
        content = Path("test-9ehmdc.md").read_text(encoding="utf-8")
        lines = content.split("\n")

        # Line 1: H1 heading
        assert lines[0].startswith("# "), "Line 1 should be H1 heading"
        # Line 2: blank
        assert lines[1] == "", "Line 2 should be blank"
        # Line 3: prose
        assert len(lines[2]) > 0, "Line 3 should contain prose"
        # Prose should be coherent (have at least 2 sentences)
        assert lines[2].count(".") >= 2, "Prose should contain at least 2 sentences"

    def test_prose_is_coherent(self):
        """Test that prose is grammatically correct and coherent (NFR-2)"""
        content = Path("test-9ehmdc.md").read_text(encoding="utf-8")
        lines = content.split("\n")
        prose = lines[2]

        # Basic checks for coherence:
        # - Should have capital letter at start
        # - Should not be gibberish
        # - Should have proper spacing
        assert prose[0].isupper(), "Prose should start with capital letter"
        assert "  " not in prose, "Prose should not have multiple consecutive spaces"
        # Check that it ends with a period
        assert prose.rstrip().endswith("."), "Prose should end with a period"
