from pathlib import Path

from validate_markdown import validate_file


def test_test_eu6asn_markdown_validation() -> None:
    """Ensure the generated markdown file matches repository validation rules."""
    path = Path("test-eu6asn.md")
    assert path.exists()
    validate_file(path)

