from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RANDOM_BELIEF_FILE = REPO_ROOT / "RANDOM_BELIEF.md"


def test_file_exists():
    assert RANDOM_BELIEF_FILE.exists(), f"{RANDOM_BELIEF_FILE} does not exist"


def test_file_has_h1_heading():
    content = RANDOM_BELIEF_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_is_not_empty():
    content = RANDOM_BELIEF_FILE.read_text(encoding="utf-8").strip()
    assert len(content) > 0, "File is empty"


def test_file_ends_with_newline():
    raw = RANDOM_BELIEF_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
