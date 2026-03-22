import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEST_FILE = REPO_ROOT / "test-walkad.md"


def test_file_exists():
    """Assert that test-walkad.md exists at repository root."""
    assert TEST_FILE.exists(), f"{TEST_FILE} does not exist"


def test_file_uses_utf8_encoding():
    """Verify file can be read with UTF-8 encoding."""
    try:
        content = TEST_FILE.read_text(encoding="utf-8")
        assert content is not None
    except UnicodeDecodeError as err:
        raise AssertionError(f"{TEST_FILE} is not valid UTF-8") from err


def test_starts_with_h1_heading():
    """Verify file contains valid CommonMark h1 heading."""
    content = TEST_FILE.read_text(encoding="utf-8")
    assert content.startswith("#"), "File must start with h1 heading (# Title)"
    assert re.match(r"^# .+\n", content), "File must start with proper h1 format: '# Title'"


def test_h1_title_format():
    """Verify h1 title has proper formatting (2-5 words, leading space)."""
    content = TEST_FILE.read_text(encoding="utf-8")
    match = re.match(r"^# (.+?)\n", content)
    assert match, "Could not extract h1 title"
    title = match.group(1)
    words = title.split()
    assert 2 <= len(words) <= 5, f"h1 title should be 2-5 words, got {len(words)}"
    assert len(title) > 0, "h1 title cannot be empty"


def test_contains_prose_sentences():
    """Verify file contains 2-3 sentences of prose after h1 heading."""
    content = TEST_FILE.read_text(encoding="utf-8")
    lines = content.split("\n")
    prose = "\n".join(lines[2:]).strip()
    sentences = re.findall(r"[^.!?]*[.!?]", prose)
    assert 2 <= len(sentences) <= 3, f"File should contain 2-3 sentences, found {len(sentences)}"


def test_content_coherence():
    """Verify prose substantiates the h1 title."""
    content = TEST_FILE.read_text(encoding="utf-8")
    title_match = re.match(r"^# (.+?)\n", content)
    assert title_match, "Could not extract h1 title"
    title = title_match.group(1).lower()
    lines = content.split("\n")
    prose = "\n".join(lines[2:]).lower()
    title_words = title.split()
    found_match = any(word in prose for word in title_words if len(word) > 3)
    assert found_match or len(title_words) <= 2, "Prose should contain key terms from h1 title"


def test_no_trailing_whitespace():
    """Verify no unwanted trailing whitespace in file."""
    with open(TEST_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines[:-1]):
        assert line.rstrip() == line.rstrip("\n"), f"Line {i + 1} has trailing whitespace"


def test_valid_markdown_syntax():
    """Verify file would render correctly as markdown."""
    content = TEST_FILE.read_text(encoding="utf-8")
    assert not content.strip().endswith("\n\n\n"), "File should not have excessive blank lines"
    assert "#" in content, "File must contain h1 heading"
    lines = [line for line in content.split("\n") if line.strip()]
    assert len(lines) >= 2, "File must contain h1 heading and at least one sentence"
