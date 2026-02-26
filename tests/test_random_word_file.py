from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
RANDOM_WORD_FILE = REPO_ROOT / "RANDOM_WORD.txt"


def test_file_exists():
    assert RANDOM_WORD_FILE.exists(), f"{RANDOM_WORD_FILE} does not exist"


def test_file_contains_exactly_one_word():
    content = RANDOM_WORD_FILE.read_text(encoding="utf-8")
    tokens = content.split()
    assert len(tokens) == 1, f"Expected 1 token, got {len(tokens)}: {tokens!r}"


def test_file_ends_with_single_lf():
    raw = RANDOM_WORD_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
    assert not raw.endswith(b"\r\n"), "File has Windows-style CRLF line ending"
    assert raw.count(b"\n") == 1, f"Expected exactly 1 newline, got {raw.count(b'\\n')}"
