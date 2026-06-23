from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
VIADUCT_FILE = REPO_ROOT / "viaduct-construction-izbuhg.md"


def test_viaduct_file_exists():
    assert VIADUCT_FILE.exists(), f"{VIADUCT_FILE} does not exist"


def test_viaduct_file_has_title():
    content = VIADUCT_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 title"


def test_viaduct_file_mentions_viaduct():
    content = VIADUCT_FILE.read_text(encoding="utf-8")
    assert "viaduct" in content.lower(), "File does not mention viaduct"


def test_viaduct_file_is_short():
    content = VIADUCT_FILE.read_text(encoding="utf-8")
    sentences = [s.strip() for s in content.replace("\n", " ").split(".") if s.strip()]
    assert 2 <= len(sentences) <= 5, f"Expected 2-5 sentences, got {len(sentences)}"


def test_viaduct_file_ends_with_newline():
    raw = VIADUCT_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
