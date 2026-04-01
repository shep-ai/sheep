"""
Unit tests for feature 305: Test function signature, parameters, and structure.

These are pure unit tests that verify:
1. The function exists and is callable
2. The function has correct signature
3. The function correctly calls create_markdown_file() with right parameters
4. Error handling works as expected

These tests use mocking to avoid requiring API credentials.
"""

import sys
from pathlib import Path
from unittest import mock

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sheep.features.feature_305 import (
    FEATURE_NAME,
    FEATURE_NUMBER,
    MARKDOWN_FILENAME,
    create_feature_305_markdown_file,
)


# ============================================================================
# FUNCTION SIGNATURE TESTS
# ============================================================================


def test_function_exists_and_callable():
    """Test that create_feature_305_markdown_file function exists and is callable."""
    assert callable(create_feature_305_markdown_file), \
        "create_feature_305_markdown_file must be callable"
    print("✓ Function exists and is callable")


def test_function_accepts_optional_repo_path():
    """Test that function accepts optional repo_path parameter."""
    import inspect
    sig = inspect.signature(create_feature_305_markdown_file)
    params = sig.parameters

    assert "repo_path" in params, \
        "Function must have repo_path parameter"

    param = params["repo_path"]
    # Check if it has a default value (is optional)
    assert param.default is not inspect.Parameter.empty, \
        "repo_path must be optional (have default value)"

    print("✓ Function accepts optional repo_path parameter")


def test_function_return_type_is_dict():
    """Test that function returns a dict (according to type hints)."""
    import inspect
    sig = inspect.signature(create_feature_305_markdown_file)

    # Check return annotation
    return_annotation = sig.return_annotation
    assert return_annotation != inspect.Signature.empty, \
        "Function must have return type annotation"

    # Should indicate dict
    annotation_str = str(return_annotation)
    assert "dict" in annotation_str.lower(), \
        f"Return type should indicate dict, got: {return_annotation}"

    print("✓ Function has correct return type annotation")


# ============================================================================
# FEATURE METADATA TESTS
# ============================================================================


def test_feature_number_is_305():
    """Test that FEATURE_NUMBER constant is set to 305."""
    assert FEATURE_NUMBER == 305, \
        f"FEATURE_NUMBER must be 305, got {FEATURE_NUMBER}"
    print(f"✓ FEATURE_NUMBER is correctly set to {FEATURE_NUMBER}")


def test_markdown_filename_is_correct():
    """Test that MARKDOWN_FILENAME is set to test-9s145k.md."""
    expected_filename = "test-9s145k.md"
    assert MARKDOWN_FILENAME == expected_filename, \
        f"MARKDOWN_FILENAME must be {expected_filename}, got {MARKDOWN_FILENAME}"
    print(f"✓ MARKDOWN_FILENAME is correctly set to {MARKDOWN_FILENAME}")


def test_feature_name_defined():
    """Test that FEATURE_NAME is defined."""
    assert FEATURE_NAME, \
        "FEATURE_NAME must be defined"
    assert isinstance(FEATURE_NAME, str), \
        f"FEATURE_NAME must be string, got {type(FEATURE_NAME)}"
    print(f"✓ FEATURE_NAME is defined: {FEATURE_NAME}")


# ============================================================================
# ORCHESTRATION CALL TESTS (Mocked)
# ============================================================================


def test_function_calls_create_markdown_file_with_filename():
    """Test that function calls create_markdown_file with correct filename."""
    mock_result = {
        "filepath": "/path/to/test-9s145k.md",
        "content": "# Title\n\nContent here.",
        "commit_message": "feat(305): create markdown file test-9s145k.md with prose content",
        "push_result": "Pushed successfully",
    }

    with mock.patch("sheep.features.feature_305.create_markdown_file", return_value=mock_result) as mock_create:
        result = create_feature_305_markdown_file()

        # Verify create_markdown_file was called
        assert mock_create.called, \
            "create_markdown_file must be called"

        # Get the call arguments
        call_args = mock_create.call_args
        args, kwargs = call_args

        # Check first positional argument is the filename
        assert MARKDOWN_FILENAME in args or MARKDOWN_FILENAME in kwargs.values(), \
            f"Filename {MARKDOWN_FILENAME} must be passed to create_markdown_file"

        print(f"✓ Function calls create_markdown_file with filename: {MARKDOWN_FILENAME}")


def test_function_calls_create_markdown_file_with_feature_number():
    """Test that function calls create_markdown_file with feature_number=305."""
    mock_result = {
        "filepath": "/path/to/test-9s145k.md",
        "content": "# Title\n\nContent here.",
        "commit_message": "feat(305): create markdown file test-9s145k.md with prose content",
        "push_result": "Pushed successfully",
    }

    with mock.patch("sheep.features.feature_305.create_markdown_file", return_value=mock_result) as mock_create:
        result = create_feature_305_markdown_file()

        # Get the call arguments
        call_args = mock_create.call_args
        args, kwargs = call_args

        # Check feature_number is passed correctly
        assert "feature_number" in kwargs, \
            "feature_number must be passed as keyword argument"

        assert kwargs["feature_number"] == FEATURE_NUMBER, \
            f"feature_number must be {FEATURE_NUMBER}, got {kwargs['feature_number']}"

        print(f"✓ Function calls create_markdown_file with feature_number={FEATURE_NUMBER}")


