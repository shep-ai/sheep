from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BEEKEEPING_FILE = REPO_ROOT / "test-local-abc123.md"


def test_file_exists():
    assert BEEKEEPING_FILE.exists(), f"{BEEKEEPING_FILE} does not exist"


def test_file_has_h1_heading():
    content = BEEKEEPING_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_has_fun_facts_content():
    content = BEEKEEPING_FILE.read_text(encoding="utf-8")
    sentences = [s.strip() for s in content.split(".") if s.strip() and not s.strip().startswith("#")]
    assert len(sentences) >= 2, "File should contain at least 2-3 sentences of fun facts"


def test_file_ends_with_newline():
    raw = BEEKEEPING_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
