"""Implementation for feature 208: Create markdown file test-mujic0.md with Claude API.

This module orchestrates the creation of a markdown file using Claude API with temperature=0
for deterministic, AI-generated content. Following the established pattern from feature 207
with the LLM integration approach from features 200+, this feature demonstrates the Sheep
platform's capability to execute deterministic file creation workflows with Claude API integration.

The file is created with:
- Exact filename: test-mujic0.md
- H1 markdown heading as title (AI-generated)
- 2-3 sentences of prose content (AI-generated with temperature=0)
- UTF-8 encoding without BOM
- Unix LF line endings
- File size between 250-600 bytes
- Git staging, commit, and push operations

This approach provides:
- Deterministic output (identical on repeated execution with temperature=0)
- AI-generated content leveraging Claude API
- Simplified error handling with comprehensive validation
- Reliable testing and review (reproducible results)
- Demonstrates LLM integration within the Sheep platform
"""

import subprocess
import sys
from pathlib import Path

from sheep.config.llm import create_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 208 constants
FILENAME = "test-mujic0.md"
FEATURE_NUMBER = 208
BRANCH_NAME = "feat/markdown-file-creation-9f7556"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with AI-generated content"

# Prompt template for deterministic markdown content generation with temperature=0
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title
4. Each sentence must end with a period

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def extract_prose_content(filename: str = FILENAME) -> str:
    """Extract prose content from file (text after blank line).

    Args:
        filename: Name of file to extract from (default: FILENAME)

    Returns:
        Prose content (text after H1 heading and blank line)

    Example:
        >>> prose = extract_prose_content("test-mujic0.md")
        >>> print(prose)
    """
    content = Path(filename).read_text(encoding="utf-8")
    lines = content.split("\n")

    # Prose starts after the blank line (line 2)
    # Join remaining lines, strip trailing whitespace
    if len(lines) > 2:
        prose = "\n".join(lines[2:]).strip()
        return prose

    return ""


def count_sentences(prose: str) -> int:
    """Count sentences in prose content (count periods).

    Uses simple period counting for human-written prose with proper punctuation.

    Args:
        prose: Text content to analyze

    Returns:
        Number of periods (sentences) in prose

    Example:
        >>> count_sentences("First sentence. Second sentence.")
        2
    """
    return prose.count(".")


def generate_content() -> tuple[str, str]:
    """Generate H1 title and 2-3 sentences of prose using Claude API with temperature=0.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same execution produces identical content on repeated calls.

    The function:
    1. Calls Claude API with markdown generation prompt
    2. Parses response to extract H1 title and prose
    3. Validates sentence count (2-3 periods)
    4. Returns tuple of (title_text, prose_text)

    Returns:
        Tuple of (title, prose) where:
        - title: H1 heading text (without # prefix)
        - prose: 2-3 sentences of prose content

    Raises:
        ValueError: If API response format is invalid or requirements not met
        Exception: If Claude API call fails

    Example:
        >>> title, prose = generate_content()
        >>> print(f"# {title}\\n\\n{prose}")
        # Example Title
        <BLANKLINE>
        This is a sentence. This is another sentence.
    """
    _logger.info("Generating markdown content using Claude API (temperature=0)")

    try:
        # Create LLM with temperature=0 for deterministic generation
        llm = create_llm(temperature=0)

        # Call Claude API with the generation prompt
        response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

        # Extract response text
        if isinstance(response, dict):
            content = str(response.get("content", str(response)))
        else:
            content = str(response)

        _logger.debug(f"Raw LLM response (first 100 chars): {content[:100]}...")

        # Parse markdown content
        lines = content.strip().split("\n")

        # Find and extract H1 title (first line should start with "# ")
        if not lines or not lines[0].startswith("# "):
            raise ValueError(
                "Generated content must start with H1 heading (# Title)"
            )

        title = lines[0].replace("# ", "").strip()
        if not title:
            raise ValueError("Generated title is empty")

        # Find blank line separator (should be after title)
        blank_line_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "" and i > 0:
                blank_line_idx = i
                break

        if blank_line_idx is None:
            raise ValueError(
                "Generated content missing blank line separator after heading"
            )

        # Extract prose content (all lines after blank line)
        prose_lines = lines[blank_line_idx + 1 :]
        prose = "\n".join(prose_lines).strip()

        if not prose:
            raise ValueError("Generated prose content is empty")

        # Validate sentence count (2-3 periods)
        sentence_count = prose.count(".")
        if not (2 <= sentence_count <= 3):
            raise ValueError(
                f"Generated prose has {sentence_count} sentences, expected 2-3"
            )

        _logger.info(
            f"Successfully generated content: title='{title}', "
            f"prose_length={len(prose)}, sentence_count={sentence_count}"
        )
        return (title, prose)

    except ValueError as e:
        _logger.error(f"Validation failed in generate_content: {e}")
        raise
    except Exception as e:
        _logger.error(f"Failed to generate content: {e}")
        raise


