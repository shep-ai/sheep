"""Content generation utilities for creating markdown and other content."""

import subprocess
from pathlib import Path

from sheep.config.llm import get_reasoning_llm
from sheep.observability.logging import get_logger
from sheep.tools import GitCommitTool, GitPushTool

_logger = get_logger(__name__)

# Prompt template for markdown generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following structure:
1. An H1 heading (using #) with a title about any topic you choose
2. A blank line
3. Exactly 2-3 sentences of coherent prose about that topic

Return ONLY the markdown content, no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def generate_markdown_content() -> str:
    """
    Generate markdown content with an H1 heading and 2-3 sentences of prose.

    Uses Claude API via CrewAI LLM framework to generate coherent,
    contextually-appropriate prose about any topic.

    Returns:
        String containing valid markdown with H1 heading and prose content.

    Raises:
        ValueError: If generated content doesn't meet format requirements.
        Exception: If LLM API call fails.
    """
    llm = get_reasoning_llm()
    _logger.info("Generating markdown content with reasoning LLM")

    try:
        # Call LLM with the prompt
        response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

        # Extract the response text
        if isinstance(response, dict):
            content = str(response.get("content", str(response)))
        else:
            content = str(response)

        _logger.debug(f"Raw LLM response: {content[:100]}...")

        # Ensure trailing newline (Unix convention)
        if not content.endswith("\n"):
            content = content + "\n"

        # Validate the response format
        _validate_markdown_content(content)

        _logger.info("Markdown content generated successfully")
        return content

    except Exception as e:
        _logger.error(f"Failed to generate markdown content: {e}")
        raise


def _validate_markdown_content(content: str) -> None:
    """
    Validate that generated content meets markdown format requirements.

    Args:
        content: The generated markdown content to validate.

    Raises:
        ValueError: If content doesn't meet format requirements.
    """
    # Check that content is not empty
    if not content or not content.strip():
        raise ValueError("Generated content is empty")

    # Check for H1 heading
    if not content.lstrip().startswith("# "):
        raise ValueError("Content must start with H1 heading (# )")

    # Check that content has reasonable length
    if len(content) < 50:
        raise ValueError("Generated content is too short to be meaningful")

    # Check for sentence structure (count periods)
    sentence_count = content.count(".")
    if sentence_count < 2 or sentence_count > 3:
        raise ValueError(
            f"Content should have 2-3 sentences, found {sentence_count}"
        )


def write_markdown_file(content: str, filename: str) -> str:
    """
    Write generated markdown content to a file at the repository root.

    Args:
        content: The markdown content to write.
        filename: The filename to create (e.g., "test-9veux3.md").

    Returns:
        Path to the created file as a string on success.

    Raises:
        ValueError: If content is invalid or file path is unsafe.
        IOError: If file write operation fails.
    """
    # Validate that filename is safe (not a path traversal)
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise ValueError(f"Invalid filename: {filename}")

    # Resolve the repository root (current working directory)
    repo_root = Path.cwd()
    file_path = repo_root / filename

    _logger.info(f"Writing markdown file to {file_path}")

    try:
        # Write file with UTF-8 encoding and explicit LF line endings (newline='')
        # prevents platform-specific line ending conversion (CRLF on Windows)
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.write(content)

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {file_path}")

        # Verify file has content
        file_size = file_path.stat().st_size
        if file_size == 0:
            raise OSError(f"File was created but is empty: {file_path}")

        _logger.info(
            f"Successfully wrote markdown file: {file_path} ({file_size} bytes)"
        )
        return str(file_path)

    except Exception as e:
        _logger.error(f"Failed to write markdown file: {e}")
        raise


def validate_file_properties(filepath: str) -> bool:
    """
    Validate that a file meets encoding and line ending requirements.

    Checks for:
    - File exists and is readable
    - UTF-8 encoding with no BOM (Byte Order Mark)
    - Unix LF line endings (not CRLF)

    This function validates file properties only, not content or structure.
    It uses efficient binary read to check encoding/line endings.

    Args:
        filepath: Path to the file to validate.

    Returns:
        True if file passes all property validation checks.

    Raises:
        ValueError: If file fails any validation check with descriptive message.
    """
    path = Path(filepath)

    if not path.exists():
        raise ValueError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {filepath}")

    _logger.info(f"Validating file properties: {filepath}")

    try:
        # Read file as binary to check encoding and line endings
        with open(path, "rb") as f:
            binary_content = f.read()

        # Check for UTF-8 BOM (should not be present)
        if binary_content.startswith(b"\xef\xbb\xbf"):
            raise ValueError("File has UTF-8 BOM (should not be present)")

        # Check for CRLF line endings (should use LF instead)
        if b"\r\n" in binary_content:
            raise ValueError("File uses CRLF line endings (should use LF)")

        # Verify the file is valid UTF-8
        try:
            binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"File is not valid UTF-8: {e}")

        _logger.info(f"File properties validation passed: {filepath}")
        return True

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Unexpected error during property validation: {e}")
        raise ValueError(f"Error validating file properties: {e}")


