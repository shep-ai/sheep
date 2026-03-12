from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RANDOM_DESIGN_PATTERN_FILE = REPO_ROOT / "RANDOM_DESIGN_PATTERN.md"


def test_file_exists():
    assert RANDOM_DESIGN_PATTERN_FILE.exists(), f"{RANDOM_DESIGN_PATTERN_FILE} does not exist"


def test_file_has_h1_heading():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_contains_mermaid_block():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "```mermaid" in content, "File does not contain a mermaid code block"


def test_file_contains_class_diagram():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "classDiagram" in content, "File does not contain a classDiagram"


def test_file_contains_python_code_block():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "```python" in content, "File does not contain a Python code block"


def test_file_contains_pattern_description():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "## Overview" in content, "File does not contain an Overview section"
    assert "## When to Use" in content, "File does not contain a When to Use section"
    assert "## Trade-offs" in content, "File does not contain a Trade-offs section"