def create_markdown_file() -> Path:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings via pathlib.Path.write_text().

    Returns:
        Path object pointing to created file

    Raises:
        ValueError: If file creation fails
        OSError: If file write operation fails
    """
    _logger.info(f"Creating markdown file: {FILENAME}")

    try:
        # Generate content using Claude API
        title, prose = generate_content()

        # Construct markdown content: # Title \n \n Prose
        markdown_content = f"# {title}\n\n{prose}\n"

        # Write file with UTF-8 encoding and LF line endings
        file_path = Path(FILENAME)
        file_path.write_text(markdown_content, encoding="utf-8")

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {file_path}")

        file_size = file_path.stat().st_size
        _logger.info(f"Successfully created {FILENAME} ({file_size} bytes)")

        return file_path

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


def verify_file_exists(filename: str = FILENAME) -> None:
    """Verify that markdown file exists.

    Args:
        filename: Name of file to verify (default: FILENAME)

    Raises:
        FileNotFoundError: If file does not exist

    Example:
        >>> verify_file_exists("test-mujic0.md")  # Raises if missing
    """
    _logger.debug(f"Verifying file exists: {filename}")

    if not Path(filename).exists():
        raise FileNotFoundError(f"File not found: {filename}")

    _logger.debug(f"File exists: {filename}")


def validate_markdown_format(filename: str = FILENAME) -> None:
    """Validate markdown file structure: H1 heading, blank line, content.

    Checks:
    1. First line is H1 heading (starts with '# ')
    2. Second line is blank
    3. Exactly one H1 heading in entire file

    Args:
        filename: Name of file to validate (default: FILENAME)

    Raises:
        ValueError: If markdown format is invalid

    Example:
        >>> validate_markdown_format("test-mujic0.md")
    """
    _logger.debug(f"Validating markdown format: {filename}")

    try:
        content = Path(filename).read_text(encoding="utf-8")
        lines = content.split("\n")

        # Check first line is H1 heading
        if not lines or not lines[0].startswith("# "):
            raise ValueError(
                "File must start with H1 heading (line begins with '# ')"
            )

        # Check second line is blank
        if len(lines) < 2 or lines[1].strip() != "":
            raise ValueError(
                "Second line must be blank (blank line after H1 heading)"
            )

        # Check exactly one H1 heading
        h1_count = sum(1 for line in lines if line.startswith("# "))
        if h1_count != 1:
            raise ValueError(
                f"File must contain exactly one H1 heading, found {h1_count}"
            )

        _logger.debug(f"Markdown format valid: {filename}")

    except ValueError:
        raise
    except Exception as e:
        _logger.error(f"Error validating markdown format: {e}")
        raise ValueError(f"Error validating markdown format: {e}") from e


def validate_sentence_count(filename: str = FILENAME) -> None:
    """Validate that file contains exactly 2-3 sentences.

    Args:
        filename: Name of file to validate (default: FILENAME)

    Raises:
        ValueError: If sentence count not 2-3

    Example:
        >>> validate_sentence_count("test-mujic0.md")
    """
    _logger.debug(f"Validating sentence count: {filename}")

    prose = extract_prose_content(filename)
    sentence_count = count_sentences(prose)

    if sentence_count not in (2, 3):
        raise ValueError(
            f"File must contain exactly 2 or 3 sentences, "
            f"found {sentence_count}"
        )

    _logger.debug(f"Sentence count valid ({sentence_count}): {filename}")


def validate_encoding(filename: str = FILENAME) -> None:
    """Validate file is UTF-8 encoded without BOM (Byte Order Mark).

    Checks:
    1. File does not start with UTF-8 BOM (bytes: EF BB BF)
    2. File decodes successfully as UTF-8

    Args:
        filename: Name of file to validate (default: FILENAME)

    Raises:
        ValueError: If encoding is invalid or BOM present

    Example:
        >>> validate_encoding("test-mujic0.md")
    """
    _logger.debug(f"Validating encoding: {filename}")

    binary_content = Path(filename).read_bytes()

    # Check for UTF-8 BOM
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError(
            "File must not contain UTF-8 BOM (Byte Order Mark)"
        )

    # Check valid UTF-8 decoding
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(
            f"File must be valid UTF-8 encoding: {e}"
        ) from e

    _logger.debug(f"Encoding valid (UTF-8 no BOM): {filename}")


def validate_line_endings(filename: str = FILENAME) -> None:
    """Validate file uses Unix LF line endings only (no CRLF or CR).

    Checks:
    1. File does not contain CRLF (Windows line ending: \\r\\n)
    2. File does not contain CR (Mac line ending: \\r)

    Args:
        filename: Name of file to validate (default: FILENAME)

    Raises:
        ValueError: If non-LF line endings found

    Example:
        >>> validate_line_endings("test-mujic0.md")
    """
    _logger.debug(f"Validating line endings: {filename}")

    binary_content = Path(filename).read_bytes()

    # Check for Windows CRLF
    if b"\r\n" in binary_content:
        raise ValueError(
            "File must use Unix LF line endings only, "
            "not Windows CRLF (\\r\\n)"
        )

    # Check for Mac CR
    if b"\r" in binary_content:
        raise ValueError(
            "File must use Unix LF line endings only, "
            "not Mac CR (\\r)"
        )

    _logger.debug(f"Line endings valid (LF only): {filename}")


def validate_file_size(
    filename: str = FILENAME, min_bytes: int = 250, max_bytes: int = 600
) -> None:
    """Validate file size is within acceptable range.

    Args:
        filename: Name of file to validate (default: FILENAME)
        min_bytes: Minimum file size in bytes (default: 250)
        max_bytes: Maximum file size in bytes (default: 600)

    Raises:
        ValueError: If file size outside range

    Example:
        >>> validate_file_size("test-mujic0.md", min_bytes=250, max_bytes=600)
    """
    _logger.debug(
        f"Validating file size: {filename} "
        f"(range: {min_bytes}-{max_bytes} bytes)"
    )

    file_size = Path(filename).stat().st_size

    if file_size < min_bytes:
        raise ValueError(
            f"File size {file_size} bytes is too small, "
            f"minimum is {min_bytes} bytes"
        )

    if file_size > max_bytes:
        raise ValueError(
            f"File size {file_size} bytes is too large, "
            f"maximum is {max_bytes} bytes"
        )

    _logger.debug(f"File size valid ({file_size} bytes): {filename}")


def validate_markdown_file(filename: str = FILENAME) -> None:
    """Orchestrate comprehensive validation of markdown file.

    Runs all validation checks in sequence:
    1. File exists
    2. Markdown format (H1, blank line, single heading)
    3. Sentence count (2-3 sentences)
    4. UTF-8 encoding without BOM
    5. Unix LF line endings
    6. File size (250-600 bytes)

    Provides fail-fast behavior: stops at first error.

    Args:
        filename: Name of file to validate (default: FILENAME)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If any validation check fails

    Example:
        >>> validate_markdown_file("test-mujic0.md")
    """
    _logger.info("Starting comprehensive validation of markdown file")

    try:
        # Check 1: File exists
        _logger.info("Check 1: Verifying file exists")
        verify_file_exists(filename)
        _logger.debug("✓ File exists")

        # Check 2: Markdown format
        _logger.info("Check 2: Validating markdown format")
        validate_markdown_format(filename)
        _logger.debug("✓ Markdown format valid")

        # Check 3: Sentence count
        _logger.info("Check 3: Validating sentence count (2-3)")
        validate_sentence_count(filename)
        _logger.debug("✓ Sentence count valid")

        # Check 4: UTF-8 encoding
        _logger.info("Check 4: Validating UTF-8 encoding without BOM")
        validate_encoding(filename)
        _logger.debug("✓ Encoding valid")

        # Check 5: Line endings
        _logger.info("Check 5: Validating Unix LF line endings")
        validate_line_endings(filename)
        _logger.debug("✓ Line endings valid")

        # Check 6: File size
        _logger.info("Check 6: Validating file size (250-600 bytes)")
        validate_file_size(filename)
        _logger.debug("✓ File size valid")

        _logger.info("All validation checks passed")

    except (FileNotFoundError, ValueError) as e:
        _logger.error(f"Validation failed: {e}")
        raise


def git_add_file(filename: str = FILENAME) -> None:
    """Stage file for commit using git add.

    Args:
        filename: Name of file to stage (default: FILENAME)

    Raises:
        subprocess.CalledProcessError: If git add fails

    Example:
        >>> git_add_file("test-mujic0.md")
    """
    _logger.info(f"Staging file with git: {filename}")

    try:
        result = subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug(f"File staged successfully: {filename}")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Failed to stage file: {e.stderr}")
        raise


def git_commit(commit_message: str = COMMIT_MESSAGE) -> None:
    """Commit staged changes with conventional commit message.

    Args:
        commit_message: Commit message (default: COMMIT_MESSAGE)

    Raises:
        subprocess.CalledProcessError: If git commit fails

    Example:
        >>> git_commit("feat(208): Create markdown file test-mujic0.md")
    """
    _logger.info(f"Committing changes: {commit_message}")

    try:
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug(f"Commit successful: {commit_message}")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Failed to commit: {e.stderr}")
        raise


def git_push(branch_name: str = BRANCH_NAME) -> None:
    """Push commit to remote branch using git push.

    Args:
        branch_name: Branch name to push (default: BRANCH_NAME)

    Raises:
        subprocess.CalledProcessError: If git push fails

    Example:
        >>> git_push("feat/markdown-file-creation-9f7556")
    """
    _logger.info(f"Pushing to remote branch: {branch_name}")

    try:
        result = subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug(f"Push successful: {branch_name}")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Failed to push: {e.stderr}")
        raise


def main() -> int:
    """Orchestrate complete feature 208 workflow: create, validate, and git operations.

    Workflow:
    1. Create markdown file with Claude API generated content
    2. Validate file structure, encoding, line endings, sentence count, size
    3. Stage file with git add
    4. Commit file with conventional commit message
    5. Push to remote branch

    Returns:
        0 on success, 1 on any failure (fail-fast principle)

    Logs:
        - 'Starting feature 208 implementation workflow' at info level
        - Each phase (Phase 1, 2, 3) at info level
        - Success message with checkmark at info level
        - Errors at error level with exception details

    Example:
        >>> exit_code = main()  # Creates file, validates, commits, and pushes
        >>> print(exit_code)  # 0 on success, 1 on failure
    """
    _logger.info("Starting feature 208 implementation workflow")

    try:
        # Phase 1: Create markdown file
        _logger.info("Phase 1: Creating markdown file")
        file_path = create_markdown_file()
        _logger.info(f"✓ File created: {file_path}")

        # Phase 2: Validate markdown file
        _logger.info("Phase 2: Validating markdown file")
        validate_markdown_file(FILENAME)
        _logger.info("✓ File validation passed")

        # Phase 3: Git operations
        _logger.info("Phase 3: Git integration (add, commit, push)")

        _logger.info("Step 3a: Stage file with git add")
        git_add_file(FILENAME)
        _logger.info("✓ File staged")

        _logger.info("Step 3b: Commit file")
        git_commit(COMMIT_MESSAGE)
        _logger.info("✓ File committed")

        _logger.info("Step 3c: Push to remote")
        git_push(BRANCH_NAME)
        _logger.info("✓ Changes pushed to remote")

        _logger.info(f"✓ Feature 208 implementation completed successfully")
        return 0

    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as e:
        _logger.error(f"Feature 208 workflow failed: {e}")
        return 1
    except Exception as e:
        _logger.error(f"Unexpected error in feature 208 workflow: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
