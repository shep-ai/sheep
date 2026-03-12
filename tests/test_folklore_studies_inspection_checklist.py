from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
FOLKLORE_FILE = REPO_ROOT / "folklore-studies-nxipmi.md"


def test_file_exists():
    assert FOLKLORE_FILE.exists(), f"{FOLKLORE_FILE} does not exist"


def test_file_has_h1_heading():
    content = FOLKLORE_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_folklore():
    content = FOLKLORE_FILE.read_text(encoding="utf-8")
    assert "folklore" in content.lower(), "File does not mention folklore"


def test_file_has_checklist():
    content = FOLKLORE_FILE.read_text(encoding="utf-8")
    assert "[ ]" in content, "File does not contain a checklist"


def test_file_ends_with_newline():
    raw = FOLKLORE_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
