"""Tests for feature 245 main orchestration function."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch


class TestFeature245Main:
    """Tests for task-2: Implement main orchestration function."""

    def test_main_function_exists_and_callable(self):
        """Test that main() function exists and is callable."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            assert callable(main)
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_returns_dictionary(self):
        """Test that main() returns a dictionary with expected keys."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                return_value="# Test\n\nTest content.\n",
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    return_value="/path/to/test-nxclc0.md",
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        return_value=True,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            return_value="Commit result",
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                return_value="Push result",
                            ):
                                result = main()

                                assert isinstance(result, dict)
                                assert "content" in result
                                assert "filepath" in result
                                assert "commit_message" in result
                                assert "push_result" in result
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_calls_task_2(self):
        """Test that main() calls task_2_generate_markdown_content."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            mock_task_2 = MagicMock(return_value="# Test\n\nTest content.\n")

            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                mock_task_2,
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    return_value="/path/to/test-nxclc0.md",
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        return_value=True,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            return_value="Commit result",
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                return_value="Push result",
                            ):
                                main()

                                # Verify task_2 was called
                                mock_task_2.assert_called_once()
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_calls_task_3(self):
        """Test that main() calls task_3_write_markdown_file_to_disk."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            mock_task_3 = MagicMock(return_value="/path/to/test-nxclc0.md")

            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                return_value="# Test\n\nTest content.\n",
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    mock_task_3,
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        return_value=True,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            return_value="Commit result",
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                return_value="Push result",
                            ):
                                main()

                                # Verify task_3 was called with the content from task_2
                                mock_task_3.assert_called_once()
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_calls_task_4(self):
        """Test that main() calls task_4_commit_markdown_file."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            mock_task_4 = MagicMock(return_value="Commit result")

            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                return_value="# Test\n\nTest content.\n",
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    return_value="/path/to/test-nxclc0.md",
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        return_value=True,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            mock_task_4,
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                return_value="Push result",
                            ):
                                main()

                                # Verify task_4 was called
                                mock_task_4.assert_called_once()
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_calls_task_5(self):
        """Test that main() calls task_5_push_markdown_file."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            mock_task_5 = MagicMock(return_value="Push result")

            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                return_value="# Test\n\nTest content.\n",
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    return_value="/path/to/test-nxclc0.md",
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        return_value=True,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            return_value="Commit result",
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                mock_task_5,
                            ):
                                main()

                                # Verify task_5 was called
                                mock_task_5.assert_called_once()
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_tasks_execute_in_order(self):
        """Test that main() calls tasks in the correct sequence."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            call_order = []

            def mock_task_2():
                call_order.append("task_2")
                return "# Test\n\nTest content.\n"

            def mock_task_3(content):
                call_order.append("task_3")
                return "/path/to/test-nxclc0.md"

            def mock_validate(filepath):
                call_order.append("validate")
                return True

            def mock_task_4(filepath, content):
                call_order.append("task_4")
                return "Commit result"

            def mock_task_5():
                call_order.append("task_5")
                return "Push result"

            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                mock_task_2,
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    mock_task_3,
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        mock_validate,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            mock_task_4,
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                mock_task_5,
                            ):
                                main()

                                # Verify order
                                expected_order = [
                                    "task_2",
                                    "task_3",
                                    "validate",
                                    "task_4",
                                    "task_5",
                                ]
                                assert call_order == expected_order
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))

    def test_main_commit_message_format(self):
        """Test that main() uses correct commit message format."""
        src_path = Path("src").resolve()
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        try:
            from sheep.feature_245_markdown_file_creation import main

            with patch(
                "sheep.feature_245_markdown_file_creation.task_2_generate_markdown_content",
                return_value="# Test\n\nTest content.\n",
            ):
                with patch(
                    "sheep.feature_245_markdown_file_creation.task_3_write_markdown_file_to_disk",
                    return_value="/path/to/test-nxclc0.md",
                ):
                    with patch(
                        "sheep.feature_245_markdown_file_creation.validate_markdown_file",
                        return_value=True,
                    ):
                        with patch(
                            "sheep.feature_245_markdown_file_creation.task_4_commit_markdown_file",
                            return_value="Commit result",
                        ):
                            with patch(
                                "sheep.feature_245_markdown_file_creation.task_5_push_markdown_file",
                                return_value="Push result",
                            ):
                                result = main()

                                # Check commit message format
                                expected_message = (
                                    "feat(245): create markdown file test-nxclc0.md with prose content"
                                )
                                assert result["commit_message"] == expected_message
        finally:
            if str(src_path) in sys.path:
                sys.path.remove(str(src_path))
