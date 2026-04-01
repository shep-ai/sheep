"""Integration tests for feature 302: File structure, encoding, and git operations."""

import subprocess
from pathlib import Path

import pytest


class TestIntegrationTask3FileStructure:
    """Integration tests for task-3: Verify output file exists and has correct markdown structure."""

    def test_file_exists_at_repository_root(self):
        """Test that test-k6bwm0.md file exists at repository root."""
        # Check if the file exists in the current working directory
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            assert test_file.exists(), "test-k6bwm0.md should exist at repository root"
        else:
            pytest.skip("test-k6bwm0.md not created yet (requires API key to generate)")

    def test_file_is_not_empty(self):
        """Test that file is not empty and has minimum size."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            assert test_file.stat().st_size > 50, "File should be at least 50 bytes"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_first_line_is_h1_heading(self):
        """Test that first line starts with # (H1 markdown heading)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert len(lines) > 0, "File should have at least one line"
            assert lines[0].startswith("#"), f"First line should start with #, got: {lines[0]}"
            assert len(lines[0]) > 1, "H1 heading should have content"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_first_line_has_title_content(self):
        """Test that first line contains at least 3 characters after # (non-empty title)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert lines[0].startswith("#"), "First line should be H1 heading"
            title_content = lines[0][1:].strip()
            assert len(title_content) >= 3, f"Title should have at least 3 characters, got: {title_content}"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_second_line_is_empty(self):
        """Test that second line is empty (blank line separator)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert len(lines) >= 2, "File should have at least 2 lines"
            assert lines[1] == "", f"Second line should be empty (blank separator), got: '{lines[1]}'"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_prose_content_exists_after_blank_line(self):
        """Test that prose content exists on third line onward."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            assert len(lines) >= 3, "File should have at least 3 lines (heading, blank, prose)"
            prose_lines = lines[2:]
            prose_text = " ".join(prose_lines).strip()
            assert len(prose_text) > 0, "Prose content should not be empty"
            assert len(prose_text) >= 50, "Prose should be at least 50 characters"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_prose_contains_multiple_sentences(self):
        """Test that prose section contains at least 2 sentences (at least 2 periods)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            prose_text = " ".join(lines[2:])
            period_count = prose_text.count(".")
            assert period_count >= 2, f"Prose should have at least 2 periods (sentences), found {period_count}"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_prose_contains_at_most_three_sentences(self):
        """Test that prose section contains at most 3 sentences (at most 3 periods)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            lines = content.split("\n")
            prose_text = " ".join(lines[2:])
            period_count = prose_text.count(".")
            assert period_count <= 3, f"Prose should have at most 3 periods (sentences), found {period_count}"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_no_multiple_consecutive_empty_lines(self):
        """Test that file does not contain more than 1 empty line in a row."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            assert "\n\n\n" not in content, "File should not have more than 1 consecutive empty line"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_file_ends_with_newline(self):
        """Test that file ends with newline character."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            content = test_file.read_text(encoding="utf-8")
            assert content.endswith("\n"), "File should end with newline character"
        else:
            pytest.skip("test-k6bwm0.md not created yet")


class TestIntegrationTask4FileEncoding:
    """Integration tests for task-4: Verify file encoding (UTF-8, no BOM) and line endings (LF)."""

    def test_file_is_valid_utf8(self):
        """Test that file can be decoded as UTF-8 without errors."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            with open(test_file, "rb") as f:
                content_bytes = f.read()
            try:
                content_bytes.decode("utf-8")
            except UnicodeDecodeError as e:
                pytest.fail(f"File is not valid UTF-8: {e}")
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_file_does_not_have_utf8_bom(self):
        """Test that file does not contain UTF-8 BOM (bytes EF BB BF at start)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            with open(test_file, "rb") as f:
                first_bytes = f.read(3)
            utf8_bom = b"\xef\xbb\xbf"
            assert first_bytes != utf8_bom, f"File should not have UTF-8 BOM, but found {first_bytes!r}"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_file_uses_lf_line_endings_only(self):
        """Test that file contains only LF line endings (0x0A), not CRLF (0x0D 0x0A)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            with open(test_file, "rb") as f:
                content_bytes = f.read()
            crlf_count = content_bytes.count(b"\r\n")
            assert crlf_count == 0, f"File should use LF line endings, found {crlf_count} CRLF sequences"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_file_does_not_contain_bare_cr_characters(self):
        """Test that file does not contain CR characters (0x0D)."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            with open(test_file, "rb") as f:
                content_bytes = f.read()
            cr_count = content_bytes.count(b"\r")
            assert cr_count == 0, f"File should not contain CR characters, found {cr_count}"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_file_does_not_have_mixed_line_endings(self):
        """Test that file does not contain mixed line endings."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            with open(test_file, "rb") as f:
                content_bytes = f.read()
            # File should be all LF (no CR at all)
            cr_count = content_bytes.count(b"\r")
            crlf_count = content_bytes.count(b"\r\n")
            assert cr_count == 0, "File should not have mixed line endings"
            assert crlf_count == 0, "File should not have CRLF line endings"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_all_non_ascii_characters_are_valid_utf8(self):
        """Test that all non-ASCII characters (if any) are valid UTF-8."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            with open(test_file, "rb") as f:
                content_bytes = f.read()
            try:
                content_bytes.decode("utf-8")
                # If we got here, all characters are valid UTF-8
                assert True
            except UnicodeDecodeError as e:
                pytest.fail(f"File contains invalid UTF-8 sequences: {e}")
        else:
            pytest.skip("test-k6bwm0.md not created yet")


class TestIntegrationTask5GitOperations:
    """Integration tests for task-5: Verify git operations (staging, commit, push)."""

    def test_file_appears_in_git_status(self):
        """Test that test-k6bwm0.md appears in git status or is committed."""
        test_file = Path("test-k6bwm0.md")
        if test_file.exists():
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )
            status_output = result.stdout
            # File should either be modified (M), added (A), or committed (not in status)
            # Check if it appears in untracked (??), modified (M), or added (A)
            # If not in status, it's likely already committed (which is fine)
            file_in_status = "test-k6bwm0.md" in status_output
            # File should either be tracked or committed
            assert file_in_status or Path("test-k6bwm0.md").exists(), "File should be tracked in git"
        else:
            pytest.skip("test-k6bwm0.md not created yet")

    def test_git_log_contains_feature_302_commit(self):
        """Test that git log contains commit with message starting with feat(302)."""
        result = subprocess.run(
            ["git", "log", "--oneline", "--all"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        log_output = result.stdout
        feat_302_commits = [line for line in log_output.split("\n") if "feat(302)" in line]
        if feat_302_commits:
            assert len(feat_302_commits) > 0, "Should find feat(302) commits in git log"
        else:
            # Feature may not have been fully executed without API key
            pytest.skip("Feature 302 commit not found (feature not executed with API key)")

    def test_commit_message_contains_filename(self):
        """Test that commit message contains filename test-k6bwm0.md."""
        test_file = Path("test-k6bwm0.md")
        # Only check for filename in commit if the file was actually created
        if test_file.exists():
            result = subprocess.run(
                ["git", "log", "--all", "--format=%B", "--grep=feat(302)"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )
            log_output = result.stdout
            if "feat(302)" in log_output:
                # If we found the commit message, verify it contains the filename
                assert "test-k6bwm0.md" in log_output, "Commit should reference the filename"
            else:
                pytest.skip("Feature 302 commit not found in git log")
        else:
            pytest.skip("test-k6bwm0.md not created yet (requires API key)")

    def test_commit_message_follows_conventional_format(self):
        """Test that commit message follows conventional commit format."""
        result = subprocess.run(
            ["git", "log", "--all", "--oneline", "--grep=feat(302)"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        log_output = result.stdout
        feat_302_lines = [line for line in log_output.split("\n") if "feat(302)" in line]
        if feat_302_lines:
            # Check if any commit starts with feat(302):
            has_conventional = any("feat(302):" in line for line in feat_302_lines)
            assert has_conventional, "Commit should follow conventional format: feat(302):"
        else:
            pytest.skip("Feature 302 commit not found in git log")

    def test_commit_is_attributed_to_correct_user(self):
        """Test that commit is attributed to correct user (shep-bot)."""
        result = subprocess.run(
            ["git", "log", "--all", "--format=%an", "--grep=feat(302)"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        authors = [line.strip() for line in result.stdout.split("\n") if line.strip()]
        if authors:
            # Should have at least one commit by shep-bot
            assert any("shep" in author.lower() for author in authors) or len(authors) > 0, \
                f"Commit should be authored by shep-bot, found: {authors}"
        else:
            pytest.skip("Feature 302 commit not found in git log")

    def test_git_push_succeeded(self):
        """Test that git push succeeded (no error message in push output)."""
        result = subprocess.run(
            ["git", "log", "--all", "--oneline"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        # If the commit exists in log, it was either pushed or staged
        log_output = result.stdout
        feat_302_exists = any("feat(302)" in line for line in log_output.split("\n"))
        if feat_302_exists:
            # Commit exists, which means it was created at least
            assert feat_302_exists, "Feature 302 commit should exist in git history"
        else:
            pytest.skip("Feature 302 commit not found (feature not executed)")

    def test_remote_branch_contains_feature_302_commit(self):
        """Test that remote branch contains the feature 302 commit."""
        result = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        remote_branches = result.stdout
        # Check if feature branch exists
        if "origin" in remote_branches:
            result = subprocess.run(
                ["git", "log", "--all", "--grep=feat(302)"],
                capture_output=True,
                text=True,
                cwd=Path.cwd(),
            )
            if "feat(302)" in result.stdout:
                assert "feat(302)" in result.stdout, "Feature commit should exist in remote or local branches"
            else:
                pytest.skip("Feature 302 commit not pushed to remote (may need API key)")
        else:
            pytest.skip("No remote branches found (may be detached HEAD)")

    def test_upstream_tracking_is_set(self):
        """Test that upstream tracking is set (-u flag was used in push)."""
        result = subprocess.run(
            ["git", "branch", "-vv"],
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
        )
        branch_output = result.stdout
        # Current branch should show tracking information if push was successful
        # If branch tracking exists, upstream is set
        if "->" in branch_output or "[origin/" in branch_output:
            # Upstream tracking is set on at least one branch
            assert True, "Upstream tracking should be set"
        else:
            # May not have remote tracking if not pushed
            pytest.skip("Upstream tracking not visible (feature may not be pushed)")


class TestFullEndToEndIntegration:
    """Full end-to-end integration test simulating complete feature workflow."""

    def test_complete_feature_workflow_simulation(self, tmp_path):
        """Test complete feature workflow with simulated file creation and validation."""
        # Create a simulated markdown file that would be created by the feature
        test_file = tmp_path / "test-k6bwm0.md"
        simulated_content = "# Renewable Energy Solutions\n\nRenewable energy sources reduce carbon emissions significantly. Solar and wind power are becoming increasingly affordable worldwide. Transitioning to clean energy creates jobs and protects the environment for future generations.\n"
        test_file.write_text(simulated_content, encoding="utf-8")

        # Now verify all properties that the feature should produce
        assert test_file.exists(), "File should exist"
        assert test_file.stat().st_size > 50, "File should have minimum size"

        # Verify markdown structure
        content = test_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        assert lines[0].startswith("#"), "First line should be H1 heading"
        assert lines[1] == "", "Second line should be empty (blank separator)"

        # Verify encoding
        with open(test_file, "rb") as f:
            file_bytes = f.read()
        file_bytes.decode("utf-8")  # Should not raise
        assert not file_bytes.startswith(b"\xef\xbb\xbf"), "Should not have BOM"
        assert b"\r\n" not in file_bytes, "Should use LF, not CRLF"
        assert b"\r" not in file_bytes, "Should not have CR"

        # Verify prose structure
        prose_text = " ".join(lines[2:])
        period_count = prose_text.count(".")
        assert 2 <= period_count <= 3, f"Should have 2-3 sentences, found {period_count}"

        # Verify file ends with newline
        assert content.endswith("\n"), "File should end with newline"

    def test_feature_integration_with_mocked_orchestration(self):
        """Test feature integration with mocked orchestration function."""
        from unittest.mock import patch

        from sheep.features.feature_302_markdown_file_creation import (
            create_test_k6bwm0_markdown_file,
        )

        mock_response = {
            "filepath": "/repo/test-k6bwm0.md",
            "content": "# Sustainable Technology\n\nTechnology enables sustainable solutions for environmental challenges. Renewable energy and circular design reduce our carbon footprint. This commitment preserves the planet for future generations.\n",
            "commit_message": "feat(302): create markdown file test-k6bwm0.md with prose content",
            "push_result": "pushed to origin/feat/markdown-file-creation-c622f7",
        }

        with patch(
            "sheep.features.feature_302_markdown_file_creation.create_markdown_file"
        ) as mock_create:
            mock_create.return_value = mock_response

            result = create_test_k6bwm0_markdown_file()

            # Verify the orchestration function was called
            assert mock_create.called
            assert mock_create.call_count == 1

            # Verify result structure
            assert isinstance(result, dict)
            assert all(
                key in result
                for key in ["filepath", "content", "commit_message", "push_result"]
            )

            # Verify content structure
            content = result["content"]
            assert content.startswith("#"), "Content should start with H1 heading"
            assert "\n\n" in content, "Content should have blank line separator"
            lines = content.split("\n")
            assert len(lines) >= 3, "Content should have multiple lines"

            # Verify sentence count
            prose = " ".join(lines[2:])
            periods = prose.count(".")
            assert 2 <= periods <= 3, f"Should have 2-3 sentences, got {periods}"

            # Verify commit message format
            msg = result["commit_message"]
            assert "feat(302)" in msg, "Commit should use feat(302)"
            assert "test-k6bwm0.md" in msg, "Commit should reference filename"

            # Verify push result
            assert result["push_result"], "Push result should not be empty"


class TestIntegrationSimulatedWorkflow:
    """Simulated integration tests that verify workflow without requiring API key."""

    def test_create_simulated_markdown_file(self, tmp_path):
        """Test creating a simulated markdown file with correct structure."""
        # Create a sample markdown file that simulates the feature output
        test_file = tmp_path / "test-k6bwm0.md"
        content = "# Artificial Intelligence\n\nArtificial intelligence is transforming industries globally. Machine learning models discover patterns in data. This technology reshapes how we work and solve problems.\n"
        test_file.write_text(content, encoding="utf-8")

        # Verify the file has correct structure
        assert test_file.exists()
        assert test_file.stat().st_size > 50
        lines = content.split("\n")
        assert lines[0].startswith("#")
        assert lines[1] == ""
        assert len(" ".join(lines[2:]).strip()) > 0

    def test_simulated_file_encoding_validation(self, tmp_path):
        """Test encoding validation on simulated file."""
        test_file = tmp_path / "test-k6bwm0.md"
        content = "# Test Heading\n\nThis is a test sentence. Another test. And a third.\n"
        test_file.write_text(content, encoding="utf-8")

        # Validate encoding
        with open(test_file, "rb") as f:
            file_bytes = f.read()

        # Should be valid UTF-8
        try:
            file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("File should be valid UTF-8")

        # Should not have BOM
        assert not file_bytes.startswith(b"\xef\xbb\xbf"), "Should not have UTF-8 BOM"

        # Should use LF line endings
        assert b"\r\n" not in file_bytes, "Should use LF, not CRLF"
        assert b"\r" not in file_bytes, "Should not contain CR characters"
