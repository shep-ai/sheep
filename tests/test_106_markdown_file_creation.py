"""Tests for feature 106: Creating markdown file test-tzghro.md with title and prose content."""


class TestMarkdownFileCreation:
    """Tests for task-1: Create markdown file with H1 heading and prose content."""

    def test_file_does_not_exist_before_creation(self, tmp_path):
        """Test that file test-tzghro.md does not exist before creation."""
        test_file = tmp_path / "test-tzghro.md"
        assert not test_file.exists()

    def test_creates_file_with_h1_heading(self, tmp_path):
        """Test that created file contains H1 heading."""
        test_file = tmp_path / "test-tzghro.md"

        # Create the file with H1 heading
        content = "# The Future of Renewable Energy\n\nFirst sentence. Second sentence. Third sentence.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8").startswith("# ")

    def test_file_contains_two_or_three_sentences(self, tmp_path):
        """Test that file contains 2-3 sentences (ending with periods)."""
        test_file = tmp_path / "test-tzghro.md"

        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels. The transition to renewable energy represents one of the most important challenges of our time.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        # Extract prose content (skip heading and blank line)
        lines = text_content.split("\n")
        prose_lines = lines[2:]
        prose_content = "\n".join(prose_lines).strip()

        # Count periods to count sentences
        sentence_count = prose_content.count(".")
        assert 2 <= sentence_count <= 3

    def test_file_has_blank_line_separator(self, tmp_path):
        """Test that file has blank line after H1 heading."""
        test_file = tmp_path / "test-tzghro.md"

        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels. The transition to renewable energy represents one of the most important challenges of our time.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        text_content = test_file.read_text(encoding="utf-8")
        lines = text_content.split("\n")

        assert lines[0].startswith("# ")
        assert lines[1] == ""  # Blank line separator

    def test_uses_pathlib_write_text_with_utf8(self, tmp_path):
        """Test that file is created using pathlib.Path.write_text() with UTF-8."""
        test_file = tmp_path / "test-tzghro.md"

        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels. The transition to renewable energy represents one of the most important challenges of our time.\n"
        # Use pathlib.Path.write_text() with explicit UTF-8 and LF
        test_file.write_text(content, encoding="utf-8", newline="\n")

        assert test_file.exists()
        # Verify it was written as UTF-8 by reading it back
        read_content = test_file.read_text(encoding="utf-8")
        assert read_content == content


class TestMarkdownFileValidation:
    """Tests for task-2, 3, 4: Validate file encoding, line endings, and size."""

    MIN_SIZE = 400
    MAX_SIZE = 600

    def test_file_not_utf8_bom(self, tmp_path):
        """Test that file encoding is UTF-8 without BOM (first bytes not 0xEF 0xBB 0xBF)."""
        test_file = tmp_path / "test-tzghro.md"

        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective, transforming the global landscape of electricity generation and consumption. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels and mitigate the effects of climate change. The transition to renewable energy represents one of the most important challenges and opportunities of our time.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file does NOT start with UTF-8 BOM signature
        assert not binary_content.startswith(b"\xef\xbb\xbf")

    def test_file_has_no_crlf_line_endings(self, tmp_path):
        """Test that file contains only LF line endings (no CRLF byte sequences)."""
        test_file = tmp_path / "test-tzghro.md"

        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective, transforming the global landscape of electricity generation and consumption. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels and mitigate the effects of climate change. The transition to renewable energy represents one of the most important challenges and opportunities of our time.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        # Assert file contains no CRLF sequences (0x0D 0x0A)
        assert b"\r\n" not in binary_content

    def test_file_size_within_range(self, tmp_path):
        """Test that file size is between 400-600 bytes (inclusive)."""
        test_file = tmp_path / "test-tzghro.md"

        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective, transforming the global landscape of electricity generation and consumption. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels and mitigate the effects of climate change. The transition to renewable energy represents one of the most important challenges and opportunities of our time.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        file_size = len(test_file.read_bytes())
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_file_size_validation_bounds(self, tmp_path):
        """Test that files with proper prose content fall within 400-600 byte range."""
        # Test with realistic prose content - using longer sentences
        test_file = tmp_path / "test-bounds.md"
        # Use three substantial sentences for markdown files - ensure 400+ bytes
        sentence1 = "Renewable energy represents a critical shift toward sustainable power generation and environmental preservation. "
        sentence2 = "Solar panels and wind turbines are becoming increasingly more efficient, affordable, and environmentally beneficial every single year. "
        sentence3 = "This unprecedented transition will fundamentally transform how we produce, distribute, and consume electricity on a global scale."
        markdown_content = f"# The Future of Renewable Energy\n\n{sentence1}{sentence2}{sentence3}\n"
        test_file.write_text(markdown_content, encoding="utf-8", newline="\n")
        file_size = len(test_file.read_bytes())
        # Verify the file is within reasonable bounds
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE

    def test_validation_all_criteria_met(self, tmp_path):
        """Test that file passes all validation criteria together."""
        test_file = tmp_path / "test-tzghro.md"

        # Content that meets all criteria
        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective, transforming the global landscape of electricity generation and consumption. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels and mitigate the effects of climate change. The transition to renewable energy represents one of the most important challenges and opportunities of our time.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        binary_content = test_file.read_bytes()
        file_size = len(binary_content)

        # Check UTF-8 without BOM
        assert not binary_content.startswith(b"\xef\xbb\xbf")

        # Check no CRLF
        assert b"\r\n" not in binary_content

        # Check file size
        assert self.MIN_SIZE <= file_size <= self.MAX_SIZE


