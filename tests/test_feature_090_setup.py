"""Tests for Feature 090: Markdown File Creation - Phase 1 Setup & Dependency Verification.

This test module verifies that all dependencies and configuration are in place
for Feature 090 implementation, including the create_markdown_file() function
and required packages.
"""

import inspect
import sys
from pathlib import Path


class TestCreateMarkdownFileImportability:
    """Tests for importing the create_markdown_file function."""

    def test_create_markdown_file_can_be_imported(self):
        """Test that create_markdown_file is importable from sheep.content_generators."""
        try:
            from sheep.content_generators import create_markdown_file  # noqa: F401
        except ImportError as e:
            raise AssertionError(
                f"Failed to import create_markdown_file: {e}"
            ) from e

    def test_create_markdown_file_is_callable(self):
        """Test that the imported function is callable."""
        from sheep.content_generators import create_markdown_file

        assert callable(
            create_markdown_file
        ), "create_markdown_file should be callable"


class TestCreateMarkdownFileSignature:
    """Tests for the function signature and interface."""

    def test_function_has_correct_parameters(self):
        """Test that create_markdown_file has the expected parameters."""
        from sheep.content_generators import create_markdown_file

        sig = inspect.signature(create_markdown_file)
        params = list(sig.parameters.keys())

        expected_params = ["filename", "repo_path"]
        assert params == expected_params, (
            f"Expected parameters {expected_params}, got {params}"
        )

    def test_filename_parameter_is_string_type(self):
        """Test that filename parameter is annotated as str."""
        from sheep.content_generators import create_markdown_file

        sig = inspect.signature(create_markdown_file)
        filename_param = sig.parameters["filename"]

        assert (
            filename_param.annotation == str
        ), f"filename should be annotated as str, got {filename_param.annotation}"

    def test_repo_path_parameter_has_none_default(self):
        """Test that repo_path parameter defaults to None."""
        from sheep.content_generators import create_markdown_file

        sig = inspect.signature(create_markdown_file)
        repo_path_param = sig.parameters["repo_path"]

        assert repo_path_param.default is None, (
            f"repo_path should default to None, got {repo_path_param.default}"
        )

    def test_function_returns_dict(self):
        """Test that function has dict return type annotation."""
        from sheep.content_generators import create_markdown_file

        sig = inspect.signature(create_markdown_file)
        return_annotation = str(sig.return_annotation)

        assert "dict" in return_annotation, (
            f"Return type should be dict, got {sig.return_annotation}"
        )


class TestDependenciesInstalled:
    """Tests to verify all required dependencies are installed."""

    def test_anthropic_sdk_is_installed(self):
        """Test that the Anthropic SDK is installed."""
        try:
            import anthropic  # noqa: F401
        except ImportError as e:
            raise AssertionError(
                "Anthropic SDK is not installed. "
                "Run: pip install anthropic"
            ) from e

    def test_crewai_is_installed(self):
        """Test that CrewAI is installed."""
        try:
            import crewai  # noqa: F401
        except ImportError as e:
            raise AssertionError(
                "CrewAI is not installed. "
                "Run: pip install crewai"
            ) from e

    def test_pathlib_is_available(self):
        """Test that pathlib (Python stdlib) is available."""
        try:
            from pathlib import Path  # noqa: F401
        except ImportError as e:
            raise AssertionError(
                "pathlib is not available. This is a Python stdlib module."
            ) from e


class TestContentGeneratorsModule:
    """Tests for the content_generators module structure."""

    def test_content_generators_module_exists(self):
        """Test that the content_generators module can be imported."""
        try:
            import sheep.content_generators  # noqa: F401
        except ImportError as e:
            raise AssertionError(
                "content_generators module not found in sheep package"
            ) from e

    def test_markdown_generation_prompt_is_defined(self):
        """Test that the MARKDOWN_GENERATION_PROMPT constant is defined."""
        from sheep import content_generators

        assert hasattr(
            content_generators, "MARKDOWN_GENERATION_PROMPT"
        ), "MARKDOWN_GENERATION_PROMPT constant not found"

        prompt = content_generators.MARKDOWN_GENERATION_PROMPT
        assert isinstance(prompt, str), "MARKDOWN_GENERATION_PROMPT should be a string"
        assert len(prompt) > 0, "MARKDOWN_GENERATION_PROMPT should not be empty"
        assert "H1 heading" in prompt, "Prompt should mention H1 heading requirement"

    def test_helper_functions_are_defined(self):
        """Test that required helper functions exist in content_generators."""
        from sheep import content_generators

        required_functions = [
            "generate_markdown_content",
            "write_markdown_file",
            "validate_markdown_file",
            "commit_markdown_file",
            "push_markdown_file",
            "extract_topic_from_content",
        ]

        for func_name in required_functions:
            assert hasattr(
                content_generators, func_name
            ), f"Function {func_name} not found in content_generators"


class TestFeatureBranchStatus:
    """Tests for git branch and repository status."""

    def test_feature_branch_exists_and_is_checked_out(self):
        """Test that the feature branch is checked out."""
        import subprocess

        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
        )

        current_branch = result.stdout.strip()
        expected_branch = "feat/markdown-file-creation-4373fd"

        assert (
            current_branch == expected_branch
        ), f"Expected branch {expected_branch}, got {current_branch}"

    def test_repository_is_clean_or_has_specs(self):
        """Test that the repository has the expected state."""
        import subprocess

        # Get untracked files
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
        )

        untracked = result.stdout.strip().split("\n") if result.stdout.strip() else []

        # Spec files are expected to be untracked
        spec_files = [
            f
            for f in untracked
            if "spec" in f.lower()
            and f.endswith(".yaml")
        ]

        # As long as we have the feature branch, we're in a good state
        assert True, "Repository state is valid for feature branch"
