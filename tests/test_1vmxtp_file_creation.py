"""Tests for test-1vmxtp.md file creation and validation."""

from pathlib import Path
import pytest


class TestMarkdownFileCreation:
    """Tests for test-1vmxtp.md file creation."""

    # No setup fixture needed - file should already exist from Phase 1

    def test_file_exists_at_repository_root(self):
        """Test that test-1vmxtp.md exists at repository root."""
        file_path = Path("test-1vmxtp.md")
        assert file_path.exists(), "File test-1vmxtp.md should exist at repository root"
        assert file_path.is_file(), "test-1vmxtp.md should be a file, not a directory"

    def test_file_contains_h1_heading(self):
        """Test that file contains a markdown H1 heading on first line."""
        file_path = Path("test-1vmxtp.md")
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) > 0, "File should not be empty"
        assert lines[0].startswith("# "), "First line must be H1 heading (starts with # )"

    def test_file_has_blank_line_after_heading(self):
        """Test that file has blank line after H1 heading."""
        file_path = Path("test-1vmxtp.md")
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        assert len(lines) >= 2, "File must have at least heading and blank line"
        assert lines[1] == "", "Second line must be blank (separator after heading)"

    def test_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose after blank line."""
        file_path = Path("test-1vmxtp.md")
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        # Get prose lines (skip heading and blank line)
        prose_lines = lines[2:]

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        assert len(prose_lines) > 0, "File must have prose content after heading"

        # Combine prose lines and check for sentences
        prose_content = "\n".join(prose_lines).strip()
        sentence_count = prose_content.count(".")

        assert sentence_count >= 2 and sentence_count <= 3, \
            f"Prose must contain 2-3 sentences, found {sentence_count}"

    def test_file_is_utf8_encoded_without_bom(self):
        """Test that file is UTF-8 encoded without BOM."""
        file_path = Path("test-1vmxtp.md")
        binary_content = file_path.read_bytes()

        # Check for UTF-8 BOM (should NOT be present)
        assert not binary_content.startswith(b"\xef\xbb\xbf"), \
            "File should not have UTF-8 BOM"

        # Verify it can be decoded as UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File is not valid UTF-8")

    def test_file_has_unix_lf_line_endings(self):
        """Test that file uses Unix LF line endings, not CRLF."""
        file_path = Path("test-1vmxtp.md")
        binary_content = file_path.read_bytes()

        assert b"\r\n" not in binary_content, \
            "File should not have CRLF line endings"
        assert b"\n" in binary_content, \
            "File should have LF line endings"

    def test_file_size_within_range(self):
        """Test that file size is between 320-600 bytes."""
        file_path = Path("test-1vmxtp.md")
        file_size = file_path.stat().st_size

        assert 320 <= file_size <= 600, \
            f"File size should be 320-600 bytes, got {file_size}"

    def test_file_ends_with_trailing_newline(self):
        """Test that file ends with trailing newline."""
        file_path = Path("test-1vmxtp.md")
        content = file_path.read_text(encoding="utf-8")

        assert content.endswith("\n"), "File must end with trailing newline"

    def test_prose_is_grammatically_correct(self):
        """Test that prose content is grammatically correct and coherent."""
        file_path = Path("test-1vmxtp.md")
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")

        prose_lines = lines[2:]
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        prose_content = "\n".join(prose_lines).strip()

        # Check that prose is not empty
        assert len(prose_content) > 0, "Prose content should not be empty"

        # Check that prose has reasonable length
        assert len(prose_content) > 50, "Prose content should be substantial (>50 chars)"

        # Check that sentences don't have obvious issues
        # (e.g., starting with lowercase or missing spaces after periods)
        sentences = prose_content.split(".")
        for i, sentence in enumerate(sentences[:-1]):  # Skip last empty element
            sentence = sentence.strip()
            assert sentence, f"Sentence {i+1} is empty"
            # First character of sentence should be uppercase
            assert sentence[0].isupper(), \
                f"Sentence {i+1} should start with uppercase: '{sentence}'"
