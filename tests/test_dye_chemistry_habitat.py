from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TOPIC_FILE = REPO_ROOT / "TOPIC.md"


def test_file_exists():
    assert TOPIC_FILE.exists(), f"{TOPIC_FILE} does not exist"


def test_file_has_h1_heading():
    content = TOPIC_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_dye_chemistry():
    content = TOPIC_FILE.read_text(encoding="utf-8")
    assert "dye" in content.lower(), "File does not mention dye chemistry"


def test_file_has_10_habitat_entries():
    content = TOPIC_FILE.read_text(encoding="utf-8")
    numbered = [
        line for line in content.splitlines()
        if line.strip() and line.strip()[0].isdigit() and ". " in line
    ]
    assert len(numbered) == 10, f"Expected 10 habitat entries, got {len(numbered)}"


def test_file_under_80_lines():
    content = TOPIC_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = TOPIC_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
