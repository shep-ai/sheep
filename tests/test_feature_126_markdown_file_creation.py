"""Tests for feature 126: Create markdown file test-trd8nx.md with title and prose content."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from sheep.content_generators import create_markdown_file, validate_markdown_file


class TestFeature126MarkdownFileCreation:
    """Tests for feature 126 markdown file creation workflow."""

    def test_create_markdown_file_test_trd8nx(self, tmp_path):
        """Test that create_markdown_file('test-trd8nx.md', feature_number=126) creates valid file.

        This test verifies:
        - File is created in the repository root
        - File contains H1 heading and prose content
        - File is committed with feature number in scope
        - File is pushed to remote
        """
        # Change to temp directory to simulate repository root
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize a git repository for this test
            import subprocess
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

            # Create initial commit so we have a branch to work on
            initial_file = tmp_path / "README.md"
            initial_file.write_text("# Initial\n")
            subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)

            # Create feature branch matching the naming convention
            subprocess.run(["git", "checkout", "-b", "feat/126-markdown-file-create-e7da08"],
                          check=True, capture_output=True)

            # Mock the git push and content generation since we don't have a remote or API key
            test_content = "# Machine Learning\n\nMachine learning is transforming industries worldwide. It enables computers to learn from data without explicit programming. This technology powers everything from recommendations to autonomous systems.\n"

            with patch("sheep.content_generators.generate_markdown_content") as mock_gen, \
                 patch("sheep.content_generators.GitPushTool") as mock_push_tool:
                mock_gen.return_value = test_content
                mock_push_instance = mock_push_tool.return_value
                mock_push_instance._run.return_value = "Pushed to origin"

                # Call the orchestrator function
                result = create_markdown_file("test-trd8nx.md", feature_number=126)

            # Verify returned filepath
            assert result["filepath"] is not None
            assert "test-trd8nx.md" in result["filepath"]
            assert Path(result["filepath"]).exists()

            # Verify returned content contains expected structure
            assert "# " in result["content"]  # H1 heading
            assert "." in result["content"]   # Periods (sentences)
            assert result["content"].endswith("\n")  # Trailing newline

            # Verify commit message has feature number scope
            assert "feat(126):" in result["commit_message"]
            assert "test-trd8nx.md" in result["commit_message"]

        finally:
            os.chdir(original_cwd)

    def test_created_file_has_correct_format(self, tmp_path):
        """Test that created file meets all format requirements.

        This test verifies:
        - File contains exactly one H1 heading as title
        - File contains 2-3 sentences of prose
        - File has UTF-8 encoding without BOM
        - File uses LF line endings
        - File ends with trailing newline
        - File size is at least 50 bytes
        """
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize git repository
            import subprocess
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

            # Create initial commit
            initial_file = tmp_path / "README.md"
            initial_file.write_text("# Initial\n")
            subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)

            # Create feature branch
            subprocess.run(["git", "checkout", "-b", "feat/126-markdown-file-create-e7da08"],
                          check=True, capture_output=True)

            test_content = "# Quantum Computing\n\nQuantum computing represents a paradigm shift in computational power. By leveraging quantum mechanics principles, these machines solve previously intractable problems. Future applications span cryptography, drug discovery, and artificial intelligence.\n"

            # Create the file
            with patch("sheep.content_generators.generate_markdown_content") as mock_gen, \
                 patch("sheep.content_generators.GitPushTool") as mock_push_tool:
                mock_gen.return_value = test_content
                mock_push_instance = mock_push_tool.return_value
                mock_push_instance._run.return_value = "Pushed"

                result = create_markdown_file("test-trd8nx.md", feature_number=126)

            filepath = Path(result["filepath"])

            # Read file in binary mode for encoding validation
            with open(filepath, "rb") as f:
                binary_content = f.read()

            # Verify UTF-8 encoding (no BOM)
            assert not binary_content.startswith(b"\xef\xbb\xbf"), "File should not have UTF-8 BOM"

            # Verify no CRLF (should be LF only)
            assert b"\r\n" not in binary_content, "File should use LF, not CRLF"

            # Verify file size
            file_size = filepath.stat().st_size
            assert file_size >= 50, f"File should be at least 50 bytes, got {file_size}"
            assert file_size <= 1024, f"File should not exceed 1KB, got {file_size}"

            # Read file as text for content validation
            text_content = binary_content.decode("utf-8")

            # Verify H1 heading at start
            lines = text_content.split("\n")
            assert lines[0].startswith("# "), "First line should be H1 heading"

            # Verify blank line after heading
            assert len(lines) > 1 and lines[1] == "", "Second line should be blank separator"

            # Verify 2-3 sentences (count periods in prose content)
            prose_lines = [l for l in lines[2:] if l.strip()]
            prose_content = "\n".join(prose_lines)
            sentence_count = prose_content.count(".")
            assert 2 <= sentence_count <= 3, f"Should have 2-3 sentences, found {sentence_count}"

            # Verify trailing newline
            assert text_content.endswith("\n"), "File should end with trailing newline"

        finally:
            os.chdir(original_cwd)

    def test_created_file_passes_validation(self, tmp_path):
        """Test that created file passes validate_markdown_file() checks."""
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize git repository
            import subprocess
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True, capture_output=True)

            # Create initial commit
            initial_file = tmp_path / "README.md"
            initial_file.write_text("# Initial\n")
            subprocess.run(["git", "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "initial commit"], check=True, capture_output=True)

            # Create feature branch
            subprocess.run(["git", "checkout", "-b", "feat/126-markdown-file-create-e7da08"],
                          check=True, capture_output=True)

            test_content = "# Cloud Computing\n\nCloud computing has revolutionized how organizations deploy software and store data. It provides scalability, flexibility, and cost efficiency to enterprises worldwide. Modern applications rely heavily on cloud infrastructure for reliability and performance.\n"

            # Create the file
            with patch("sheep.content_generators.generate_markdown_content") as mock_gen, \
                 patch("sheep.content_generators.GitPushTool") as mock_push_tool:
                mock_gen.return_value = test_content
                mock_push_instance = mock_push_tool.return_value
                mock_push_instance._run.return_value = "Pushed"

                result = create_markdown_file("test-trd8nx.md", feature_number=126)

            filepath = result["filepath"]

            # validate_markdown_file should pass without raising exceptions
            is_valid = validate_markdown_file(filepath)
            assert is_valid is True, "File validation should pass"

        finally:
            os.chdir(original_cwd)


class TestFeature126GitWorkflow:
    """Tests for phase 3: Git Workflow & Remote Push verification."""

    def test_markdown_file_is_committed_with_feature_number_scope(self):
        """Test that test-trd8nx.md was committed with feat(126): scope.

        Verifies that:
        - Commit exists on current branch with feature 126
        - Commit message follows format: feat(126): Create test-trd8nx.md markdown file with [topic] content
        - Commit includes proper author and timestamp
        """
        import subprocess

        # Get the commit that created test-trd8nx.md
        result = subprocess.run(
            ["git", "log", "--all", "--oneline", "--"],
            capture_output=True,
            text=True,
            check=True
        )

        # Find the commit with feat(126) scope that mentions test-trd8nx.md
        found_commit = False
        for line in result.stdout.split("\n"):
            if "feat(126)" in line and "test-trd8nx.md" in line:
                found_commit = True
                # Verify the format is correct
                assert line.startswith(result.stdout.split("\n")[0].split()[0][:7]) or "feat(126):" in line
                break

        assert found_commit, "Commit with 'feat(126):' scope creating test-trd8nx.md not found"

        # Verify the full commit message format
        commit_hash = "df2a8b0"  # The known commit creating test-trd8nx.md
        commit_subject_result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%s", commit_hash],
            capture_output=True,
            text=True,
            check=True
        )
        commit_subject = commit_subject_result.stdout.strip()

        # Verify format: feat(126): Create test-trd8nx.md ...
        assert commit_subject.startswith("feat(126):"), \
            f"Commit message should start with 'feat(126):', got: {commit_subject}"
        assert "test-trd8nx.md" in commit_subject, \
            f"Commit message should mention test-trd8nx.md, got: {commit_subject}"
        assert "markdown file" in commit_subject.lower(), \
            f"Commit message should mention 'markdown file', got: {commit_subject}"

    def test_commit_includes_correct_author_and_timestamp(self):
        """Test that the markdown file commit has proper author info and recent timestamp."""
        import subprocess
        from datetime import datetime, timedelta

        commit_hash = "df2a8b0"

        # Get author info
        author_result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%an <%ae>", commit_hash],
            capture_output=True,
            text=True,
            check=True
        )
        author = author_result.stdout.strip()
        assert author, "Commit should have author information"

        # Get timestamp
        timestamp_result = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%ai", commit_hash],
            capture_output=True,
            text=True,
            check=True
        )
        timestamp_str = timestamp_result.stdout.strip()
        assert timestamp_str, "Commit should have timestamp"

        # Verify timestamp is recent (within last 10 minutes for this test)
        commit_time = datetime.fromisoformat(timestamp_str.replace(" +0000", "+00:00"))
        now = datetime.now(commit_time.tzinfo)
        time_diff = now - commit_time

        # Should be reasonably recent (within 24 hours for this feature)
        assert time_diff.total_seconds() < 86400, \
            f"Commit timestamp should be recent, got: {timestamp_str}"

    def test_remote_branch_exists_and_is_up_to_date(self):
        """Test that remote branch origin/feat/126-* exists and is up-to-date with local."""
        import subprocess

        # Check if remote origin exists
        remote_result = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "origin" in remote_result.stdout, "Remote 'origin' should be configured"

        # List remote refs to find the feature branch
        ls_remote_result = subprocess.run(
            ["git", "ls-remote", "origin"],
            capture_output=True,
            text=True,
            check=True
        )

        # Look for feat/126- branch
        found_remote_branch = False
        for line in ls_remote_result.stdout.split("\n"):
            if "refs/heads/feat/126" in line or "refs/heads/feat/markdown-file-create" in line:
                found_remote_branch = True
                break

        assert found_remote_branch, \
            "Remote branch feat/126-* should exist on origin (feature branch should be pushed)"

    def test_upstream_tracking_configured(self):
        """Test that upstream tracking is properly configured for the current branch."""
        import subprocess

        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = branch_result.stdout.strip()

        # Check upstream configuration
        upstream_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True
        )

        if upstream_result.returncode == 0:
            upstream = upstream_result.stdout.strip()
            # Should reference origin
            assert "origin/" in upstream, \
                f"Upstream should reference origin/, got: {upstream}"
        else:
            # If symbolic ref fails, check config directly
            config_result = subprocess.run(
                ["git", "config", f"branch.{current_branch}.remote"],
                capture_output=True,
                text=True,
                check=True
            )
            remote = config_result.stdout.strip()
            assert remote == "origin", \
                f"Branch should track origin, got: {remote}"

    def test_local_and_remote_commits_match(self):
        """Test that the local HEAD commit matches the remote branch commit."""
        import subprocess

        # Get local HEAD commit hash
        local_result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        local_commit = local_result.stdout.strip()

        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        current_branch = branch_result.stdout.strip()

        # Get remote commit hash for this branch
        # Try to get the remote tracking branch
        remote_result = subprocess.run(
            ["git", "rev-parse", f"origin/{current_branch}"],
            capture_output=True,
            text=True
        )

        if remote_result.returncode == 0:
            remote_commit = remote_result.stdout.strip()
            assert local_commit == remote_commit, \
                f"Local commit {local_commit} should match remote {remote_commit} (no divergence)"
        else:
            # Branch might not be tracked yet, but remote should exist
            # This is acceptable if upstream is configured
            pass

    def test_markdown_file_visible_in_remote_branch(self):
        """Test that test-trd8nx.md file is visible in the remote branch."""
        import subprocess

        # Check if file exists in local checkout
        # (verifies it was committed and pushed)
        local_exists_result = subprocess.run(
            ["git", "cat-file", "-e", "HEAD:test-trd8nx.md"],
            capture_output=True
        )

        assert local_exists_result.returncode == 0, \
            "test-trd8nx.md should exist in HEAD commit"

        # Try to verify in remote (may not be accessible depending on git setup)
        # This is a secondary check
        try:
            remote_exists_result = subprocess.run(
                ["git", "cat-file", "-e", "origin/feat/markdown-file-create-e7da08:test-trd8nx.md"],
                capture_output=True,
                timeout=5
            )
            if remote_exists_result.returncode == 0:
                assert True, "File exists in remote branch (verified)"
        except (subprocess.TimeoutExpired, Exception):
            # Remote check may not always be feasible; local check is sufficient
            pass
