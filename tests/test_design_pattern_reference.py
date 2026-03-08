from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DESIGN_PATTERN_REF_FILE = REPO_ROOT / "DESIGN_PATTERN_REFERENCE.md"


def test_file_exists():
    assert DESIGN_PATTERN_REF_FILE.exists(), f"{DESIGN_PATTERN_REF_FILE} does not exist"


def test_file_has_h1_heading():
    content = DESIGN_PATTERN_REF_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_contains_python_code_block():
    content = DESIGN_PATTERN_REF_FILE.read_text(encoding="utf-8")
    assert "```python" in content, "File does not contain a python code block"


def test_file_contains_design_pattern_sections():
    content = DESIGN_PATTERN_REF_FILE.read_text(encoding="utf-8")
    assert "## Overview" in content, "File does not contain Overview section"
    assert "## When to Use" in content, "File does not contain When to Use section"
    assert "## Trade-offs" in content, "File does not contain Trade-offs section"
