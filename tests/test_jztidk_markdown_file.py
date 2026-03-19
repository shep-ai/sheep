from pathlib import Path

from sheep.content_generators import validate_markdown_file


def test_test_jztidk_md_is_valid_markdown_file():
    """Validate the newly created markdown fixture file."""
    path = Path("test-jztidk.md")
    assert path.exists(), "test-jztidk.md must exist at repository root"

    # Match the expected sizing constraints used across other fixtures.
    size = path.stat().st_size
    assert 320 <= size <= 600, f"File size {size} bytes is outside expected range"

    # Validate encoding, CRLF/LF, heading, blank-line separator, sentence count, etc.
    assert validate_markdown_file(str(path)) is True

    # Sanity check: no stray CR characters.
    content = path.read_bytes()
    assert b"\r\n" not in content
    assert b"\r" not in content

