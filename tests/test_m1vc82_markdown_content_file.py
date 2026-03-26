from pathlib import Path

from sheep.content_generators import validate_markdown_file


def test_test_m1vc82_markdown_file_is_valid() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    path = repo_root / "test-m1vc82.md"

    assert validate_markdown_file(str(path)) is True

