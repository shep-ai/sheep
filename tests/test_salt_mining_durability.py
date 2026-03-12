from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SALT_FILE = REPO_ROOT / "salt-mining.md"


def test_file_exists():
    assert SALT_FILE.exists(), f"{SALT_FILE} does not exist"


def test_file_has_h1_heading():
    content = SALT_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_salt_mining():
    content = SALT_FILE.read_text(encoding="utf-8")
    assert "salt" in content.lower(), "File does not mention salt"


def test_file_has_durability_ranking():
    content = SALT_FILE.read_text(encoding="utf-8")
    assert "durability" in content.lower(), "File does not contain durability ranking"


def test_file_under_80_lines():
    content = SALT_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = SALT_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