def validate_markdown_file(filepath: str) -> bool:
    """
    Validate that a markdown file meets all non-functional requirements.

    Checks for:
    - Valid markdown syntax (H1 heading, blank line separator)
    - Proper prose content (2-3 sentences)
    - UTF-8 encoding with no BOM
    - Unix LF line endings (not CRLF)
    - Trailing newline

    Args:
        filepath: Path to the markdown file to validate.

    Returns:
        True if file passes all validation checks.

    Raises:
        ValueError: If file fails any validation check with descriptive message.
        IOError: If file cannot be read.
    """
    path = Path(filepath)

    if not path.exists():
        raise OSError(f"File does not exist: {filepath}")

    if not path.is_file():
        raise OSError(f"Path is not a file: {filepath}")

    _logger.info(f"Validating markdown file: {filepath}")

    try:
        # Read file as binary to check encoding and line endings
        with open(path, "rb") as f:
            binary_content = f.read()

        # Check for UTF-8 BOM (should not be present)
        if binary_content.startswith(b"\xef\xbb\xbf"):
            raise ValueError("File has UTF-8 BOM (should not be present)")

        # Decode as UTF-8 to verify encoding
        try:
            text_content = binary_content.decode("utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(f"File is not valid UTF-8: {e}")

        # Check for CRLF line endings (should use LF instead)
        if b"\r\n" in binary_content:
            raise ValueError("File uses CRLF line endings (should use LF)")

        # Check for H1 heading at start
        if not text_content.lstrip().startswith("# "):
            raise ValueError("File must start with H1 heading (# )")

        lines = text_content.split("\n")

        # Check that first line is H1 heading
        if not lines[0].startswith("# "):
            raise ValueError("First line must be H1 heading (# )")

        # Check that second line is blank (separator)
        if len(lines) < 2 or lines[1] != "":
            raise ValueError("Second line must be blank (separator after heading)")

        # Get prose content (skip heading and blank line)
        prose_lines = lines[2:]

        # Remove trailing empty lines for prose validation
        while prose_lines and prose_lines[-1] == "":
            prose_lines.pop()

        if not prose_lines:
            raise ValueError("No prose content found after heading")

        prose_content = "\n".join(prose_lines).strip()

        # Validate sentence count (count periods)
        sentence_count = prose_content.count(".")
        if sentence_count < 2 or sentence_count > 3:
            raise ValueError(
                f"Content must have 2-3 sentences, found {sentence_count}"
            )

        # Check for trailing newline (Unix convention)
        if not text_content.endswith("\n"):
            raise ValueError("File must end with trailing newline")

        _logger.info(f"Markdown file validation passed: {filepath}")
        return True

    except (OSError, ValueError):
        raise
    except Exception as e:
        _logger.error(f"Unexpected error during validation: {e}")
        raise OSError(f"Error validating file: {e}")


def extract_topic_from_content(content: str) -> str:
    """
    Extract the topic/title from markdown content.

    Extracts the H1 heading from the markdown content to use as the topic
    in the commit message.

    Args:
        content: The markdown content string.

    Returns:
        The topic extracted from the H1 heading (without the # prefix).

    Raises:
        ValueError: If no H1 heading is found.
    """
    lines = content.split("\n")
    if not lines or not lines[0].startswith("# "):
        raise ValueError("No H1 heading found in content")

    topic = lines[0].replace("# ", "").strip()
    if not topic:
        raise ValueError("H1 heading is empty")

    return topic


def commit_markdown_file(
    filepath: str,
    content: str,
    repo_path: str | None = None,
    custom_message: str | None = None,
    feature_number: int | None = None,
) -> str:
    """
    Stage and commit the markdown file with a conventional commit message.

    Args:
        filepath: Path to the markdown file to commit.
        content: The markdown content (used to extract topic for commit message).
        repo_path: Path to the git repository (defaults to current directory).
        custom_message: Optional custom commit message to use instead of auto-generated.
        feature_number: Feature number for conventional commit scope (defaults to 272).

    Returns:
        The commit result message from GitCommitTool.

    Raises:
        ValueError: If content is invalid or topic cannot be extracted.
        Exception: If git commit fails.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    if feature_number is None:
        feature_number = 272

    _logger.info(f"Committing markdown file: {filepath}")

    try:
        # Get filename only (for message clarity)
        filename = Path(filepath).name

        # Use custom message if provided, otherwise generate from content
        if custom_message:
            commit_message = custom_message
            _logger.debug(f"Using custom commit message: {commit_message}")
        else:
            # Format commit message: "feat(272): create markdown file test-visstj.md with prose content"
            commit_message = f"feat({feature_number}): create markdown file {filename} with prose content"

        _logger.debug(f"Commit message: {commit_message}")

        # Use GitCommitTool to stage and commit
        tool = GitCommitTool()
        result = tool._run(repo_path=repo_path, message=commit_message, add_all=True)

        _logger.info(f"Markdown file committed: {filename}")
        return result

    except Exception as e:
        _logger.error(f"Failed to commit markdown file: {e}")
        raise


def push_markdown_file(repo_path: str | None = None, remote: str = "origin") -> str:
    """
    Push the committed markdown file to remote repository.

    Args:
        repo_path: Path to the git repository (defaults to current directory).
        remote: Remote name to push to (default: origin).

    Returns:
        The push result message from GitPushTool.

    Raises:
        Exception: If git push fails.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    _logger.info(f"Pushing to remote {remote}")

    try:
        # Use GitPushTool to push with upstream tracking
        tool = GitPushTool()
        result = tool._run(repo_path=repo_path, remote=remote, set_upstream=True)

        _logger.info(f"Successfully pushed to {remote}")
        return result

    except Exception as e:
        _logger.error(f"Failed to push to remote: {e}")
        raise


def git_add(filename: str, repo_path: str | None = None) -> str:
    """
    Stage a file with git add using subprocess.

    Args:
        filename: Name of the file to add (e.g., "test-msqxtg.md").
        repo_path: Path to the git repository (defaults to current directory).

    Returns:
        Success message with exit code 0.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        subprocess.CalledProcessError: If git add fails.
        ValueError: If filename is invalid.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    # Validate filename
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise ValueError(f"Invalid filename: {filename}")

    repo_root = Path(repo_path)
    file_path = repo_root / filename

    _logger.info(f"Staging file with git add: {filename}")

    try:
        # Check if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")

        # Run git add
        result = subprocess.run(
            ["git", "add", filename],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )

        _logger.info(f"Successfully staged file: {filename}")
        return f"Successfully added {filename} (exit code: {result.returncode})"

    except FileNotFoundError:
        _logger.error(f"File not found: {file_path}")
        raise
    except subprocess.CalledProcessError as e:
        _logger.error(f"git add failed: {e.stderr}")
        raise
    except Exception as e:
        _logger.error(f"Unexpected error in git_add: {e}")
        raise


def git_commit(message: str, repo_path: str | None = None) -> str:
    """
    Create a git commit with the exact specified message using subprocess.

    Args:
        message: Exact commit message to use.
        repo_path: Path to the git repository (defaults to current directory).

    Returns:
        Commit result message with exit code 0.

    Raises:
        subprocess.CalledProcessError: If git commit fails.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    repo_root = Path(repo_path)

    _logger.info(f"Creating git commit with message: {message}")

    try:
        # Run git commit with exact message
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )

        _logger.info(f"Successfully created commit: {message}")
        return f"Committed: {message}\n{result.stdout}"

    except subprocess.CalledProcessError as e:
        # Check if nothing to commit (not an error)
        if "nothing to commit" in e.stderr.lower():
            _logger.warning("Nothing to commit, working tree clean")
            return "Nothing to commit, working tree clean."
        _logger.error(f"git commit failed: {e.stderr}")
        raise
    except Exception as e:
        _logger.error(f"Unexpected error in git_commit: {e}")
        raise


