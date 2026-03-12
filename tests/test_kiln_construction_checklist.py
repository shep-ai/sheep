from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CHECKLIST_FILE = REPO_ROOT / "kiln-construction-u2p0ty.md"


def test_checklist_file_exists():
    assert CHECKLIST_FILE.exists(), f"{CHECKLIST_FILE} does not exist"


def test_checklist_has_title():
    content = CHECKLIST_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 title"


def test_checklist_mentions_kiln():
    content = CHECKLIST_FILE.read_text(encoding="utf-8")
    assert "kiln" in content.lower(), "File does not mention kiln"


def test_checklist_is_short():
    content = CHECKLIST_FILE.read_text(encoding="utf-8")
    sentences = [s.strip() for s in content.replace("\n", " ").split(".") if s.strip()]
    assert 2 <= len(sentences) <= 5, f"Expected 2-5 sentences, got {len(sentences)}"


def test_checklist_ends_with_newline():
    raw = CHECKLIST_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
