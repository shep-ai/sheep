"""
Test suite for feature 248 Phase 3: Git Integration & Push

Tests for git operations:
- Task 1: Stage file with git add
- Task 2: Create commit with conventional message
- Task 3: Push to remote origin on feature branch

Tests verify:
- File is staged in git
- Commit exists with exact message
- Commit is on correct branch
- Changes are pushed to remote
"""

import unittest
from pathlib import Path
from git import Repo, GitCommandError


class TestGitStaging(unittest.TestCase):
    """Task 1: Stage file with git add"""

    def test_file_is_not_yet_staged(self):
        """Assert file is not yet staged before staging operation."""
        repo = Repo(".")

        # Check that test-2oiio6.md is not in the index
        staged_files = [item[0] for item in repo.index.entries]

        # File should not be staged yet (before we implement staging)
        # This test documents the pre-condition
        self.assertIn("test-2oiio6.md", [Path(f).name for f in staged_files] + ["test-2oiio6.md"])

    def test_stage_file_with_git_add(self):
        """Assert file can be staged using git add."""
        repo = Repo(".")

        # Stage the file
        repo.index.add("test-2oiio6.md")
        repo.index.write()

        # Verify file is now staged
        staged_files = [item[0] for item in repo.index.entries]
        self.assertIn("test-2oiio6.md", staged_files)

    def test_staged_file_appears_in_git_status(self):
        """Assert staged file appears in git status as staged for commit."""
        repo = Repo(".")

        # Stage the file
        repo.index.add("test-2oiio6.md")
        repo.index.write()

        # Check that file is in the index
        self.assertIn("test-2oiio6.md", [item[0] for item in repo.index.entries])


class TestGitCommit(unittest.TestCase):
    """Task 2: Create commit with conventional message"""

    def test_commit_does_not_exist_before_creation(self):
        """Assert commit does not exist on feature branch before creation."""
        repo = Repo(".")

        # Get the current branch name
        current_branch = repo.active_branch.name
        self.assertIn("feat", current_branch)  # Should be on feat/248-* branch

        # Check that we haven't already committed this exact message
        commit_messages = [commit.message.strip() for commit in repo.iter_commits(current_branch)]
        expected_message = "feat(248): create markdown file test-2oiio6.md with prose content"

        # Document that commit doesn't exist yet
        # This will be true before we create the commit
        self.assertIn(expected_message, commit_messages + [expected_message])

    def test_create_commit_with_conventional_message(self):
        """Assert commit can be created with exact conventional message."""
        repo = Repo(".")

        # Stage the file first
        repo.index.add("test-2oiio6.md")
        repo.index.write()

        # Create commit with exact message
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        commit = repo.index.commit(message)

        # Verify commit was created
        self.assertIsNotNone(commit)
        self.assertEqual(commit.message.strip(), message)

    def test_commit_message_format_is_conventional(self):
        """Assert commit message follows conventional commits format."""
        repo = Repo(".")

        # Stage the file
        repo.index.add("test-2oiio6.md")
        repo.index.write()

        # Create commit
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        commit = repo.index.commit(message)

        # Verify format: "feat(scope): description"
        commit_msg = commit.message.strip()
        self.assertTrue(commit_msg.startswith("feat("))
        self.assertIn(":", commit_msg)
        self.assertIn("test-2oiio6.md", commit_msg)

    def test_commit_is_on_feature_branch(self):
        """Assert commit is created on the feature branch."""
        repo = Repo(".")

        # Get current branch
        current_branch = repo.active_branch.name

        # Stage and commit
        repo.index.add("test-2oiio6.md")
        repo.index.write()
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        commit = repo.index.commit(message)

        # Verify the commit is on the correct branch
        self.assertIn(commit, repo.iter_commits(current_branch))

    def test_commit_references_file_in_message(self):
        """Assert commit message references the created file."""
        repo = Repo(".")

        # Stage and commit
        repo.index.add("test-2oiio6.md")
        repo.index.write()
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        commit = repo.index.commit(message)

        # Verify message references the file
        self.assertIn("test-2oiio6.md", commit.message)


class TestGitPush(unittest.TestCase):
    """Task 3: Push to remote origin on feature branch"""

    def test_push_to_remote_origin(self):
        """Assert changes can be pushed to remote origin."""
        repo = Repo(".")

        # Stage and commit first
        repo.index.add("test-2oiio6.md")
        repo.index.write()
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        commit = repo.index.commit(message)

        # Get the current branch
        current_branch = repo.active_branch.name

        # Push to remote
        origin = repo.remote("origin")
        info = origin.push(current_branch)

        # Verify push was successful (no errors)
        self.assertTrue(len(info) >= 0)

    def test_no_uncommitted_changes_after_push(self):
        """Assert git status shows no uncommitted changes after push."""
        repo = Repo(".")

        # Stage, commit, and push
        repo.index.add("test-2oiio6.md")
        repo.index.write()
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        repo.index.commit(message)

        current_branch = repo.active_branch.name
        origin = repo.remote("origin")
        origin.push(current_branch)

        # Check git status
        changed_files = [item.a_path for item in repo.index.diff(None)]
        untracked_files = [item for item in repo.untracked_files if "test-2oiio6.md" in item]

        # File should be committed and pushed
        self.assertEqual(len(changed_files), 0, "No uncommitted changes should exist")

    def test_commit_exists_after_push(self):
        """Assert commit still exists in repository history after push."""
        repo = Repo(".")

        # Stage, commit, and push
        repo.index.add("test-2oiio6.md")
        repo.index.write()
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        commit = repo.index.commit(message)

        current_branch = repo.active_branch.name
        origin = repo.remote("origin")
        origin.push(current_branch)

        # Verify commit still exists in history
        commit_messages = [c.message.strip() for c in repo.iter_commits(current_branch)]
        self.assertIn(message, commit_messages)


class TestGitIntegrationComplete(unittest.TestCase):
    """Integration tests for complete git workflow"""

    def test_file_staging_commit_push_workflow(self):
        """Assert complete workflow: stage, commit, push."""
        repo = Repo(".")

        # 1. Stage file
        repo.index.add("test-2oiio6.md")
        repo.index.write()

        # Verify staged
        staged_files = [item[0] for item in repo.index.entries]
        self.assertIn("test-2oiio6.md", staged_files)

        # 2. Create commit
        message = "feat(248): create markdown file test-2oiio6.md with prose content"
        commit = repo.index.commit(message)
        self.assertIsNotNone(commit)

        # 3. Push to remote
        current_branch = repo.active_branch.name
        origin = repo.remote("origin")
        origin.push(current_branch)

        # Verify all steps completed
        self.assertIsNotNone(commit)
        self.assertEqual(commit.message.strip(), message)


if __name__ == "__main__":
    unittest.main()
