from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CLOUD_COMPUTING_FILE = REPO_ROOT / "cloud-computing-xwbxsh.md"


def test_file_exists():
    assert CLOUD_COMPUTING_FILE.exists(), f"{CLOUD_COMPUTING_FILE} does not exist"


def test_file_has_h1_heading():
    content = CLOUD_COMPUTING_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_cloud_computing():
    content = CLOUD_COMPUTING_FILE.read_text(encoding="utf-8")
    assert "cloud computing" in content.lower(), "File does not mention cloud computing"


def test_file_under_80_lines():
    content = CLOUD_COMPUTING_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = CLOUD_COMPUTING_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
