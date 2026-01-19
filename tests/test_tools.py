"""Tests for tools."""

import tempfile
from pathlib import Path

import pytest

from sheep.tools.file_tools import DirectoryTreeTool, FileReadTool, FileWriteTool


class TestFileTools:
    """Tests for file operation tools."""

    def test_file_read_nonexistent(self):
        """Test reading a file that doesn't exist."""
        tool = FileReadTool()
        result = tool._run("/nonexistent/path/file.txt")
        assert "Error" in result
        assert "does not exist" in result

    def test_file_write_and_read(self):
        """Test writing and reading a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = f"{tmpdir}/test.txt"
            content = "Hello, Sheep!"

            # Write
            write_tool = FileWriteTool()
            result = write_tool._run(filepath, content)
            assert "Successfully wrote" in result

            # Read
            read_tool = FileReadTool()
            result = read_tool._run(filepath)
            assert result == content

    def test_file_read_with_line_range(self):
        """Test reading specific lines from a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = f"{tmpdir}/test.txt"
            content = "line1\nline2\nline3\nline4\nline5"

            # Write
            write_tool = FileWriteTool()
            write_tool._run(filepath, content)

            # Read lines 2-4
            read_tool = FileReadTool()
            result = read_tool._run(filepath, start_line=2, end_line=4)
            assert "line2" in result
            assert "line3" in result
            assert "line4" in result
            assert "line1" not in result
            assert "line5" not in result

    def test_directory_tree(self):
        """Test directory tree generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some structure
            Path(f"{tmpdir}/src").mkdir()
            Path(f"{tmpdir}/src/main.py").touch()
            Path(f"{tmpdir}/tests").mkdir()
            Path(f"{tmpdir}/tests/test_main.py").touch()

            tool = DirectoryTreeTool()
            result = tool._run(tmpdir, max_depth=2)

            assert "src" in result
            assert "tests" in result
            assert "main.py" in result
