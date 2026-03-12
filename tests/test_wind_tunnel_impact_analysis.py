from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
WIND_TUNNEL_FILE = REPO_ROOT / "wind-tunnel-testing-3didae.md"


def test_file_exists():
    assert WIND_TUNNEL_FILE.exists(), f"{WIND_TUNNEL_FILE} does not exist"


def test_file_has_h1_heading():
    content = WIND_TUNNEL_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_mentions_wind_tunnel():
    content = WIND_TUNNEL_FILE.read_text(encoding="utf-8")
    assert "wind tunnel" in content.lower(), "File does not mention wind tunnel"


def test_file_under_80_lines():
    content = WIND_TUNNEL_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    assert len(lines) < 80, f"File has {len(lines)} lines, expected under 80"


def test_file_ends_with_newline():
    raw = WIND_TUNNEL_FILE.read_bytes()
    assert raw.endswith(b"\n"), "File does not end with a newline"
