from pathlib import Path

from sheep.content_generators import validate_markdown_file


def test_gyl68r_markdown_file_valid() -> None:
    """Validate the repo markdown formatting constraints for this specific file."""
    path = Path("test-gyl68r.md")
    assert path.exists(), "test-gyl68r.md must exist at repository root"

    assert validate_markdown_file(str(path)) is True

    # Keep consistent with the stricter validation script in the repo.
    size = path.stat().st_size
    assert 320 <= size <= 600