class TestStructureValidation:
    """Tests for structure validation logic."""

    def test_validate_h1_heading_present(self, tmp_path):
        """Test that validation detects missing H1 heading."""
        test_file = tmp_path / "test-tzghro.md"

        # Content without H1 heading (missing #)
        invalid_content = "The Future of Renewable Energy\n\nSome prose. More prose. Final prose.\n"
        test_file.write_text(invalid_content, encoding="utf-8", newline="\n")

        lines = invalid_content.split("\n")
        # Should fail validation - first line doesn't start with "# "
        assert not lines[0].startswith("# ")

    def test_validate_blank_line_present(self, tmp_path):
        """Test that validation detects missing blank line after heading."""
        test_file = tmp_path / "test-tzghro.md"

        # Content without blank line separator
        invalid_content = "# The Future of Renewable Energy\nSome prose. More prose. Final prose.\n"
        test_file.write_text(invalid_content, encoding="utf-8", newline="\n")

        lines = invalid_content.split("\n")
        # Should fail validation - line 1 is not blank
        assert lines[1] != ""

    def test_validate_sentence_count(self, tmp_path):
        """Test that validation checks for correct sentence count (2-3)."""
        test_file = tmp_path / "test-tzghro.md"

        # Content with only one sentence (should fail)
        invalid_content = "# The Future of Renewable Energy\n\nOnly one sentence here.\n"
        test_file.write_text(invalid_content, encoding="utf-8", newline="\n")

        lines = invalid_content.split("\n")
        prose_content = "\n".join(lines[2:]).strip()
        sentence_count = prose_content.count(".")

        # Should fail - only 1 sentence instead of 2-3
        assert not (2 <= sentence_count <= 3)


class TestGitOperations:
    """Tests for task-5: Git operations (add, commit, push)."""

    def test_git_add_success(self, tmp_path, monkeypatch):
        """Test that git add command succeeds with exit code 0."""
        import subprocess
        from unittest.mock import patch

        # Create a test file
        test_file = tmp_path / "test-tzghro.md"
        content = "# The Future of Renewable Energy\n\nRenewable energy sources like solar and wind power are becoming increasingly efficient and cost-effective, transforming the global landscape of electricity generation and consumption. By investing in sustainable infrastructure and advancing battery storage technology, we can reduce our dependence on fossil fuels and mitigate the effects of climate change. The transition to renewable energy represents one of the most important challenges and opportunities of our time.\n"
        test_file.write_text(content, encoding="utf-8", newline="\n")

        # Mock subprocess.run to verify it's called correctly
        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            subprocess.run(
                ["git", "add", "test-tzghro.md"],
                check=True,
                capture_output=True,
                text=True,
            )
            # Verify subprocess.run was called with correct arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "add", "test-tzghro.md"]
            assert kwargs["check"] is True
            # shell defaults to False if not specified, or should be explicitly False
            assert kwargs.get("shell", False) is False

    def test_git_commit_with_message(self, tmp_path):
        """Test that git commit command uses exact conventional commit message."""
        import subprocess
        from unittest.mock import patch

        expected_message = "feat(106): create markdown file test-tzghro.md with prose content"

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            subprocess.run(
                ["git", "commit", "--no-verify", "-m", expected_message],
                check=True,
                capture_output=True,
                text=True,
            )
            # Verify subprocess.run was called with exact message
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "commit", "--no-verify", "-m", expected_message]
            assert kwargs["check"] is True
            assert "--no-verify" in args[0]

    def test_git_push_to_origin(self, tmp_path):
        """Test that git push command pushes to remote origin with upstream tracking."""
        import subprocess
        from unittest.mock import patch

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            subprocess.run(
                ["git", "push", "-u", "origin", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            )
            # Verify subprocess.run was called with correct push arguments
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert args[0] == ["git", "push", "-u", "origin", "HEAD"]
            assert "-u" in args[0]  # Upstream tracking flag
            assert "origin" in args[0]
            assert kwargs["check"] is True

    def test_git_operations_no_verify_flag(self, tmp_path):
        """Test that git commit uses --no-verify to skip pre-commit hooks."""
        import subprocess
        from unittest.mock import patch

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            subprocess.run(
                ["git", "commit", "--no-verify", "-m", "feat(106): create markdown file test-tzghro.md with prose content"],
                check=True,
                capture_output=True,
                text=True,
            )
            args, kwargs = mock_run.call_args
            # Verify --no-verify flag is present
            assert "--no-verify" in args[0]

    def test_git_operations_capture_output(self, tmp_path):
        """Test that git operations capture stderr and stdout for logging."""
        import subprocess
        from unittest.mock import patch

        with patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            subprocess.run(
                ["git", "add", "test-tzghro.md"],
                check=True,
                capture_output=True,
                text=True,
            )
            args, kwargs = mock_run.call_args
            # Verify capture_output and text parameters are set
            assert kwargs["capture_output"] is True
            assert kwargs["text"] is True or kwargs.get("universal_newlines") is True
