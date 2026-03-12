from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BLACK_HOLES_FILE = REPO_ROOT / "black-holes-lpgi51.md"


def test_file_exists():
    assert BLACK_HOLES_FILE.exists(), f"{BLACK_HOLES_FILE} does not exist"


def test_file_has_h1_heading():
    content = BLACK_HOLES_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_black_holes():
    content = BLACK_HOLES_FILE.read_text(encoding="utf-8")
    assert "black hole" in content.lower(), "File does not mention black holes"


def test_file_under_80_lines():
    content = BLACK_HOLES_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = BLACK_HOLES_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
