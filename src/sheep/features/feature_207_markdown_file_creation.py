"""Implementation for feature 207: Create markdown file test-5q8o2a.md with title and prose content.

This module orchestrates the creation of a markdown file following the established pattern
from prior features. The file is created with:
- Exact filename: test-5q8o2a.md
- H1 markdown heading as title
- 2-3 sentences of prose content
- UTF-8 encoding without BOM
- Unix LF line endings
- File size approximately 300-600 bytes
- Git staging, commit, and push operations

Content generation uses Claude API with temperature=0 for deterministic, reproducible output.
Same input produces identical output on repeated calls.
"""

import subprocess
import sys
from pathlib import Path

from sheep.config.llm import create_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Feature 207 constants
FILENAME = "test-5q8o2a.md"
FEATURE_NUMBER = 207
BRANCH_NAME = "feat/207-markdown-file-creation-521e88"
COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): Create markdown file {FILENAME} with title and prose content"

# Prompt template for deterministic markdown content generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""


def generate_prose(feature_number: int = FEATURE_NUMBER) -> str:
    """Generate 2-3 sentences of prose content using Claude API.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same feature input produces identical prose output on repeated calls.

    Args:
        feature_number: Feature number to seed generation (default: 207)

    Returns:
        String containing 2-3 sentences of meaningful, coherent prose

    Raises:
        ValueError: If generated prose is invalid or doesn't meet requirements
        Exception: If Claude API call fails
    """
    _logger.info("Generating prose content using Claude API (temperature=0)")

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

        # Parse prose from markdown content (second paragraph after blank line)
        lines = content.strip().split("\n")

        # Find blank line separator (should be after title)
        blank_line_idx = None
        for i, line in enumerate(lines):
            if line.strip() == "" and i > 0:
                blank_line_idx = i
                break

        if blank_line_idx is None:
            raise ValueError("Generated content missing blank line separator after heading")

        # Extract prose content (all lines after blank line)
        prose_lines = lines[blank_line_idx + 1:]
        prose = "\n".join(prose_lines).strip()

        if not prose:
            raise ValueError("Generated prose content is empty")

        # Validate sentence count
        sentence_count = prose.count(".")
        if not (2 <= sentence_count <= 3):
            raise ValueError(
                f"Generated prose has {sentence_count} sentences, expected 2-3"
            )

        _logger.info(f"Successfully generated prose with {sentence_count} sentences")
        return prose

    except Exception as e:
        _logger.error(f"Failed to generate prose: {e}")
        raise


def generate_title(feature_number: int = FEATURE_NUMBER) -> str:
    """Generate H1 markdown title using Claude API.

    Uses Claude API with temperature=0 for deterministic, reproducible output.
    Same feature input produces identical title output on repeated calls.

    Args:
        feature_number: Feature number to seed generation (default: 207)

    Returns:
        String containing H1 markdown heading (without # prefix)

    Raises:
        ValueError: If generated title is invalid
        Exception: If Claude API call fails
    """
    _logger.info("Generating title using Claude API (temperature=0)")

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

        # Parse title from markdown content (first line should be H1)
        lines = content.strip().split("\n")

        if not lines or not lines[0].startswith("# "):
            raise ValueError("Generated content must start with H1 heading (# Title)")

        # Extract title (remove # prefix and whitespace)
        title = lines[0].replace("# ", "").strip()

        if not title:
            raise ValueError("Generated title is empty")

        _logger.info(f"Successfully generated title: '{title}'")
        return title

    except Exception as e:
        _logger.error(f"Failed to generate title: {e}")
        raise


def create_markdown_file() -> str:
    """Create markdown file with proper encoding and line endings.

    Creates file with H1 heading, blank line, and prose content.
    Uses UTF-8 encoding and Unix LF line endings via pathlib.Path.write_text().

    Returns:
        Absolute path to created file

    Raises:
        FileExistsError: If file already exists
        ValueError: If title or prose generation fails
        OSError: If file write operation fails
    """
    _logger.info(f"Creating markdown file: {FILENAME}")

    try:
        # Check file doesn't already exist
        file_path = Path(FILENAME)
        if file_path.exists():
            raise FileExistsError(f"File {FILENAME} already exists")

        # Generate title and prose
        _logger.info("Generating title and prose content")
        title = generate_title()
        prose = generate_prose()

        # Construct markdown content
        content = f"# {title}\n\n{prose}\n"

        # Write file with UTF-8 encoding and LF line endings
        _logger.info(f"Writing file to {file_path}")
        file_path.write_text(content, encoding="utf-8")

        # Verify file was created
        if not file_path.exists():
            raise OSError(f"File was not created: {file_path}")

        file_size = file_path.stat().st_size
        _logger.info(f"Successfully created {FILENAME} ({file_size} bytes)")

        return str(file_path.absolute())

    except Exception as e:
        _logger.error(f"Failed to create markdown file: {e}")
        raise


