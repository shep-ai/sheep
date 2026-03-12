from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
ENAMEL_FILE = REPO_ROOT / "enamel-art-pz8a65.md"


def test_file_exists():
    assert ENAMEL_FILE.exists(), f"{ENAMEL_FILE} does not exist"


def test_file_has_h1_heading():
    content = ENAMEL_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_enamel():
    content = ENAMEL_FILE.read_text(encoding="utf-8")
    assert "enamel" in content.lower(), "File does not mention enamel"


def test_file_has_provenance_content():
    content = ENAMEL_FILE.read_text(encoding="utf-8")
    assert "provenance" in content.lower() or "custody" in content.lower(), \
        "File does not contain provenance record content"


def test_file_under_80_lines():
    content = ENAMEL_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = ENAMEL_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
