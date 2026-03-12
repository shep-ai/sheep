from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
URBAN_BEEKEEPING_FILE = REPO_ROOT / "urban-beekeeping.md"


def test_file_exists():
    assert URBAN_BEEKEEPING_FILE.exists(), f"{URBAN_BEEKEEPING_FILE} does not exist"


def test_file_has_h1_heading():
    content = URBAN_BEEKEEPING_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_beekeeping():
    content = URBAN_BEEKEEPING_FILE.read_text(encoding="utf-8")
    assert "beekeeping" in content.lower(), "File does not mention beekeeping"


def test_file_under_80_lines():
    content = URBAN_BEEKEEPING_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = URBAN_BEEKEEPING_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
