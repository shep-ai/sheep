from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
UV_FILE = REPO_ROOT / "ultraviolet-light.md"


def test_file_exists():
    assert UV_FILE.exists(), f"{UV_FILE} does not exist"


def test_file_has_h1_heading():
    content = UV_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_ultraviolet():
    content = UV_FILE.read_text(encoding="utf-8")
    assert "ultraviolet" in content.lower(), "File does not mention ultraviolet"


def test_file_has_taste_profile_chart():
    content = UV_FILE.read_text(encoding="utf-8")
    assert "|" in content, "File has no table (taste profile chart)"


def test_file_under_80_lines():
    content = UV_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = UV_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
