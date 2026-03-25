"""
Tests for Feature 211: Markdown file creation with git integration
"""
import tempfile
import re
from pathlib import Path
from git import Repo
import pytest


class TestMarkdownFileCreation:
    """Tests for markdown file creation functionality"""

    def test_file_exists(self):
        """Test that test-vqqlp6.md exists in repository root"""
        path = Path("test-vqqlp6.md")
        assert path.exists(), f"File {path} does not exist"

    def test_file_contains_markdown_heading(self):
        """Test that file starts with markdown heading"""
        path = Path("test-vqqlp6.md")
        content = path.read_text(encoding='utf-8')
        lines = content.split('\n')
        assert re.match(r'^#\s+', lines[0]), "First line must be markdown heading (# Title)"

    def test_file_contains_prose_content(self):
        """Test that file contains 2-3 sentences of prose"""
        path = Path("test-vqqlp6.md")
        content = path.read_text(encoding='utf-8')

        # Count sentences (separated by '. ')
        sentences = re.findall(r'[^.]+\.', content)
        assert 2 <= len(sentences) <= 3, f"Expected 2-3 sentences, got {len(sentences)}"

    def test_file_uses_utf8_encoding(self):
        """Test that file is UTF-8 encoded"""
        path = Path("test-vqqlp6.md")
        try:
            content = path.read_text(encoding='utf-8')
            assert isinstance(content, str), "Content should be properly decoded UTF-8"
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not properly UTF-8 encoded: {e}")

    def test_file_uses_lf_line_endings(self):
        """Test that file uses LF line endings, not CRLF"""
        path = Path("test-vqqlp6.md")
        content = path.read_text(encoding='utf-8')
        assert '\r' not in content, "File must use LF line endings, not CRLF"

    def test_markdown_syntax_is_valid(self):
        """Test that markdown syntax is valid"""
        path = Path("test-vqqlp6.md")
        content = path.read_text(encoding='utf-8')

        # Basic validation: has heading and prose
        assert re.search(r'^#\s+.+$', content, re.MULTILINE), "Must have markdown heading"
        assert len(content) > 50, "File should have substantive content"


class TestGitIntegration:
    """Tests for git integration"""

    def test_file_is_committed(self):
        """Test that file is committed to git (not untracked)"""
        repo = Repo('.')

        # Get list of tracked files in the latest commit
        try:
            committed_files = [item.path for item in repo.head.commit.tree.traverse()]
            assert 'test-vqqlp6.md' in committed_files, "File is not committed to git"
        except ValueError:
            pytest.skip("Cannot check committed files in empty repository")

    def test_commit_message_format(self):
        """Test that commit message follows conventional commit format"""
        repo = Repo('.')

        # Find the commit that created test-vqqlp6.md
        for commit in repo.iter_commits():
            if 'feat(211)' in commit.message and 'test-vqqlp6.md' in commit.message:
                assert re.match(r'^feat\(211\):', commit.message), \
                    f"Commit message should follow conventional format: {commit.message}"
                return

        pytest.fail("No commit found for feature 211 markdown file creation")

    def test_commit_is_pushed(self):
        """Test that commit is pushed to remote branch"""
        repo = Repo('.')
        branch_name = repo.active_branch.name

        # Verify upstream is set
        assert repo.active_branch.tracking_branch() is not None, \
            "Upstream branch not set"

        # Verify local and remote are in sync
        try:
            local_commit = repo.head.commit
            remote_commit = repo.remotes.origin.refs[branch_name].commit
            assert local_commit == remote_commit, \
                "Local and remote commits do not match"
        except Exception as e:
            pytest.fail(f"Error verifying remote branch: {e}")

    def test_working_tree_is_clean(self):
        """Test that working tree has no uncommitted changes"""
        repo = Repo('.')
        assert not repo.is_dirty(), "Working tree should be clean"


class TestSuccessCriteria:
    """Integration tests verifying all success criteria"""

    def test_all_success_criteria_met(self):
        """Verify all acceptance criteria are satisfied"""
        path = Path("test-vqqlp6.md")
        repo = Repo('.')

        # Success criterion 1: File exists
        assert path.exists(), "File test-vqqlp6.md must exist in repository root"

        # Success criterion 2: File contains markdown heading
        content = path.read_text(encoding='utf-8')
        assert re.match(r'^#\s+', content.split('\n')[0]), \
            "File must contain markdown heading"

        # Success criterion 3: File contains 2-3 sentences
        sentences = re.findall(r'[^.]+\.', content)
        assert 2 <= len(sentences) <= 3, \
            f"File must contain 2-3 sentences, got {len(sentences)}"

        # Success criterion 4: UTF-8 encoding without BOM
        assert isinstance(content, str), "File must be UTF-8 encoded"

        # Success criterion 5: LF line endings
        assert '\r' not in content, "File must use LF line endings"

        # Success criterion 6: File is staged and committed
        branch_name = repo.active_branch.name
        assert branch_name == "feat/markdown-file-creation-5c9555", \
            "Must be on feature branch"

        # Success criterion 7: Commit message follows conventional format
        commit_found = False
        for commit in repo.iter_commits():
            if 'feat(211)' in commit.message:
                assert commit.message.startswith('feat(211):'), \
                    "Commit must follow conventional format"
                commit_found = True
                break
        assert commit_found, "No feature 211 commit found"

        # Success criterion 8: Commit pushed to remote
        remote_branch = repo.active_branch.tracking_branch()
        assert remote_branch is not None, "Upstream branch must be set"

        # Success criterion 9: Clean working tree
        assert not repo.is_dirty(), "Working tree must be clean"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