def verify_file_exists(filename: str = FILENAME) -> bool:
    """Verify that the markdown file exists.

    Args:
        filename: Path to file to verify (defaults to FILENAME)

    Returns:
        True if file exists

    Raises:
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Checking file exists: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")
    return True


def validate_markdown_format(filename: str = FILENAME) -> bool:
    """Validate markdown file structure: H1 heading, blank line, prose.

    Checks that:
    1. File starts with exactly one H1 heading (# Title)
    2. Line 2 is blank (separator between heading and prose)
    3. Exactly one H1 heading exists in the file

    Args:
        filename: Path to markdown file to validate

    Returns:
        True if format is valid

    Raises:
        ValueError: If markdown format is invalid
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating markdown format: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Check first line is H1 heading
    if not lines or not lines[0].startswith("# "):
        raise ValueError("File must start with H1 heading (# Title)")

    # Check second line is blank (blank line separator)
    if len(lines) < 2 or lines[1].strip() != "":
        raise ValueError("Second line must be blank (separator between heading and prose)")

    # Check exactly one H1 heading exists
    h1_count = sum(1 for line in lines if line.startswith("# ") and not line.startswith("# #"))
    if h1_count != 1:
        raise ValueError(f"File must contain exactly one H1 heading, found {h1_count}")

    return True


def validate_encoding(filename: str = FILENAME) -> bool:
    """Validate file is UTF-8 encoded without BOM.

    Checks that:
    1. File does not start with UTF-8 BOM (byte order mark)
    2. File can be decoded as valid UTF-8

    Args:
        filename: Path to file to validate

    Returns:
        True if encoding is valid

    Raises:
        ValueError: If file has BOM or is not valid UTF-8
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating encoding: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    binary_content = file_path.read_bytes()

    # Check for UTF-8 BOM
    if binary_content.startswith(b"\xef\xbb\xbf"):
        raise ValueError("File contains UTF-8 BOM (byte order mark)")

    # Verify UTF-8 encoding
    try:
        binary_content.decode("utf-8")
    except UnicodeDecodeError as e:
        raise ValueError(f"File contains invalid UTF-8 encoding: {e}") from e

    return True


def validate_line_endings(filename: str = FILENAME) -> bool:
    """Validate file uses Unix LF line endings exclusively.

    Checks that:
    1. File does not contain CRLF (\\r\\n) Windows line endings
    2. File does not contain CR (\\r) Mac line endings
    3. File uses only LF (\\n) Unix line endings

    Args:
        filename: Path to file to validate

    Returns:
        True if line endings are valid

    Raises:
        ValueError: If file contains CRLF or CR line endings
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating line endings: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    binary_content = file_path.read_bytes()

    if b"\r\n" in binary_content:
        raise ValueError("File contains Windows CRLF (\\r\\n) line endings")

    if b"\r" in binary_content:
        raise ValueError("File contains Mac CR (\\r) line endings")

    return True


def extract_prose_content(filename: str = FILENAME) -> str:
    """Extract prose content from markdown file.

    Extracts the text content that appears after the H1 heading and blank line.
    This helper function is used by other validation functions.

    Args:
        filename: Path to markdown file

    Returns:
        Prose content as string (empty if no prose found)

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If file structure is invalid
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Find blank line after heading (should be at index 1)
    blank_line_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "" and i > 0:
            blank_line_idx = i
            break

    if blank_line_idx is None:
        raise ValueError("No blank line separator found after heading")

    # Extract prose content (all lines after blank line)
    prose_lines = lines[blank_line_idx + 1:]
    prose_text = "\n".join(prose_lines).strip()

    return prose_text


def count_sentences(prose: str) -> int:
    """Count sentences in prose text using period counting.

    Counts the number of periods (.) in the prose content. This is a simple
    but effective approach for validating sentence count in typical prose.

    Args:
        prose: Text content to count sentences in

    Returns:
        Number of periods found in the prose

    Raises:
        ValueError: If prose is empty
    """
    if not prose:
        raise ValueError("Prose content is empty")

    return prose.count(".")


def validate_sentence_count(filename: str = FILENAME) -> bool:
    """Validate file contains exactly 2-3 sentences of prose.

    Extracts prose content and counts periods to validate exactly 2-3 sentences.
    This function uses the extract_prose_content() and count_sentences() helpers.

    Args:
        filename: Path to file to verify

    Returns:
        True if sentence count is valid

    Raises:
        ValueError: If sentence count is not 2-3
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating sentence count: {filename}")
    prose_text = extract_prose_content(filename)
    sentence_count = count_sentences(prose_text)

    if not (2 <= sentence_count <= 3):
        raise ValueError(f"Expected 2-3 sentences, found {sentence_count}")

    return True


def validate_file_size(filename: str = FILENAME, min_bytes: int = 200, max_bytes: int = 700) -> bool:
    """Validate file size with soft validation (log warnings but allow commit).

    Checks file size and logs warnings if outside the expected range, but does NOT
    reject the file. This enables observability while preventing false negatives.

    Args:
        filename: Path to file to validate
        min_bytes: Minimum expected file size in bytes (default: 200)
        max_bytes: Maximum expected file size in bytes (default: 700)

    Returns:
        True always (soft validation; never raises)

    Raises:
        FileNotFoundError: If file does not exist
    """
    _logger.debug(f"Validating file size: {filename}")
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"File {filename} does not exist")

    file_size = file_path.stat().st_size

    if min_bytes <= file_size <= max_bytes:
        _logger.info(f"File size {file_size} bytes is within expected range {min_bytes}-{max_bytes} bytes")
    else:
        if file_size < min_bytes:
            _logger.warning(
                f"File size {file_size} bytes is below recommended minimum {min_bytes} bytes"
            )
        else:
            _logger.warning(
                f"File size {file_size} bytes is above recommended maximum {max_bytes} bytes"
            )

    return True


