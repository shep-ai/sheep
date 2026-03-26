#!/usr/bin/env python3
"""
Tests for feature 223: markdown-file-creation-995640
Tests the create_file() function and git integration functions.
"""

import subprocess
import sys
from pathlib import Path
import tempfile
import os

# Import the script module
sys.path.insert(0, str(Path(__file__).parent))
from create_markdown_file_223 import (
    create_file,
    git_add,
    git_commit,
    git_push,
    FILENAME,
    TITLE,
    PROSE,
    COMMIT_MESSAGE,
)


def test_create_file_basic():
    """Test that create_file() creates the file with correct content."""
    # Clean up if file exists from prior runs
    if Path(FILENAME).exists():
        Path(FILENAME).unlink()

    # Verify file doesn't exist before
    assert not Path(FILENAME).exists(), f"{FILENAME} should not exist before test"

    # Call create_file()
    result = create_file()

    # Verify file exists after
    assert Path(FILENAME).exists(), f"{FILENAME} should exist after create_file()"

    # Verify result is a Path object
    assert isinstance(result, Path), "create_file() should return a Path object"
    assert result.name == FILENAME, f"Returned path should have name {FILENAME}"

    # Verify file content
    content = Path(FILENAME).read_text(encoding="utf-8")
    assert f"# {TITLE}" in content, "File should contain H1 heading with TITLE"
    assert PROSE in content, "File should contain PROSE"

    # Clean up
    Path(FILENAME).unlink()


def test_create_file_encoding():
    """Test that create_file() creates file with UTF-8 encoding."""
    # Clean up if file exists from prior runs
    if Path(FILENAME).exists():
        Path(FILENAME).unlink()

    # Call create_file()
    create_file()

    # Verify UTF-8 encoding
    # Read file and verify it's valid UTF-8
    with open(FILENAME, "rb") as f:
        raw_bytes = f.read()

    try:
        raw_bytes.decode("utf-8")
        # If this succeeds, file is valid UTF-8
        is_utf8 = True
    except UnicodeDecodeError:
        is_utf8 = False

    assert is_utf8, "File should be encoded in UTF-8"

    # Clean up
    Path(FILENAME).unlink()


def test_create_file_line_endings():
    """Test that create_file() creates file with LF line endings (not CRLF)."""
    # Clean up if file exists from prior runs
    if Path(FILENAME).exists():
        Path(FILENAME).unlink()

    # Call create_file()
    create_file()

    # Read file in binary to check line endings
    with open(FILENAME, "rb") as f:
        raw_bytes = f.read()

    # Check for CRLF (Windows line endings) - should NOT exist
    has_crlf = b"\r\n" in raw_bytes
    assert not has_crlf, "File should use LF line endings, not CRLF"

    # Check for LF (Unix line endings) - should exist
    has_lf = b"\n" in raw_bytes
    assert has_lf, "File should contain LF line endings"

    # Clean up
    Path(FILENAME).unlink()


def test_create_file_markdown_structure():
    """Test that create_file() creates proper markdown structure."""
    # Clean up if file exists from prior runs
    if Path(FILENAME).exists():
        Path(FILENAME).unlink()

    # Call create_file()
    create_file()

    # Read file content
    content = Path(FILENAME).read_text(encoding="utf-8")
    lines = content.split("\n")

    # Verify H1 heading on first line
    assert lines[0] == f"# {TITLE}", "First line should be H1 heading"

    # Verify blank line on second line
    assert lines[1] == "", "Second line should be blank"

    # Verify prose starts on third line
    assert PROSE in content, "Prose should be in the file"

    # Verify file ends with newline
    assert content.endswith("\n"), "File should end with newline"

    # Clean up
    Path(FILENAME).unlink()


def test_create_file_raises_fileexistserror():
    """Test that create_file() raises FileExistsError if file already exists."""
    # Clean up and create the file first
    if Path(FILENAME).exists():
        Path(FILENAME).unlink()
    Path(FILENAME).write_text("existing content")

    # Verify it exists
    assert Path(FILENAME).exists(), "File should exist for this test"

    # Call create_file() - should raise FileExistsError
    try:
        create_file()
        assert False, "create_file() should raise FileExistsError if file exists"
    except FileExistsError as e:
        # Expected exception
        assert FILENAME in str(e), "Error message should mention the filename"
    finally:
        # Clean up
        if Path(FILENAME).exists():
            Path(FILENAME).unlink()


def test_create_file_docstring():
    """Test that create_file() has a docstring."""
    assert create_file.__doc__ is not None, "create_file() should have a docstring"
    assert len(create_file.__doc__) > 20, "Docstring should be descriptive"


def test_git_add_executable():
    """Test that git_add() function is callable and uses subprocess."""
    # Just verify the function exists and is callable
    assert callable(git_add), "git_add should be callable"
    # Verify it has proper subprocess integration via import check
    import inspect
    source = inspect.getsource(git_add)
    assert "subprocess.run" in source, "git_add should use subprocess.run"
    assert "git" in source and "add" in source, "git_add should contain git add command"


def test_git_commit_executable():
    """Test that git_commit() function is callable and uses subprocess."""
    # Just verify the function exists and is callable
    assert callable(git_commit), "git_commit should be callable"
    # Verify it has proper subprocess integration via import check
    import inspect
    source = inspect.getsource(git_commit)
    assert "subprocess.run" in source, "git_commit should use subprocess.run"
    assert "git" in source and "commit" in source, "git_commit should contain git commit command"
    assert "COMMIT_MESSAGE" in source, "git_commit should use COMMIT_MESSAGE constant"


def test_git_add_has_docstring():
    """Test that git_add() has a docstring."""
    assert git_add.__doc__ is not None, "git_add() should have a docstring"
    assert len(git_add.__doc__) > 10, "Docstring should be descriptive"


def test_git_commit_has_docstring():
    """Test that git_commit() has a docstring."""
    assert git_commit.__doc__ is not None, "git_commit() should have a docstring"
    assert len(git_commit.__doc__) > 10, "Docstring should be descriptive"


def test_git_push_has_docstring():
    """Test that git_push() has a docstring."""
    assert git_push.__doc__ is not None, "git_push() should have a docstring"
    assert len(git_push.__doc__) > 10, "Docstring should be descriptive"


if __name__ == "__main__":
    # Run tests manually if desired
    test_create_file_basic()
    print("✓ test_create_file_basic passed")

    test_create_file_encoding()
    print("✓ test_create_file_encoding passed")

    test_create_file_line_endings()
    print("✓ test_create_file_line_endings passed")

    test_create_file_markdown_structure()
    print("✓ test_create_file_markdown_structure passed")

    test_create_file_raises_fileexistserror()
    print("✓ test_create_file_raises_fileexistserror passed")

    test_create_file_docstring()
    print("✓ test_create_file_docstring passed")

    test_git_add_has_docstring()
    print("✓ test_git_add_has_docstring passed")

    test_git_commit_has_docstring()
    print("✓ test_git_commit_has_docstring passed")

    test_git_push_has_docstring()
    print("✓ test_git_push_has_docstring passed")

    test_git_add_executable()
    print("✓ test_git_add_executable passed")

    test_git_commit_executable()
    print("✓ test_git_commit_executable passed")

    print("\nAll tests passed!")
