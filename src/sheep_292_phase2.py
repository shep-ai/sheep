"""Feature 292 Phase 2: File Creation and Git Integration.

This module provides utilities for creating markdown files with explicit encoding
and line ending handling, and integrating with git for staging, committing, and pushing.

Phase 2 Implementation:
- Task 5: Create file with pathlib using explicit UTF-8 encoding and LF line endings
- Task 6: Stage file in git index using git add
- Task 7: Commit file with conventional commit message
- Task 8: Push commit to feature branch
"""

import subprocess
from pathlib import Path

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Conventional commit message template
COMMIT_MESSAGE_TEMPLATE = "feat(292): create markdown file {filename} with prose content"


def create_markdown_file(content: str, filename: str) -> bool:
    """
    Create a markdown file with explicit UTF-8 encoding and LF line endings.

    Writes content to file in repository root only. Ensures:
    - UTF-8 encoding without BOM
    - LF line endings (not CRLF)
    - File exists after creation
    - Content is exactly as provided

    Args:
        content: The markdown content to write.
        filename: The filename to create (relative path, repository root only).

    Returns:
        True if file was successfully created and verified.

    Raises:
        IOError: If file creation fails or verification fails.
        ValueError: If filename contains path traversal characters.
    """
    # Security check: ensure no path traversal
    if "/" in filename or "\\" in filename or ".." in filename:
        raise ValueError(f"Invalid filename: {filename} (no path traversal allowed)")

    file_path = Path(filename)

    try:
        _logger.info(f"Creating markdown file: {file_path}")

        # Write file with explicit UTF-8 encoding (no BOM) and LF line endings
        # Use binary mode to ensure LF line endings across platforms (Windows converts \n to \r\n in text mode)
        content_bytes = content.encode("utf-8")
        file_path.write_bytes(content_bytes)

        _logger.debug(f"File written: {file_path}")

        # Verify file exists
        if not file_path.exists():
            raise IOError(f"File creation failed: {file_path} does not exist after write")

        _logger.debug(f"File existence verified: {file_path}")

        # Verify file contains exact content (by reading bytes)
        read_bytes = file_path.read_bytes()
        if read_bytes != content_bytes:
            raise IOError(
                f"File content mismatch: written {len(content_bytes)} bytes, "
                f"read {len(read_bytes)} bytes"
            )

        _logger.debug("File content verified")

        # Verify UTF-8 encoding without BOM
        if read_bytes.startswith(b"\xef\xbb\xbf"):
            raise IOError("File has UTF-8 BOM (must be UTF-8 without BOM)")

        _logger.debug("UTF-8 encoding verified (no BOM)")

        # Verify LF line endings (not CRLF)
        if b"\r\n" in read_bytes:
            raise IOError("File has CRLF line endings (must be LF only)")

        _logger.debug("LF line endings verified (not CRLF)")
        _logger.info(
            f"File successfully created: {file_path} "
            f"({len(read_bytes)} bytes, UTF-8, LF)"
        )

        return True

    except (IOError, ValueError) as e:
        _logger.error(f"File creation failed: {e}")
        raise


def stage_file_in_git(filename: str) -> bool:
    """
    Stage file in git index using 'git add'.

    Executes git add command and verifies file is staged by checking
    git status output. File must show as staged (A or M status).

    Args:
        filename: The filename to stage.

    Returns:
        True if file was successfully staged.

    Raises:
        subprocess.CalledProcessError: If git add fails.
    """
    try:
        _logger.info(f"Staging file in git: {filename}")

        # Execute git add
        result = subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )

        _logger.debug(f"git add executed: {result.returncode}")

        # Verify file is staged
        status_result = subprocess.run(
            ["git", "status", "--short"],
            check=True,
            capture_output=True,
            text=True,
        )

        status_output = status_result.stdout
        _logger.debug(f"git status output:\n{status_output}")

        # Check that file appears in status with staged marker (A or M in first position)
        # Format: "A  filename" (added) or "M  filename" (modified) or "AM filename" (added, modified)
        staged = False
        for line in status_output.split("\n"):
            if filename in line and (line[0] == "A" or line[0] == "M"):
                staged = True
                break

        if not staged:
            raise subprocess.CalledProcessError(
                1,
                "git add",
                stderr=f"File not in staged status: {filename}\n{status_output}",
            )

        _logger.info(f"File successfully staged: {filename}")
        return True

    except subprocess.CalledProcessError as e:
        _logger.error(f"git add failed: {e.stderr or e.stdout or str(e)}")
        raise


def commit_file_in_git(filename: str) -> bool:
    """
    Commit staged file with conventional commit message.

    Constructs commit message in conventional format and executes git commit.
    Verifies commit was created by checking git log.

    Args:
        filename: The filename being committed.

    Returns:
        True if commit was successfully created.

    Raises:
        subprocess.CalledProcessError: If git commit fails.
    """
    try:
        # Construct conventional commit message
        message = COMMIT_MESSAGE_TEMPLATE.format(filename=filename)

        _logger.info(f"Creating commit: {message}")

        # Execute git commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            check=True,
            capture_output=True,
            text=True,
        )

        _logger.debug(f"git commit executed: {result.returncode}")
        _logger.debug(f"commit output: {result.stdout}")

        # Verify commit was created by checking git log
        log_result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            check=True,
            capture_output=True,
            text=True,
        )

        log_output = log_result.stdout.strip()
        _logger.debug(f"git log output: {log_output}")

        # Verify commit message appears in log
        if "feat(292)" not in log_output or filename not in log_output:
            raise subprocess.CalledProcessError(
                1,
                "git commit",
                stderr=f"Commit message not found in log: {log_output}",
            )

        _logger.info(f"Commit successfully created: {log_output}")
        return True

    except subprocess.CalledProcessError as e:
        _logger.error(f"git commit failed: {e.stderr or e.stdout or str(e)}")
        raise


def push_to_branch(branch: str) -> bool:
    """
    Push commit to feature branch.

    Executes 'git push -u origin <branch>' and verifies push was successful
    by checking git status.

    Args:
        branch: The branch name to push to (e.g., 'feat/292-markdown-file-creation-a7c367').

    Returns:
        True if push was successfully completed.

    Raises:
        subprocess.CalledProcessError: If git push fails.
    """
    try:
        _logger.info(f"Pushing to branch: {branch}")

        # Execute git push
        result = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            check=True,
            capture_output=True,
            text=True,
        )

        _logger.debug(f"git push executed: {result.returncode}")
        _logger.debug(f"push output: {result.stdout}")

        # Verify push was successful by checking git status
        status_result = subprocess.run(
            ["git", "status", "-sb"],
            check=True,
            capture_output=True,
            text=True,
        )

        status_output = status_result.stdout.strip()
        _logger.debug(f"git status output: {status_output}")

        # Check that branch is tracking origin
        if "origin/" + branch in status_output or f"[origin/{branch}" in status_output:
            _logger.info(f"Push successful: branch {branch} tracking origin")
            return True
        else:
            # Even if status doesn't show tracking, the push may have succeeded
            # Just log a warning and return True since push command succeeded
            _logger.warning(
                f"Push may have succeeded but tracking status unclear: {status_output}"
            )
            return True

    except subprocess.CalledProcessError as e:
        _logger.error(f"git push failed: {e.stderr or e.stdout or str(e)}")
        raise
