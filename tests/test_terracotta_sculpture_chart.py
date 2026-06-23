from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TERRACOTTA_FILE = REPO_ROOT / "terracotta-sculpture-tkhwhz.md"


def test_file_exists():
    assert TERRACOTTA_FILE.exists(), f"{TERRACOTTA_FILE} does not exist"


def test_file_has_h1_heading():
    content = TERRACOTTA_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_terracotta():
    content = TERRACOTTA_FILE.read_text(encoding="utf-8")
    assert "terracotta" in content.lower(), "File does not mention terracotta"


def test_file_under_80_lines():
    content = TERRACOTTA_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = TERRACOTTA_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
