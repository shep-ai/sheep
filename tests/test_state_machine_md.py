from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STATE_MACHINE_FILE = REPO_ROOT / "STATE_MACHINE.md"


def test_file_exists():
    assert STATE_MACHINE_FILE.exists(), f"{STATE_MACHINE_FILE} does not exist"


def test_file_contains_mermaid_block():
    content = STATE_MACHINE_FILE.read_text(encoding="utf-8")
    assert "```mermaid" in content, "File does not contain a mermaid code block"


def test_file_contains_statediagram_v2():
    content = STATE_MACHINE_FILE.read_text(encoding="utf-8")
    assert "stateDiagram-v2" in content, "File does not contain stateDiagram-v2"


def test_file_contains_all_traffic_light_states():
    content = STATE_MACHINE_FILE.read_text(encoding="utf-8")
    assert "Red" in content, "File does not contain state: Red"
    assert "Green" in content, "File does not contain state: Green"
    assert "Yellow" in content, "File does not contain state: Yellow"


def test_file_has_h1_heading():
    content = STATE_MACHINE_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_size_under_1kb():
    size = STATE_MACHINE_FILE.stat().st_size
    assert size < 1024, f"File size {size} bytes exceeds 1 KB"
