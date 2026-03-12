from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
KNOTS_FILE = REPO_ROOT / "nautical-knots-wqwlea.md"


def test_file_exists():
    assert KNOTS_FILE.exists(), f"{KNOTS_FILE} does not exist"


def test_file_has_h1_heading():
    content = KNOTS_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_knot():
    content = KNOTS_FILE.read_text(encoding="utf-8")
    assert "knot" in content.lower(), "File does not mention knot"


def test_file_under_80_lines():
    content = KNOTS_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = KNOTS_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
