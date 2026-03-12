from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
EMBOSSING_FILE = REPO_ROOT / "embossing-j1qx9z.md"


def test_file_exists():
    assert EMBOSSING_FILE.exists(), f"{EMBOSSING_FILE} does not exist"


def test_file_has_h1_heading():
    content = EMBOSSING_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_embossing():
    content = EMBOSSING_FILE.read_text(encoding="utf-8")
    assert "embossing" in content.lower(), "File does not mention embossing"


def test_file_has_comparison_table():
    content = EMBOSSING_FILE.read_text(encoding="utf-8")
    assert "|" in content and "---" in content, "File does not contain a comparison table"


def test_file_ends_with_newline():
    raw = EMBOSSING_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
