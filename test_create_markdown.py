"""Tests for markdown file creation (feature 123)."""
import re
from pathlib import Path
import tempfile
import os


def test_content_has_h1_heading():
    """Content should have exactly one H1 heading."""
    from create_markdown import CONTENT
    assert CONTENT.startswith("# "), "Content must start with H1 heading (# )"
    lines = CONTENT.split("\n")
    assert lines[0].startswith("# "), "First line must be H1 heading"
    h1_count = sum(1 for line in lines if line.startswith("# "))
    assert h1_count == 1, f"Expected exactly 1 H1 heading, found {h1_count}"


def test_content_has_blank_line_after_heading():
    """Content should have a blank line after the H1 heading."""
    from create_markdown import CONTENT
    lines = CONTENT.split("\n")
    assert len(lines) > 1, "Content must have multiple lines"
    assert lines[1] == "", "Second line must be blank"


def test_content_has_prose():
    """Content should have 2-3 sentences of prose after the blank line."""
    from create_markdown import CONTENT
    lines = CONTENT.split("\n")
    prose_text = "\n".join(lines[2:]).strip()
    assert prose_text, "Content must have prose after blank line"

    # Count sentences (roughly: split by periods)
    sentences = [s.strip() for s in prose_text.split(".") if s.strip()]
    assert 2 <= len(sentences) <= 3, f"Expected 2-3 sentences, found {len(sentences)}: {sentences}"


def test_file_write_creates_file():
    """Writing file should create test-aibs55.md."""
    # Use temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            from create_markdown import write_markdown_file

            write_markdown_file()

            file_path = Path("test-aibs55.md")
            assert file_path.exists(), "test-aibs55.md should exist after write_markdown_file()"
        finally:
            os.chdir(original_cwd)


def test_file_size_in_range():
    """File size should be between 300-500 bytes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            from create_markdown import write_markdown_file

            write_markdown_file()

            file_path = Path("test-aibs55.md")
            file_size = file_path.stat().st_size
            assert 300 <= file_size <= 500, f"File size {file_size} not in range 300-500"
        finally:
            os.chdir(original_cwd)


def test_file_encoding_utf8():
    """File should be UTF-8 encoded."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            from create_markdown import write_markdown_file

            write_markdown_file()

            file_path = Path("test-aibs55.md")
            # Read with UTF-8 should succeed
            content = file_path.read_text(encoding="utf-8")
            assert content, "File should have readable UTF-8 content"
        finally:
            os.chdir(original_cwd)


def test_file_line_endings_lf():
    """File should use Unix LF line endings, not CRLF."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            from create_markdown import write_markdown_file

            write_markdown_file()

            file_path = Path("test-aibs55.md")
            # Read as binary to check line endings
            content_binary = file_path.read_bytes()
            assert b"\r\n" not in content_binary, "File should not contain CRLF (Windows line endings)"
            assert b"\n" in content_binary, "File should contain LF (Unix line endings)"
        finally:
            os.chdir(original_cwd)


def test_file_content_matches_constant():
    """File content should match CONTENT constant."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmpdir)
            from create_markdown import CONTENT, write_markdown_file

            write_markdown_file()

            file_path = Path("test-aibs55.md")
            file_content = file_path.read_text(encoding="utf-8")
            assert file_content == CONTENT, "File content should match CONTENT constant"
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    # Run with: python -m pytest test_create_markdown.py -v
    print("Run tests with: python -m pytest test_create_markdown.py -v")
