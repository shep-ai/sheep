from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
FILE = REPO_ROOT / "folklore-studies-hiof3w.md"


def test_file_exists():
    assert FILE.exists(), f"{FILE} does not exist"


def test_file_has_h1_heading():
    content = FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_has_10_items():
    content = FILE.read_text(encoding="utf-8")
    numbered = [
        line
        for line in content.splitlines()
        if line.strip() and line.strip()[0].isdigit() and ". " in line
    ]
    assert len(numbered) == 10, f"Expected 10 list items, got {len(numbered)}"


def test_file_mentions_folklore():
    content = FILE.read_text(encoding="utf-8")
    assert "folklore" in content.lower(), "File does not mention folklore"


def test_file_ends_with_newline():
    raw = FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