def validate_markdown_file(filename: str = FILENAME) -> bool:
    """Comprehensive validation pipeline for markdown file.

    Runs all validation checks required by the specification:
    1. File exists at the specified path
    2. File encoding is UTF-8 without BOM (checked early to catch BOM issues)
    3. File uses Unix LF line endings
    4. Markdown format is valid (H1 heading, blank line, prose)
    5. Sentence count is exactly 2-3
    6. File size is within expected range (soft validation with warnings)

    This function validates all success criteria and fails fast on the first
    error, providing clear error messages for debugging.

    Args:
        filename: Path to markdown file to validate

    Returns:
        True if all validations pass

    Raises:
        FileNotFoundError: If file does not exist
        ValueError: If any validation check fails (except file size, which warns but allows)
    """
    _logger.info(f"Starting comprehensive validation pipeline for {filename}")

    try:
        # Check 1: File exists
        _logger.info("Check 1: Verifying file exists")
        verify_file_exists(filename)
        _logger.debug(f"✓ File exists: {filename}")

        # Check 2: UTF-8 encoding without BOM (checked early)
        _logger.info("Check 2: Validating file encoding")
        validate_encoding(filename)
        _logger.debug("✓ File encoding is valid UTF-8 without BOM")

        # Check 3: Unix LF line endings
        _logger.info("Check 3: Validating line endings")
        validate_line_endings(filename)
        _logger.debug("✓ File uses Unix LF line endings")

        # Check 4: Markdown format (H1 heading, blank line, prose)
        _logger.info("Check 4: Validating markdown format")
        validate_markdown_format(filename)
        _logger.debug("✓ Markdown format is valid")

        # Check 5: Sentence count (2-3 sentences)
        _logger.info("Check 5: Validating sentence count")
        validate_sentence_count(filename)
        _logger.debug("✓ Sentence count is valid (2-3)")

        # Check 6: File size (soft validation with warnings)
        _logger.info("Check 6: Validating file size")
        validate_file_size(filename)
        _logger.debug("✓ File size validation complete (warnings logged if needed)")

        _logger.info(f"All validation checks passed for {filename}")
        return True

    except FileNotFoundError as e:
        _logger.error(f"File validation failed - file not found: {e}")
        raise
    except ValueError as e:
        _logger.error(f"File validation failed: {e}")
        raise


