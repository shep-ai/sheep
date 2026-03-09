import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
RANDOM_DESIGN_PATTERN_FILE = REPO_ROOT / "RANDOM_DESIGN_PATTERN.md"


def test_file_exists():
    assert RANDOM_DESIGN_PATTERN_FILE.exists(), f"{RANDOM_DESIGN_PATTERN_FILE} does not exist"


def test_file_has_h1_heading():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert any(line.startswith("# ") for line in content.splitlines()), "File has no H1 heading"


def test_file_contains_overview_section():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "## Overview" in content, "File does not contain Overview section"


def test_file_contains_structure_section():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "## Structure" in content, "File does not contain Structure section"


def test_file_contains_when_to_use_section():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "## When to Use" in content, "File does not contain When to Use section"


def test_file_contains_trade_offs_section():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "## Trade-offs" in content, "File does not contain Trade-offs section"


def test_file_contains_python_code_block():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    assert "```python" in content, "File does not contain a Python code block"


def test_python_code_is_syntactically_valid():
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    match = re.search(r"```python\n(.*?)```", content, re.DOTALL)
    assert match, "No Python code block found"
    code = match.group(1).strip()
    try:
        ast.parse(code)
    except SyntaxError as e:
        raise AssertionError(f"Python code has syntax error: {e}") from e


def test_file_documents_distinct_pattern():
    """Ensure the pattern is not Observer or Strategy (already documented elsewhere)."""
    content = RANDOM_DESIGN_PATTERN_FILE.read_text(encoding="utf-8")
    first_heading = next(
        (line for line in content.splitlines() if line.startswith("# ")), ""
    )
    assert "Observer" not in first_heading, "File documents Observer (already in DESIGN_PATTERN.md)"
    assert "Strategy" not in first_heading, "File documents Strategy (already in DESIGN_PATTERN_SUMMARY.md)"
