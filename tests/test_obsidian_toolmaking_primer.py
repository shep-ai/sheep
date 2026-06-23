from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PRIMER_FILE = REPO_ROOT / "obsidian-toolmaking-7o5t7j.md"


def test_primer_file_exists():
    assert PRIMER_FILE.exists(), f"{PRIMER_FILE} does not exist"


def test_primer_has_title():
    content = PRIMER_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 title"


def test_primer_mentions_obsidian():
    content = PRIMER_FILE.read_text(encoding="utf-8")
    assert "obsidian" in content.lower(), "File does not mention obsidian"


def test_primer_is_short():
    content = PRIMER_FILE.read_text(encoding="utf-8")
    sentences = [s.strip() for s in content.replace("\n", " ").split(".") if s.strip()]
    assert 2 <= len(sentences) <= 5, f"Expected 2-5 sentences, got {len(sentences)}"


def test_primer_ends_with_newline():
    raw = PRIMER_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
