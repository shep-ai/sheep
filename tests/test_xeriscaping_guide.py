from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
XERISCAPING_FILE = REPO_ROOT / "xeriscaping-j7okgb.md"


def test_file_exists():
    assert XERISCAPING_FILE.exists(), f"{XERISCAPING_FILE} does not exist"


def test_file_has_h1_heading():
    content = XERISCAPING_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_xeriscaping():
    content = XERISCAPING_FILE.read_text(encoding="utf-8")
    assert "xeriscap" in content.lower(), "File does not mention xeriscaping"


def test_file_ends_with_newline():
    raw = XERISCAPING_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
