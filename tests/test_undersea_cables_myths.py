from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
UNDERSEA_CABLES_FILE = REPO_ROOT / "undersea-cables-5xdewv.md"


def test_file_exists():
    assert UNDERSEA_CABLES_FILE.exists(), f"{UNDERSEA_CABLES_FILE} does not exist"


def test_file_has_h1_heading():
    content = UNDERSEA_CABLES_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_undersea_cables():
    content = UNDERSEA_CABLES_FILE.read_text(encoding="utf-8")
    assert "undersea cables" in content.lower(), "File does not mention undersea cables"


def test_file_under_80_lines():
    content = UNDERSEA_CABLES_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = UNDERSEA_CABLES_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
