from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
JOKE4_FILE = REPO_ROOT / "JOKE4.md"


def test_file_exists():
    assert JOKE4_FILE.exists(), f"{JOKE4_FILE} does not exist"


def test_file_has_h1_heading():
    content = JOKE4_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_contains_joke_format():
    content = JOKE4_FILE.read_text(encoding="utf-8")
    assert "**Q:**" in content, "File does not contain Q&A joke format"
    assert "**A:**" in content, "File does not contain Q&A joke format"


def test_file_is_valid_markdown():
    content = JOKE4_FILE.read_text(encoding="utf-8")
    assert len(content.strip()) > 0, "File is empty"
    assert content.count("**Q:**") >= 1, "File should have at least one joke"