def test_function_calls_create_markdown_file_with_repo_path():
    """Test that function passes repo_path to create_markdown_file."""
    mock_result = {
        "filepath": "/path/to/test-9s145k.md",
        "content": "# Title\n\nContent here.",
        "commit_message": "feat(305): create markdown file test-9s145k.md with prose content",
        "push_result": "Pushed successfully",
    }

    test_repo_path = "/custom/repo/path"

    with mock.patch("sheep.features.feature_305.create_markdown_file", return_value=mock_result) as mock_create:
        result = create_feature_305_markdown_file(repo_path=test_repo_path)

        # Get the call arguments
        call_args = mock_create.call_args
        args, kwargs = call_args

        # Check repo_path is passed
        assert "repo_path" in kwargs or (len(args) > 1), \
            "repo_path must be passed to create_markdown_file"

        if "repo_path" in kwargs:
            assert kwargs["repo_path"] == test_repo_path, \
                f"repo_path should be {test_repo_path}, got {kwargs['repo_path']}"

        print(f"✓ Function correctly passes repo_path to create_markdown_file")


def test_function_returns_create_markdown_file_result():
    """Test that function returns the result from create_markdown_file."""
    mock_result = {
        "filepath": "/path/to/test-9s145k.md",
        "content": "# Sample Title\n\nThis is sentence one. This is sentence two. This is sentence three.",
        "commit_message": "feat(305): create markdown file test-9s145k.md with prose content",
        "push_result": "Pushed to origin/feat/305-markdown-file-creation-e9500c",
    }

    with mock.patch("sheep.features.feature_305.create_markdown_file", return_value=mock_result):
        result = create_feature_305_markdown_file()

        assert result == mock_result, \
            "Function must return the exact result from create_markdown_file"

        assert result["filepath"] == mock_result["filepath"], \
            "Result filepath must match"

        assert result["content"] == mock_result["content"], \
            "Result content must match"

        print("✓ Function returns correct result from create_markdown_file")


def test_function_returns_dict_with_required_keys():
    """Test that returned dict has all required keys."""
    mock_result = {
        "filepath": "/path/to/test-9s145k.md",
        "content": "# Title\n\nSentence one. Sentence two.",
        "commit_message": "feat(305): create markdown file test-9s145k.md with prose content",
        "push_result": "Pushed successfully",
    }

    with mock.patch("sheep.features.feature_305.create_markdown_file", return_value=mock_result):
        result = create_feature_305_markdown_file()

        required_keys = {"filepath", "content", "commit_message", "push_result"}
        result_keys = set(result.keys())

        assert required_keys.issubset(result_keys), \
            f"Result missing keys: {required_keys - result_keys}"

        print(f"✓ Returned dict has all required keys: {sorted(required_keys)}")


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_function_propagates_exceptions():
    """Test that function propagates exceptions (fail-fast pattern)."""
    test_error = ValueError("Test error from create_markdown_file")

    with mock.patch("sheep.features.feature_305.create_markdown_file", side_effect=test_error):
        try:
            create_feature_305_markdown_file()
            assert False, "Function should propagate exception"
        except ValueError as e:
            assert str(e) == "Test error from create_markdown_file", \
                f"Should propagate original error, got: {e}"

        print("✓ Function correctly propagates exceptions (fail-fast)")


def test_function_logs_on_success():
    """Test that function logs when successful."""
    mock_result = {
        "filepath": "/path/to/test-9s145k.md",
        "content": "# Title\n\nSentence.",
        "commit_message": "feat(305): create markdown file test-9s145k.md with prose content",
        "push_result": "Pushed",
    }

    with mock.patch("sheep.features.feature_305.create_markdown_file", return_value=mock_result):
        with mock.patch("sheep.features.feature_305._logger") as mock_logger:
            result = create_feature_305_markdown_file()

            # Check that logger was called
            assert mock_logger.info.called, \
                "Logger must be called"

            print("✓ Function logs on success")


def test_function_logs_on_failure():
    """Test that function logs errors."""
    test_error = RuntimeError("Test failure")

    with mock.patch("sheep.features.feature_305.create_markdown_file", side_effect=test_error):
        with mock.patch("sheep.features.feature_305._logger") as mock_logger:
            try:
                create_feature_305_markdown_file()
            except RuntimeError:
                pass

            # Check that logger error was called
            assert mock_logger.error.called, \
                "Logger.error must be called on failure"

            print("✓ Function logs errors correctly")


# ============================================================================
# RUN TESTS
# ============================================================================


if __name__ == "__main__":
    """Run all unit tests."""
    tests = [
        # Function signature tests
        ("Function exists and callable", test_function_exists_and_callable),
        ("Function accepts repo_path", test_function_accepts_optional_repo_path),
        ("Function return type is dict", test_function_return_type_is_dict),

        # Feature metadata tests
        ("FEATURE_NUMBER is 305", test_feature_number_is_305),
        ("MARKDOWN_FILENAME is correct", test_markdown_filename_is_correct),
        ("FEATURE_NAME is defined", test_feature_name_defined),

        # Orchestration tests
        ("Calls create_markdown_file with filename", test_function_calls_create_markdown_file_with_filename),
        ("Calls create_markdown_file with feature_number", test_function_calls_create_markdown_file_with_feature_number),
        ("Passes repo_path correctly", test_function_calls_create_markdown_file_with_repo_path),
        ("Returns create_markdown_file result", test_function_returns_create_markdown_file_result),
        ("Result has required keys", test_function_returns_dict_with_required_keys),

        # Error handling tests
        ("Propagates exceptions", test_function_propagates_exceptions),
        ("Logs on success", test_function_logs_on_success),
        ("Logs on failure", test_function_logs_on_failure),
    ]

    passed = 0
    failed = 0

    print(f"\n{'='*70}")
    print(f"Running Feature 305 Unit Tests")
    print(f"{'='*70}\n")

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_name}: Unexpected error: {e}")
            failed += 1

    print(f"\n{'='*70}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print(f"{'='*70}\n")

    if failed > 0:
        sys.exit(1)
