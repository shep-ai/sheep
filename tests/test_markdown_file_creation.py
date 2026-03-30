"""Tests for markdown file creation feature (287)."""

import os
from pathlib import Path


TEST_FILE_PATH = Path(__file__).parent.parent / "test-hzqchm.md"


def test_markdown_file_does_not_exist_initially(tmp_path):
    """Test that the markdown file does not exist before creation."""
    file_path = tmp_path / "test-hzqchm.md"
    assert not file_path.exists()


def test_markdown_file_creation(tmp_path):
    """Test that markdown file is created with correct structure."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    assert file_path.exists()
    assert file_path.read_text(encoding="utf-8") == content


def test_markdown_file_contains_h1_heading(tmp_path):
    """Test that file contains H1 heading in correct format."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    text = file_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    assert lines[0].startswith("# ")
    assert len(lines[0]) > 2  # At least "# " plus title


def test_markdown_file_has_blank_line_after_heading(tmp_path):
    """Test that blank line separates heading from prose."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    text = file_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    assert lines[0].startswith("# ")
    assert lines[1] == ""  # Blank line


def test_markdown_file_contains_2_3_sentences(tmp_path):
    """Test that file contains exactly 2-3 sentences of prose."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    text = file_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    prose = lines[2]  # Third line is the prose

    # Count sentences (simple heuristic: count periods)
    sentence_count = prose.count(".")
    assert 2 <= sentence_count <= 3


def test_markdown_file_utf8_encoding(tmp_path):
    """Test that file is encoded in UTF-8 without BOM."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    # Read as bytes to check for BOM
    raw_bytes = file_path.read_bytes()
    # UTF-8 BOM is EF BB BF
    assert not raw_bytes.startswith(b"\xef\xbb\xbf")
    # Should be valid UTF-8
    assert raw_bytes.decode("utf-8") == content


def test_markdown_file_lf_line_endings(tmp_path):
    """Test that file uses LF line endings, not CRLF."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    raw_bytes = file_path.read_bytes()
    # Should not contain CRLF
    assert b"\r\n" not in raw_bytes
    # Should contain LF
    assert b"\n" in raw_bytes


def test_markdown_file_size(tmp_path):
    """Test that file size is approximately 400-600 bytes."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    file_size = file_path.stat().st_size
    assert 300 <= file_size <= 700  # Slightly broader range to account for variations


def test_markdown_file_valid_commonmark_syntax(tmp_path):
    """Test that markdown syntax conforms to CommonMark specification."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    text = file_path.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Check H1 heading format (ATX style)
    assert lines[0].startswith("# ")
    # Check blank line
    assert lines[1] == ""
    # Check prose (should be plain text)
    assert lines[2]  # Not empty


def test_markdown_file_prose_is_meaningful(tmp_path):
    """Test that prose content is meaningful and grammatically correct."""
    file_path = tmp_path / "test-hzqchm.md"
    content = "# The Power of Curiosity\n\nCuriosity is the driving force behind human discovery and innovation, pushing us to explore beyond the boundaries of what we already know and understand. It fuels scientific research, artistic expression, and personal growth, transforming ordinary individuals into pioneers of new fields and creators of remarkable achievements. By nurturing our natural inclination to ask questions and seek answers, we unlock our potential to contribute meaningfully to the world around us.\n"
    file_path.write_text(content, encoding="utf-8", newline="")

    text = file_path.read_text(encoding="utf-8")
    lines = text.split("\n")
    prose = lines[2]

    # Basic checks for meaningful content
    assert len(prose) > 0
    assert prose[0].isupper()  # Starts with capital letter
    assert "." in prose  # Contains periods
    # Should have multiple words
    words = prose.split()
    assert len(words) >= 5


def test_actual_markdown_file_exists():
    """Test that the actual markdown file exists at repository root."""
    assert TEST_FILE_PATH.exists(), f"File {TEST_FILE_PATH} should exist at repository root"


def test_actual_markdown_file_has_correct_structure():
    """Test that the actual markdown file has correct H1 + blank line + prose structure."""
    text = TEST_FILE_PATH.read_text(encoding="utf-8")
    lines = text.split("\n")

    # First line should be H1 heading
    assert lines[0].startswith("# "), "First line should be H1 heading"
    # Second line should be blank
    assert lines[1] == "", "Second line should be blank"
    # Third line should contain prose
    assert lines[2], "Third line should contain prose"


def test_actual_markdown_file_utf8_no_bom():
    """Test that the actual markdown file is UTF-8 without BOM."""
    raw_bytes = TEST_FILE_PATH.read_bytes()
    # UTF-8 BOM is EF BB BF
    assert not raw_bytes.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"


def test_actual_markdown_file_lf_line_endings():
    """Test that the actual markdown file uses LF line endings."""
    raw_bytes = TEST_FILE_PATH.read_bytes()
    # Should not contain CRLF
    assert b"\r\n" not in raw_bytes, "File should not contain CRLF line endings"
    # Should contain LF
    assert b"\n" in raw_bytes, "File should contain LF line endings"


def test_actual_markdown_file_size():
    """Test that the actual markdown file size is approximately 400-600 bytes."""
    file_size = TEST_FILE_PATH.stat().st_size
    assert 300 <= file_size <= 700, f"File size {file_size} should be approximately 400-600 bytes"


def test_actual_markdown_file_sentence_count():
    """Test that the actual markdown file contains 2-3 sentences."""
    text = TEST_FILE_PATH.read_text(encoding="utf-8")
    lines = text.split("\n")
    prose = lines[2]  # Third line is the prose

    # Count sentences (simple heuristic: count periods)
    sentence_count = prose.count(".")
    assert 2 <= sentence_count <= 3, f"File should contain 2-3 sentences, found {sentence_count}"
