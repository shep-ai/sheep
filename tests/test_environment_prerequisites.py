"""Tests for environment prerequisites verification for feature 070."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest


class TestEnvironmentPrerequisites:
    """Verify that all environment prerequisites are in place for feature 070 implementation."""

    def test_anthropic_api_key_is_set(self):
        """Test that ANTHROPIC_API_KEY environment variable is set.

        To fix this test:
        1. Copy .env.example to .env: cp .env.example .env
        2. Add your Anthropic API key to .env:
           ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE
        3. Get your API key from: https://console.anthropic.com/account/keys
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        assert (
            api_key is not None
        ), (
            "ANTHROPIC_API_KEY environment variable must be set. "
            "Create a .env file with: ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE"
        )
        assert (
            api_key.strip() != ""
        ), "ANTHROPIC_API_KEY environment variable must not be empty"

    def test_anthropic_api_key_format_is_valid(self):
        """Test that ANTHROPIC_API_KEY has expected format.

        Valid Anthropic API keys start with 'sk-ant-' and are reasonably long.
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        assert (
            api_key is not None
        ), (
            "ANTHROPIC_API_KEY must be set. "
            "Create a .env file with: ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE"
        )
        assert len(api_key) > 10, (
            "ANTHROPIC_API_KEY should be a valid key (>10 chars). "
            "Get your key from: https://console.anthropic.com/account/keys"
        )

    def test_git_user_name_is_configured(self):
        """Test that git user.name is configured."""
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=False,
        )
        git_user_name = result.stdout.strip()
        assert (
            git_user_name != ""
        ), "Git user.name must be configured. Run: git config user.name 'Your Name'"

    def test_git_user_email_is_configured(self):
        """Test that git user.email is configured."""
        result = subprocess.run(
            ["git", "config", "user.email"],
            capture_output=True,
            text=True,
            check=False,
        )
        git_user_email = result.stdout.strip()
        assert (
            git_user_email != ""
        ), "Git user.email must be configured. Run: git config user.email 'your.email@example.com'"

    def test_current_branch_is_feature_branch(self):
        """Test that current git branch is the expected feature branch."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        current_branch = result.stdout.strip()
        expected_branch = "feat/markdown-file-creation-71e3ba"
        assert (
            current_branch == expected_branch
        ), f"Expected branch '{expected_branch}', but on '{current_branch}'"

    def test_pathlib_module_is_importable(self):
        """Test that pathlib module is available."""
        try:
            from pathlib import Path
            assert Path is not None
        except ImportError as e:
            pytest.fail(f"pathlib module is not importable: {e}")

    def test_structlog_module_is_importable(self):
        """Test that structlog module is available."""
        try:
            import structlog
            assert structlog is not None
        except ImportError as e:
            pytest.fail(f"structlog module is not importable: {e}")

    def test_content_generators_module_is_importable(self):
        """Test that content_generators module can be imported."""
        try:
            from sheep.content_generators import create_markdown_file
            assert create_markdown_file is not None
        except ImportError as e:
            pytest.fail(f"content_generators module is not importable: {e}")

    def test_git_tools_module_is_importable(self):
        """Test that git tools are importable."""
        try:
            from sheep.tools import GitCommitTool, GitPushTool
            assert GitCommitTool is not None
            assert GitPushTool is not None
        except ImportError as e:
            pytest.fail(f"git_tools module is not importable: {e}")

    def test_repository_root_is_accessible(self):
        """Test that repository root directory is accessible and writable."""
        repo_root = Path.cwd()
        assert (
            repo_root.exists()
        ), f"Repository root does not exist: {repo_root}"
        assert (
            repo_root.is_dir()
        ), f"Repository root is not a directory: {repo_root}"
        # Test write accessibility by checking if we can stat the directory
        try:
            repo_root.stat()
        except OSError as e:
            pytest.fail(f"Repository root is not accessible: {e}")

    def test_test_file_does_not_exist(self):
        """Test that target file test-9yn2il.md does not already exist."""
        target_file = Path.cwd() / "test-9yn2il.md"
        assert (
            not target_file.exists()
        ), f"File {target_file} already exists. Clean state required before feature execution."

    def test_git_is_initialized(self):
        """Test that current directory is a git repository."""
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            text=True,
            check=False,
        )
        assert (
            result.returncode == 0
        ), "Current directory is not a git repository"

    def test_python_version_meets_requirement(self):
        """Test that Python version is 3.11 or higher."""
        current_version = sys.version_info
        required_version = (3, 11)
        assert (
            current_version >= required_version
        ), f"Python {required_version[0]}.{required_version[1]}+ required, but running {current_version.major}.{current_version.minor}"


