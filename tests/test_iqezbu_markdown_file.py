"""Tests for test-iqezbu.md: title (H1) and short prose."""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
MARKDOWN_FILE = REPO_ROOT / "test-iqezbu.md"


def test_file_exists():
    assert MARKDOWN_FILE.exists(), f"{MARKDOWN_FILE} does not exist"


def test_file_has_h1_heading():
    content = MARKDOWN_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert lines and lines[0].startswith("# "), "First line should be an H1 heading"


def test_file_has_two_or_three_sentences():
    content = MARKDOWN_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    # Prose after blank line following H1
    prose_start = 1
    while prose_start < len(lines) and lines[prose_start].strip() == "":
        prose_start += 1
    prose = " ".join(lines[prose_start:]).strip()
    sentence_count = prose.count(".")
    assert 2 <= sentence_count <= 3, f"Expected 2-3 sentences, found {sentence_count} (by period count)"


def test_file_ends_with_newline():
    raw = MARKDOWN_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File should end with a newline"
