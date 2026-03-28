"""Validate that test-7fyam7.md meets repository markdown conventions."""

from pathlib import Path

import pytest

from sheep.content_generators import validate_markdown_file


class Test7fyam7MarkdownFile:
    """Ensure sample markdown file exists and passes structural checks."""

    def test_file_exists_in_repository_root(self) -> None:
        filepath = Path("test-7fyam7.md")
        assert filepath.exists(), "File test-7fyam7.md does not exist in repository root"
        assert filepath.is_file(), "test-7fyam7.md is not a file"

    def test_file_has_utf8_encoding_no_bom(self) -> None:
        filepath = Path("test-7fyam7.md")
        binary_content = filepath.read_bytes()
        assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")

    def test_file_uses_lf_line_endings(self) -> None:
        filepath = Path("test-7fyam7.md")
        binary_content = filepath.read_bytes()
        assert b"\r\n" not in binary_content, "File should use LF, not CRLF"
        assert b"\n" in binary_content, "File should have LF line endings"

    def test_file_contains_h1_heading(self) -> None:
        filepath = Path("test-7fyam7.md")
        text_content = filepath.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert lines[0].startswith("# "), "First line must be H1 heading (# )"
        h1_count = text_content.count("# ")
        assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"

    def test_file_has_blank_line_after_heading(self) -> None:
        filepath = Path("test-7fyam7.md")
        text_content = filepath.read_text(encoding="utf-8")
        lines = text_content.split("\n")
        assert len(lines) >= 2, "File should have at least 2 lines"
        assert lines[1] == "", "Second line should be blank separator"

    def test_file_contains_2_3_sentences(self) -> None:
        filepath = Path("test-7fyam7.md")
        text_content = filepath.read_text(encoding="utf-8")
        sentence_count = text_content.count(".")
        assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count}"

    def test_file_has_trailing_newline(self) -> None:
        filepath = Path("test-7fyam7.md")
        text_content = filepath.read_text(encoding="utf-8")
        assert text_content.endswith("\n"), "File should end with trailing newline"

    def test_file_passes_comprehensive_validation(self) -> None:
        result = validate_markdown_file("test-7fyam7.md")
        assert result is True, "File should pass comprehensive validation"