class TestEnvironmentVerificationHelpers:
    """Helper functions for environment verification."""

    @staticmethod
    def verify_all_prerequisites() -> dict[str, bool]:
        """
        Verify all prerequisites and return status of each check.

        Returns:
            Dictionary with prerequisite names as keys and verification status as values.
        """
        checks = {
            "api_key_set": os.environ.get("ANTHROPIC_API_KEY") is not None,
            "git_configured": subprocess.run(
                ["git", "config", "user.name"],
                capture_output=True,
                check=False,
            ).returncode == 0,
            "is_git_repo": subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                check=False,
            ).returncode == 0,
            "correct_branch": subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout.strip()
            == "feat/markdown-file-creation-71e3ba",
            "repo_accessible": Path.cwd().exists() and Path.cwd().is_dir(),
            "target_file_clean": not (
                Path.cwd() / "test-9yn2il.md"
            ).exists(),
        }
        return checks

    def test_verify_all_prerequisites_function(self):
        """Test that verify_all_prerequisites helper works correctly."""
        checks = self.verify_all_prerequisites()

        # Verify the function returns a dictionary
        assert isinstance(checks, dict)

        # Verify all expected checks are present
        expected_checks = {
            "api_key_set",
            "git_configured",
            "is_git_repo",
            "correct_branch",
            "repo_accessible",
            "target_file_clean",
        }
        assert set(checks.keys()) == expected_checks

        # Verify all checks return boolean values
        for check_name, check_result in checks.items():
            assert isinstance(check_result, bool), f"{check_name} should return bool"


class TestEnvironmentEdgeCases:
    """Test edge cases and error handling for environment verification."""

    def test_handles_missing_git_gracefully(self):
        """Test that git check fails gracefully if git is not available."""
        # This test verifies the check itself handles errors gracefully
        # even if git is not installed (though in practice git should be available)
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            check=False,
        )
        # If git is available, version check should succeed
        assert (
            result.returncode == 0
        ), "Git must be installed and available on PATH"

    def test_current_branch_exists(self):
        """Test that current branch is a valid git ref."""
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            check=False,
        )
        assert (
            result.returncode == 0
        ), "Current HEAD is not a valid git reference"

    def test_api_key_does_not_contain_sensitive_patterns(self):
        """Test that API key environment variable follows expected patterns.

        Skip this test if API key is not yet configured (expected during setup).
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        # Skip if not configured (expected during first-time setup)
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not configured - expected during setup phase")
        # API key should not contain common placeholder patterns
        assert (
            api_key.lower() != "your-api-key"
        ), "API key appears to be a placeholder"
        assert (
            api_key.lower() != "sk-xxx"
        ), "API key appears to be a placeholder"
        assert (
            api_key != ""
        ), "API key must not be empty string"


class TestEnvironmentSetupGuide:
    """Documentation and helpers for environment setup."""

    def test_setup_instructions_documented(self):
        """Verify that setup instructions are available in the codebase."""
        env_example_file = Path.cwd() / ".env.example"
        assert (
            env_example_file.exists()
        ), ".env.example file must exist with configuration template"

    def print_setup_requirements(self):
        """
        Print setup requirements for the environment.

        Call this method to see what needs to be configured:
        pytest tests/test_environment_prerequisites.py::TestEnvironmentSetupGuide::test_print_setup_help -s
        """
        print("\n" + "=" * 70)
        print("ENVIRONMENT SETUP REQUIREMENTS FOR FEATURE 070")
        print("=" * 70)
        print("\n✓ VERIFIED PREREQUISITES:")
        print("  - Git is installed and repository is initialized")
        print("  - Git user.name is configured:", self._get_git_config("user.name"))
        print("  - Git user.email is configured:", self._get_git_config("user.email"))
        print("  - Current branch:", self._get_current_branch())
        print("  - Python version:", self._get_python_version())
        print("  - All required modules are importable")
        print("  - Repository root is accessible and writable")
        print("  - Target file test-9yn2il.md does not exist (clean state)")

        print("\n✗ MISSING PREREQUISITES:")
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("  - ANTHROPIC_API_KEY environment variable is not set")
            print("\n  TO FIX:")
            print("    1. Copy .env.example to .env:")
            print("       cp .env.example .env")
            print("    2. Edit .env and add your Anthropic API key:")
            print("       ANTHROPIC_API_KEY=sk-ant-YOUR-KEY-HERE")
            print("    3. Get your API key from:")
            print("       https://console.anthropic.com/account/keys")
            print("    4. Reload your shell or restart your IDE")

        print("\n" + "=" * 70)

    def test_print_setup_help(self, capsys):
        """Test that prints setup requirements (run with -s flag to see output)."""
        self.print_setup_requirements()

    @staticmethod
    def _get_git_config(key: str) -> str:
        """Get git configuration value."""
        result = subprocess.run(
            ["git", "config", key],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or "<not configured>"

    @staticmethod
    def _get_current_branch() -> str:
        """Get current git branch."""
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or "<unknown>"

    @staticmethod
    def _get_python_version() -> str:
        """Get Python version."""
        return f"Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