def git_push(repo_path: str | None = None, remote: str = "origin") -> str:
    """
    Push to remote repository with upstream tracking using subprocess.

    Args:
        repo_path: Path to the git repository (defaults to current directory).
        remote: Remote name to push to (default: origin).

    Returns:
        Push result message with exit code 0.

    Raises:
        subprocess.CalledProcessError: If git push fails.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    repo_root = Path(repo_path)

    _logger.info(f"Pushing to remote {remote} with upstream tracking")

    try:
        # Get current branch
        result_branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = result_branch.stdout.strip()
        _logger.debug(f"Current branch: {current_branch}")

        # Run git push with upstream tracking (-u flag)
        result = subprocess.run(
            ["git", "push", "-u", remote, current_branch],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )

        _logger.info(f"Successfully pushed to {remote}/{current_branch}")
        return f"Pushed to {remote}/{current_branch}\n{result.stderr}"

    except subprocess.CalledProcessError as e:
        _logger.error(f"git push failed: {e.stderr}")
        raise
    except Exception as e:
        _logger.error(f"Unexpected error in git_push: {e}")
        raise


def create_markdown_file(
    filename: str, repo_path: str | None = None, feature_number: int | None = None
) -> dict[str, str]:
    """
    Orchestrate the complete workflow to create, write, commit, and push a markdown file.

    This is the main entry point that combines all previous functions into a single
    end-to-end workflow:
    1. Generate markdown content (title + 2-3 sentences)
    2. Write file to disk at repository root
    3. Validate the file meets all requirements
    4. Stage and commit with conventional message
    5. Push to remote with upstream tracking

    Args:
        filename: Name of the markdown file to create (e.g., "test-visstj.md").
        repo_path: Path to the git repository (defaults to current directory).
        feature_number: Feature number for conventional commit scope (defaults to 272).

    Returns:
        Dictionary containing:
        - filepath: Full path to the created file
        - content: The markdown content
        - commit_message: The git commit message used
        - push_result: The result from git push operation

    Raises:
        ValueError: If filename or content is invalid.
        IOError: If file operations fail.
        Exception: If git operations fail.
    """
    if repo_path is None:
        repo_path = str(Path.cwd())

    if feature_number is None:
        feature_number = 272

    _logger.info(f"Creating markdown file: {filename}")

    try:
        # Step 1: Generate markdown content
        _logger.info("Step 1: Generating markdown content")
        content = generate_markdown_content()
        _logger.debug(f"Generated {len(content)} bytes of content")

        # Step 2: Write file to disk
        _logger.info("Step 2: Writing markdown file to disk")
        filepath = write_markdown_file(content, filename)
        _logger.debug(f"File written to: {filepath}")

        # Step 3: Validate file
        _logger.info("Step 3: Validating markdown file")
        validate_markdown_file(filepath)
        _logger.info("File validation passed")

        # Step 4: Commit file
        _logger.info("Step 4: Committing markdown file")
        commit_result = commit_markdown_file(filepath, content, repo_path, feature_number=feature_number)
        _logger.debug(f"Commit result: {commit_result}")

        # Construct commit message for return value (matches what was committed)
        commit_message = f"feat({feature_number}): create markdown file {filename} with prose content"

        # Step 5: Push to remote
        _logger.info("Step 5: Pushing to remote repository")
        push_result = push_markdown_file(repo_path)
        _logger.debug(f"Push result: {push_result}")

        _logger.info(f"Successfully created and published markdown file: {filename}")

        return {
            "filepath": filepath,
            "content": content,
            "commit_message": commit_message,
            "push_result": push_result,
        }

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise
