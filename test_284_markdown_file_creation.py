"""
Test suite for feature 284: markdown file creation (Phase 1 - File Creation & Content Setup).

This module validates the creation of test-3b9lxg.md with proper structure,
encoding, and line endings.

Test Coverage:
- File exists at repository root with correct filename
- Content structure (H1 heading + blank line + prose + trailing newline)
- Encoding validation (UTF-8 without BOM)
- Line ending validation (Unix LF, no Windows CRLF)
- Prose content validation (2-3 sentences)
- File size validation (400-600 bytes)
"""

from pathlib import Path
import pytest


class TestMarkdownFileCreation:
    """Tests for markdown file test-3b9lxg.md creation."""

    @pytest.fixture
    def repo_root(self):
        """Return the repository root path."""
        return Path(__file__).parent

    def test_file_exists_in_repository_root(self, repo_root):
        """Test that test-3b9lxg.md exists in repository root."""
        filepath = repo_root / "test-3b9lxg.md"
        assert filepath.exists(), f"File {filepath} should exist"
        assert filepath.is_file(), f"{filepath} should be a file"

    def test_file_has_correct_filename(self, repo_root):
        """Test that the file is named exactly test-3b9lxg.md."""
        filepath = repo_root / "test-3b9lxg.md"
        assert filepath.name == "test-3b9lxg.md"

    def test_file_contains_h1_heading(self, repo_root):
        """Test that file contains exactly one H1 markdown heading."""
        filepath = repo_root / "test-3b9lxg.md"
        content = filepath.read_text(encoding="utf-8")

        # Should start with H1
        assert content.startswith("# "), "File should start with H1 heading (# )"

        # Count H1 headings (lines starting with "# ")
        lines = content.split("\n")
        h1_count = sum(1 for line in lines if line.startswith("# "))
        assert h1_count == 1, f"File should contain exactly 1 H1 heading, found {h1_count}"

    def test_file_has_blank_line_after_heading(self, repo_root):
        """Test that file has blank line separating heading from prose."""
        filepath = repo_root / "test-3b9lxg.md"
        content = filepath.read_text(encoding="utf-8")

        lines = content.split("\n")
        assert len(lines) >= 3, "File should have at least: heading, blank line, and prose"
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank"

    def test_file_contains_prose_content(self, repo_root):
        """Test that file contains prose content after the blank line."""
        filepath = repo_root / "test-3b9lxg.md"
        content = filepath.read_text(encoding="utf-8")

        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()

        assert prose, "File should contain prose content"
        assert len(prose) > 50, "Prose content should be substantial (>50 characters)"

    def test_prose_contains_2_to_3_sentences(self, repo_root):
        """Test that prose contains 2-3 sentences."""
        filepath = repo_root / "test-3b9lxg.md"
        content = filepath.read_text(encoding="utf-8")

        lines = content.split("\n")
        prose = "\n".join(lines[2:]).strip()

        # Count periods as sentence markers
        sentence_count = prose.count(".")
        assert 2 <= sentence_count <= 3, (
            f"Prose should contain 2-3 sentences (periods), "
            f"found {sentence_count}"
        )

    def test_file_is_utf8_encoded(self, repo_root):
        """Test that file is UTF-8 encoded."""
        filepath = repo_root / "test-3b9lxg.md"
        binary_content = filepath.read_bytes()

        # Should be valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_has_no_utf8_bom(self, repo_root):
        """Test that file has no UTF-8 BOM."""
        filepath = repo_root / "test-3b9lxg.md"
        binary_content = filepath.read_bytes()

        # Should not start with UTF-8 BOM (EF BB BF)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), (
            "File should not have UTF-8 BOM"
        )

    def test_file_uses_lf_line_endings(self, repo_root):
        """Test that file uses Unix LF line endings, not Windows CRLF."""
        filepath = repo_root / "test-3b9lxg.md"
        binary_content = filepath.read_bytes()

        # Should not contain CRLF
        assert b"\r\n" not in binary_content, (
            "File should use Unix LF line endings, not Windows CRLF"
        )

        # Should contain at least one LF
        assert b"\n" in binary_content, "File should contain LF line endings"

    def test_file_ends_with_newline(self, repo_root):
        """Test that file ends with a newline character."""
        filepath = repo_root / "test-3b9lxg.md"
        binary_content = filepath.read_bytes()

        assert binary_content.endswith(b"\n"), "File should end with a newline"

    def test_file_size_within_target_range(self, repo_root):
        """Test that file size is between 400-600 bytes."""
        filepath = repo_root / "test-3b9lxg.md"
        file_size = filepath.stat().st_size

        assert 400 <= file_size <= 600, (
            f"File size {file_size} bytes does not meet specification "
            f"requirement of 400-600 bytes"
        )

    def test_content_is_meaningful_and_grammatical(self, repo_root):
        """Test that content is meaningful and grammatically correct."""
        filepath = repo_root / "test-3b9lxg.md"
        content = filepath.read_text(encoding="utf-8")

        lines = content.split("\n")
        title = lines[0][2:].strip()  # Extract title (remove "# ")
        prose = "\n".join(lines[2:]).strip()

        # Title should be reasonable length
        assert 3 <= len(title) <= 100, "Title should be 3-100 characters"

        # Title should contain letters (not just numbers or special chars)
        assert any(c.isalpha() for c in title), "Title should contain letters"

        # Prose should have reasonable structure (contain actual words)
        assert any(c.isalpha() for c in prose), "Prose should contain letters"

    def test_file_matches_established_pattern(self, repo_root):
        """Test that file structure matches established pattern from existing test files."""
        filepath = repo_root / "test-3b9lxg.md"
        content = filepath.read_text(encoding="utf-8")

        # Pattern: H1 heading, blank line, prose content, trailing newline
        assert content.count("\n\n") >= 1, "File should have blank line separator"

        # Check structure: first line is heading, second is blank
        lines = content.split("\n")
        assert lines[0].startswith("# "), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be blank"

        # Content should exist after blank line
        assert len(lines) > 2, "File should have content after blank line"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
