"""Helpers for validating markdown file properties for task-3."""

from pathlib import Path
import re


def validate_markdown_encoding(filepath: str | Path) -> dict:
    """
    Validate markdown file encoding is UTF-8 without BOM.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    # Check if file exists
    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    # Read file as bytes to check BOM
    with open(filepath, "rb") as f:
        content_bytes = f.read()

    # Check for UTF-8 BOM (EF BB BF)
    if content_bytes.startswith(b'\xef\xbb\xbf'):
        return {"valid": False, "error": "File has UTF-8 BOM (should not have BOM)"}

    # Try to decode as UTF-8
    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError as e:
        return {"valid": False, "error": f"File is not valid UTF-8: {e}"}

    return {"valid": True, "content": content_str}


def validate_markdown_line_endings(filepath: str | Path) -> dict:
    """
    Validate markdown file uses Unix LF line endings, not CRLF.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    # Read file as bytes to check line endings
    with open(filepath, "rb") as f:
        content_bytes = f.read()

    # Check for CRLF (Windows line endings)
    if b'\r\n' in content_bytes:
        return {"valid": False, "error": "File has CRLF line endings (should have LF only)"}

    # Check for CR without LF (old Mac)
    if b'\r' in content_bytes and b'\n' not in content_bytes:
        return {"valid": False, "error": "File has CR line endings (should have LF)"}

    return {"valid": True}


def validate_markdown_h1_heading(filepath: str | Path) -> dict:
    """
    Validate markdown file has H1 heading at start.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    if not lines or not lines[0].startswith("# "):
        return {"valid": False, "error": "First line is not an H1 heading (# Title)"}

    # Check for blank line after H1
    if len(lines) < 2 or lines[1].strip() != "":
        return {"valid": False, "error": "H1 heading not followed by blank line"}

    return {"valid": True, "heading": lines[0]}


def validate_markdown_sentence_count(filepath: str | Path) -> dict:
    """
    Validate markdown file has 2-3 sentences of prose content.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Count periods in prose (after heading)
    lines = content.split("\n")
    # Prose is everything after the heading and blank line
    prose_lines = lines[2:] if len(lines) > 2 else []
    prose = "\n".join(prose_lines)

    # Count periods as sentence markers
    period_count = prose.count(".")

    if period_count < 2 or period_count > 3:
        return {
            "valid": False,
            "error": f"File has {period_count} periods (should have 2-3 sentences)"
        }

    return {"valid": True, "sentence_count": period_count}


def validate_markdown_trailing_newline(filepath: str | Path) -> dict:
    """
    Validate markdown file has trailing newline at end.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    with open(filepath, "rb") as f:
        content_bytes = f.read()

    if not content_bytes.endswith(b'\n'):
        return {"valid": False, "error": "File does not have trailing newline"}

    return {"valid": True}


def validate_markdown_file_size(filepath: str | Path, min_size: int = 300, max_size: int = 600) -> dict:
    """
    Validate markdown file size is in typical range.

    Args:
        filepath: Path to the markdown file
        min_size: Minimum file size in bytes
        max_size: Maximum file size in bytes

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    file_size = filepath.stat().st_size

    if file_size < min_size or file_size > max_size:
        return {
            "valid": False,
            "error": f"File size {file_size} bytes is outside range {min_size}-{max_size}"
        }

    return {"valid": True, "size": file_size}


def validate_markdown_no_trailing_whitespace(filepath: str | Path) -> dict:
    """
    Validate markdown file has no trailing whitespace on lines.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Check for trailing whitespace (except newlines)
    for i, line in enumerate(lines, 1):
        if line.rstrip('\n') != line.rstrip('\n').rstrip():
            return {
                "valid": False,
                "error": f"Line {i} has trailing whitespace"
            }

    return {"valid": True}


def validate_markdown_grammar_check(filepath: str | Path) -> dict:
    """
    Basic grammar validation for markdown prose.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with validation results
    """
    filepath = Path(filepath)

    if not filepath.exists():
        return {"valid": False, "error": f"File {filepath} does not exist"}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    prose_lines = lines[2:] if len(lines) > 2 else []
    prose = "\n".join(prose_lines)

    # Basic checks
    # Check that sentences start with capital letter
    sentences = [s.strip() for s in prose.split(".") if s.strip()]

    for sentence in sentences:
        if sentence and not sentence[0].isupper():
            return {
                "valid": False,
                "error": f"Sentence does not start with capital letter: '{sentence}'"
            }

    # Check for common grammar issues
    if "  " in prose:
        return {"valid": False, "error": "Multiple consecutive spaces found (check formatting)"}

    return {"valid": True}


def validate_all_markdown_properties(filepath: str | Path) -> dict:
    """
    Run all validation checks on a markdown file.

    Args:
        filepath: Path to the markdown file

    Returns:
        Dictionary with all validation results
    """
    filepath = str(filepath)

    checks = {
        "encoding": validate_markdown_encoding(filepath),
        "line_endings": validate_markdown_line_endings(filepath),
        "h1_heading": validate_markdown_h1_heading(filepath),
        "sentence_count": validate_markdown_sentence_count(filepath),
        "trailing_newline": validate_markdown_trailing_newline(filepath),
        "file_size": validate_markdown_file_size(filepath),
        "trailing_whitespace": validate_markdown_no_trailing_whitespace(filepath),
        "grammar": validate_markdown_grammar_check(filepath),
    }

    # Determine overall validity
    all_valid = all(check.get("valid", False) for check in checks.values())

    return {
        "filepath": filepath,
        "all_valid": all_valid,
        "checks": checks,
        "summary": f"{sum(1 for c in checks.values() if c.get('valid'))} of {len(checks)} checks passed"
    }
