from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RANDOM_JOKE_FILE = REPO_ROOT / "RANDOM_JOKE.md"


def test_file_exists():
    assert RANDOM_JOKE_FILE.exists(), f"{RANDOM_JOKE_FILE} does not exist"


def test_file_has_h1_heading():
    content = RANDOM_JOKE_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_contains_single_joke():
    content = RANDOM_JOKE_FILE.read_text(encoding="utf-8")
    separators = [line.strip() for line in content.splitlines() if line.strip() == "---"]
    assert len(separators) == 1, f"Expected exactly 1 separator (---), got {len(separators)}"


def test_file_ends_with_newline():
    raw = RANDOM_JOKE_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
