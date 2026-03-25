from pathlib import Path

from validate_markdown import ValidationError, validate_file


def test_test_smblg0_markdown_file_passes_validation() -> None:
    """Ensure `test-smblg0.md` satisfies repository markdown constraints."""
    path = Path("test-smblg0.md")
    assert path.exists(), "Expected test-smblg0.md to exist in repository root"

    try:
        validate_file(path)
    except ValidationError as e:  # pragma: no cover - assertion below covers failures
        raise AssertionError(f"test-smblg0.md failed validation: {e}") from e

