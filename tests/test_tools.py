"""Tests for tools."""

import base64
import struct
import tempfile
import zlib
from pathlib import Path

from sheep.tools.file_tools import (
    AttachmentReadTool,
    DirectoryTreeTool,
    FileReadTool,
    FileWriteTool,
)


def _make_minimal_png() -> bytes:
    """Create a minimal valid 1x1 white PNG for testing."""
    sig = b"\x89PNG\r\n\x1a\n"

    def chunk(ctype: bytes, data: bytes) -> bytes:
        crc = struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + ctype + data + crc

    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(b"\x00\xff\xff\xff"))
    iend = chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


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


class TestAttachmentReadTool:
    """Tests for attachment reading tool."""

    def test_attachment_read_nonexistent_file(self):
        """Test reading an attachment that doesn't exist."""
        tool = AttachmentReadTool()
        result = tool._run("/nonexistent/path/image.png")
        assert "Error" in result
        assert "does not exist" in result

    def test_attachment_read_image_returns_base64(self):
        """Test that reading an image attachment returns base64 content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            png_path = f"{tmpdir}/screenshot.png"
            png_bytes = _make_minimal_png()
            with open(png_path, "wb") as f:
                f.write(png_bytes)

            tool = AttachmentReadTool()
            result = tool._run(png_path)

            assert "screenshot.png" in result
            assert "image/png" in result
            expected_b64 = base64.b64encode(png_bytes).decode("utf-8")
            assert expected_b64 in result

    def test_attachment_read_text_file_returns_content(self):
        """Test that reading a text attachment returns its content."""
        with tempfile.TemporaryDirectory() as tmpdir:
            txt_path = f"{tmpdir}/notes.txt"
            content = "This is a design note for the feature."
            with open(txt_path, "w") as f:
                f.write(content)

            tool = AttachmentReadTool()
            result = tool._run(txt_path)

            assert "notes.txt" in result
            assert content in result

    def test_attachment_read_jpeg_uses_correct_mime(self):
        """Test that JPEG files get the correct MIME type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            jpg_path = f"{tmpdir}/mockup.jpg"
            with open(jpg_path, "wb") as f:
                f.write(b"\xff\xd8\xff\xe0some jpeg data")

            tool = AttachmentReadTool()
            result = tool._run(jpg_path)

            assert "mockup.jpg" in result
            assert "image/jpeg" in result

    def test_attachment_read_path_is_directory(self):
        """Test error when path is a directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tool = AttachmentReadTool()
            result = tool._run(tmpdir)
            assert "Error" in result


class TestCodeImplementationStateAttachments:
    """Tests for attachment support in CodeImplementationState."""

    def test_state_has_attachments_field(self):
        """Test that CodeImplementationState has an attachments field."""
        from sheep.flows.code_implementation import CodeImplementationState

        state = CodeImplementationState(
            repo_path="/some/path",
            issue_description="Add login feature",
            attachments=["/path/to/mockup.png"],
        )
        assert state.attachments == ["/path/to/mockup.png"]

    def test_state_attachments_defaults_to_empty(self):
        """Test that attachments defaults to empty list."""
        from sheep.flows.code_implementation import CodeImplementationState

        state = CodeImplementationState(
            repo_path="/some/path",
            issue_description="Add login feature",
        )
        assert state.attachments == []

    def test_run_code_implementation_accepts_attachments(self):
        """Test that run_code_implementation accepts attachments parameter."""
        import inspect

        from sheep.flows.code_implementation import run_code_implementation

        sig = inspect.signature(run_code_implementation)
        assert "attachments" in sig.parameters
