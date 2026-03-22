"""Tests for Phase 1: Script Setup & Content Definition for feature 157."""

from pathlib import Path


class TestPhase1ScriptSetup:
    """Tests for Phase 1: Script Setup & Content Definition."""

    def test_script_file_exists(self):
        """Test that create_test_19idn1.py file exists in repository root."""
        script_path = Path("create_test_19idn1.py")
        assert script_path.exists(), "create_test_19idn1.py should exist in repository root"

    def test_script_can_be_imported(self):
        """Test that the script can be imported without errors."""
        import create_test_19idn1

        assert create_test_19idn1 is not None

    def test_main_function_exists(self):
        """Test that main() function exists in the script."""
        import create_test_19idn1

        assert hasattr(create_test_19idn1, "main"), "Script should have main() function"
        assert callable(create_test_19idn1.main), "main should be callable"

    def test_prose_content_is_defined(self):
        """Test that prose content is defined as module constants."""
        import create_test_19idn1

        # Check HEADING constant exists and is a string
        assert hasattr(
            create_test_19idn1, "HEADING"
        ), "Script should have HEADING constant"
        assert isinstance(create_test_19idn1.HEADING, str), "HEADING should be a string"
        assert create_test_19idn1.HEADING.startswith("# "), "HEADING should start with '# '"

        # Check PROSE constant exists and is a string
        assert hasattr(
            create_test_19idn1, "PROSE"
        ), "Script should have PROSE constant"
        assert isinstance(create_test_19idn1.PROSE, str), "PROSE should be a string"
        assert len(create_test_19idn1.PROSE) > 0, "PROSE should not be empty"

    def test_heading_contains_title(self):
        """Test that HEADING constant contains a meaningful title."""
        import create_test_19idn1

        heading = create_test_19idn1.HEADING
        # Remove the '# ' prefix
        title = heading[2:].strip()
        assert len(title) > 0, "Title should not be empty"
        assert len(title) < 200, "Title should be reasonable length"

    def test_prose_contains_multiple_sentences(self):
        """Test that PROSE contains multiple sentences (has period characters)."""
        import create_test_19idn1

        prose = create_test_19idn1.PROSE
        sentence_count = prose.count(".")
        assert (
            sentence_count >= 2
        ), "PROSE should contain at least 2 sentences (2-3 periods)"

    def test_filename_constant_is_correct(self):
        """Test that FILENAME constant is set correctly."""
        import create_test_19idn1

        assert hasattr(
            create_test_19idn1, "FILENAME"
        ), "Script should have FILENAME constant"
        assert (
            create_test_19idn1.FILENAME == "test-19idn1.md"
        ), "FILENAME should be 'test-19idn1.md'"

    def test_commit_message_constant_is_correct(self):
        """Test that COMMIT_MESSAGE constant follows conventional commits format."""
        import create_test_19idn1

        assert hasattr(
            create_test_19idn1, "COMMIT_MESSAGE"
        ), "Script should have COMMIT_MESSAGE constant"
        msg = create_test_19idn1.COMMIT_MESSAGE
        # Check conventional commits format: type(scope): subject
        assert msg.startswith("feat(157):"), "Message should start with 'feat(157):'"
        assert "test-19idn1.md" in msg, "Message should mention the filename"

    def test_module_has_docstring(self):
        """Test that script has a module-level docstring."""
        import create_test_19idn1

        assert (
            create_test_19idn1.__doc__ is not None
        ), "Script should have a module docstring"
        assert len(create_test_19idn1.__doc__) > 0, "Module docstring should not be empty"

    def test_phase_1_structure_is_defined(self):
        """Test that phase 1 constants and setup are in place."""
        import create_test_19idn1

        # All required constants should exist
        assert hasattr(create_test_19idn1, "FILENAME")
        assert hasattr(create_test_19idn1, "COMMIT_MESSAGE")
        assert hasattr(create_test_19idn1, "HEADING")
        assert hasattr(create_test_19idn1, "PROSE")

    def test_main_can_be_called(self):
        """Test that main() function can be called and returns an integer."""
        import create_test_19idn1

        result = create_test_19idn1.main()
        assert isinstance(result, int), "main() should return an integer exit code"
        assert result == 0, "main() should return 0 for successful setup phase"
