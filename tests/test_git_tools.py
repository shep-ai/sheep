"""Tests for git tools."""

import tempfile
from unittest.mock import MagicMock, patch

from sheep.tools.git_tools import GitStatusTool


class TestGitStatusTool:
    """Tests for GitStatusTool._run() covering all reachable branches."""

    def test_path_not_found(self):
        """Test that a nonexistent repo path returns an error string."""
        tool = GitStatusTool()
        result = tool._run("/nonexistent/repo/path")
        assert "Error" in result
        assert "does not exist" in result

    def test_clean_working_tree(self):
        """Test that empty git status output returns a clean-tree message."""
        tool = GitStatusTool()
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = MagicMock()
            mock_result.stdout = ""
            with patch("sheep.tools.git_tools.subprocess.run", return_value=mock_result):
                result = tool._run(tmpdir)
        assert "Working tree is clean" in result

    def test_dirty_working_tree(self):
        """Test that non-empty git status output is returned as-is."""
        tool = GitStatusTool()
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_result = MagicMock()
            mock_result.stdout = "M  README.md\n"
            with patch("sheep.tools.git_tools.subprocess.run", return_value=mock_result):
                result = tool._run(tmpdir)
        assert "M  README.md" in result
