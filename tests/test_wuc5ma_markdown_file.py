import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEST_FILE = REPO_ROOT / "test-wuc5ma.md"


def test_file_exists():
    assert TEST_FILE.exists(), f"{TEST_FILE} does not exist"


def test_file_uses_utf8_encoding():
    # If this raises UnicodeDecodeError, it's not valid UTF-8.
    content = TEST_FILE.read_text(encoding="utf-8")
    assert content


def test_starts_with_h1_heading_and_blank_line():
    content = TEST_FILE.read_text(encoding="utf-8")
    assert re.match(r"^# .+\n\n", content), "Expected H1 heading followed by a blank line"


def test_contains_two_or_three_sentences():
    content = TEST_FILE.read_text(encoding="utf-8")
    lines = content.split("\n")
    prose = "\n".join(lines[2:]).strip()  # Skip heading and blank line

    sentences = re.findall(r"[^.!?]*[.!?]", prose)
    assert 2 <= len(sentences) <= 3, f"Expected 2-3 sentences, found {len(sentences)}"

