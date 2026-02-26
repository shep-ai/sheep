"""File operation tools for agents."""

import subprocess
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)


class FileReadInput(BaseModel):
    """Input for reading a file."""

    file_path: str = Field(description="Path to the file to read")
    start_line: int | None = Field(
        default=None, description="Starting line number (1-indexed)"
    )
    end_line: int | None = Field(
        default=None, description="Ending line number (inclusive)"
    )


class FileReadTool(BaseTool):
    """Read contents of a file."""

    name: str = "file_read"
    description: str = "Read the contents of a file. Can optionally read specific line ranges."
    args_schema: type[BaseModel] = FileReadInput

    def _run(
        self,
        file_path: str,
        start_line: int | None = None,
        end_line: int | None = None,
    ) -> str:
        path = Path(file_path)
        if not path.exists():
            return f"Error: File does not exist: {file_path}"

        if not path.is_file():
            return f"Error: Path is not a file: {file_path}"

        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

            if start_line is not None or end_line is not None:
                start = (start_line or 1) - 1
                end = end_line or len(lines)
                lines = lines[start:end]

            content = "".join(lines)

            # Limit output size
            if len(content) > 50000:
                content = content[:50000] + "\n... (truncated)"

            return content
        except Exception as e:
            return f"Error reading file: {e}"


class FileWriteInput(BaseModel):
    """Input for writing a file."""

    file_path: str = Field(description="Path to the file to write")
    content: str = Field(description="Content to write to the file")
    create_dirs: bool = Field(
        default=True, description="Create parent directories if they don't exist"
    )


class FileWriteTool(BaseTool):
    """Write content to a file."""

    name: str = "file_write"
    description: str = "Write content to a file. Creates the file if it doesn't exist."
    args_schema: type[BaseModel] = FileWriteInput

    def _run(
        self,
        file_path: str,
        content: str,
        create_dirs: bool = True,
    ) -> str:
        path = Path(file_path)

        try:
            if create_dirs and not path.parent.exists():
                path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"Successfully wrote {len(content)} characters to {file_path}"
        except Exception as e:
            return f"Error writing file: {e}"


class FileSearchInput(BaseModel):
    """Input for searching files."""

    directory: str = Field(description="Directory to search in")
    pattern: str = Field(description="Search pattern (regex or text)")
    file_pattern: str = Field(
        default="*", description="File glob pattern (e.g., '*.py', '*.ts')"
    )
    max_results: int = Field(default=50, description="Maximum number of results")


class FileSearchTool(BaseTool):
    """Search for patterns in files."""

    name: str = "file_search"
    description: str = "Search for a pattern in files within a directory using ripgrep."
    args_schema: type[BaseModel] = FileSearchInput

    def _run(
        self,
        directory: str,
        pattern: str,
        file_pattern: str = "*",
        max_results: int = 50,
    ) -> str:
        path = Path(directory)
        if not path.exists():
            return f"Error: Directory does not exist: {directory}"

        try:
            # Try ripgrep first, fall back to grep
            cmd = [
                "rg",
                "--line-number",
                "--with-filename",
                f"--max-count={max_results}",
                f"--glob={file_pattern}",
                pattern,
                str(path),
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                return result.stdout if result.stdout.strip() else "No matches found."
            elif result.returncode == 1:
                return "No matches found."
            else:
                # Fall back to grep
                return self._grep_fallback(path, pattern, file_pattern, max_results)

        except FileNotFoundError:
            return self._grep_fallback(path, pattern, file_pattern, max_results)
        except subprocess.TimeoutExpired:
            return "Error: Search timed out"
        except Exception as e:
            return f"Error during search: {e}"

    def _grep_fallback(
        self,
        path: Path,
        pattern: str,
        file_pattern: str,
        max_results: int,
    ) -> str:
        """Fallback to grep if ripgrep is not available."""
        try:
            cmd = [
                "grep",
                "-r",
                "-n",
                f"--include={file_pattern}",
                pattern,
                str(path),
            ]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout
            if output:
                lines = output.strip().split("\n")[:max_results]
                return "\n".join(lines)
            return "No matches found."
        except Exception as e:
            return f"Error during grep fallback: {e}"


class DirectoryTreeInput(BaseModel):
    """Input for directory tree."""

    directory: str = Field(description="Directory to show tree for")
    max_depth: int = Field(default=3, description="Maximum depth to traverse")
    show_hidden: bool = Field(default=False, description="Show hidden files")


class DirectoryTreeTool(BaseTool):
    """Show directory structure as a tree."""

    name: str = "directory_tree"
    description: str = "Show the directory structure as a tree for understanding project layout."
    args_schema: type[BaseModel] = DirectoryTreeInput

    def _run(
        self,
        directory: str,
        max_depth: int = 3,
        show_hidden: bool = False,
    ) -> str:
        path = Path(directory)
        if not path.exists():
            return f"Error: Directory does not exist: {directory}"

        lines: list[str] = []
        self._build_tree(path, lines, "", max_depth, show_hidden)
        return "\n".join(lines)

    def _build_tree(
        self,
        path: Path,
        lines: list[str],
        prefix: str,
        max_depth: int,
        show_hidden: bool,
        depth: int = 0,
    ) -> None:
        """Recursively build tree representation."""
        if depth > max_depth:
            return

        if depth == 0:
            lines.append(str(path))
        else:
            name = path.name
            if path.is_dir():
                name += "/"
            lines.append(f"{prefix}{name}")

        if path.is_dir() and depth < max_depth:
            try:
                entries = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name))
                entries = [e for e in entries if show_hidden or not e.name.startswith(".")]

                # Limit entries to prevent huge outputs
                if len(entries) > 50:
                    entries = entries[:50]
                    truncated = True
                else:
                    truncated = False

                for i, entry in enumerate(entries):
                    is_last = i == len(entries) - 1 and not truncated
                    connector = "└── " if is_last else "├── "
                    prefix + ("    " if is_last else "│   ")

                    self._build_tree(
                        entry,
                        lines,
                        prefix + connector,
                        max_depth,
                        show_hidden,
                        depth + 1,
                    )

                if truncated:
                    lines.append(f"{prefix}└── ... (truncated)")

            except PermissionError:
                lines.append(f"{prefix}└── [permission denied]")