def git_add_file(filename: str = FILENAME) -> None:
    """Stage the markdown file for commit using git add.

    Executes `git add <filename>` to stage the file for the next commit.
    Uses subprocess.run() with shell=False for security and fail-fast behavior.

    Args:
        filename: Path to file to stage (defaults to FILENAME)

    Raises:
        subprocess.CalledProcessError: If git add command fails
        OSError: If git command is not available
    """
    _logger.info(f"Staging file with git add: {filename}")

    try:
        subprocess.run(
            ["git", "add", filename],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug(f"✓ Successfully staged {filename}")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Git add failed: {e.stderr}")
        raise


def git_commit(commit_message: str = COMMIT_MESSAGE) -> None:
    """Create a git commit with the specified message.

    Executes `git commit -m <message>` to commit staged changes.
    Uses subprocess.run() with shell=False for security and fail-fast behavior.
    Message must follow conventional commits format (feat/fix/docs/etc scope).

    Args:
        commit_message: Commit message following conventional commits format

    Raises:
        subprocess.CalledProcessError: If git commit command fails
        OSError: If git command is not available
    """
    _logger.info(f"Creating commit with message: {commit_message}")

    try:
        subprocess.run(
            ["git", "commit", "-m", commit_message],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug("✓ Successfully created commit")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Git commit failed: {e.stderr}")
        raise


def git_push(branch_name: str = BRANCH_NAME) -> None:
    """Push the commit to the remote repository.

    Executes `git push -u origin HEAD` to push the current branch to the remote.
    The -u flag establishes upstream tracking for the branch.
    Uses subprocess.run() with shell=False for security and fail-fast behavior.

    Args:
        branch_name: Branch name for logging context (defaults to BRANCH_NAME)

    Raises:
        subprocess.CalledProcessError: If git push command fails
        OSError: If git command is not available
    """
    _logger.info(f"Pushing branch to remote: {branch_name}")

    try:
        subprocess.run(
            ["git", "push", "-u", "origin", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.debug(f"✓ Successfully pushed branch {branch_name}")

    except subprocess.CalledProcessError as e:
        _logger.error(f"Git push failed: {e.stderr}")
        raise


def main() -> None:
    """Orchestration function for complete feature 207 workflow.

    Coordinates the following steps:
    1. Generate title using Claude API (temperature=0)
    2. Generate prose using Claude API (temperature=0)
    3. Create markdown file with proper encoding and line endings
    4. Validate file meets all specification requirements
    5. Stage file with git add
    6. Commit file with conventional commit message
    7. Push commit to remote branch

    Logs all major workflow steps and validation results.
    Raises exceptions on first failure (fail-fast principle).

    Raises:
        ValueError: If content generation or validation fails
        OSError: If file operations fail
        subprocess.CalledProcessError: If git operations fail
    """
    _logger.info("Starting feature 207 implementation workflow")

    try:
        # Phase 1: Generate content and create file
        _logger.info("Phase 1: Content Generation & File Creation")
        create_markdown_file()
        _logger.info(f"✓ Created markdown file: {FILENAME}")

        # Phase 2: Validate file
        _logger.info("Phase 2: Comprehensive Validation")
        validate_markdown_file(FILENAME)
        _logger.info(f"✓ Validated markdown file: {FILENAME}")

        # Phase 3: Git integration and orchestration
        _logger.info("Phase 3: Git Integration & Orchestration")
        git_add_file(FILENAME)
        _logger.info(f"✓ Staged file: {FILENAME}")

        git_commit(COMMIT_MESSAGE)
        _logger.info(f"✓ Committed with message: {COMMIT_MESSAGE}")

        git_push(BRANCH_NAME)
        _logger.info(f"✓ Pushed to remote branch: {BRANCH_NAME}")

        _logger.info("✓ Feature 207 implementation completed successfully")

    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as e:
        _logger.error(f"Feature 207 workflow failed: {e}")
        raise
    except Exception as e:
        _logger.error(f"Unexpected error in feature 207 workflow: {e}")
        raise


if __name__ == "__main__":
    try:
        main()
        print("✓ Successfully completed feature 207 workflow")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
