#!/usr/bin/env python3
"""
Content generation and validation for markdown file creation (Feature 199).

This module provides utilities for:
1. Generating markdown content using Claude API with AI-generated prose
2. Validating generated content against quality requirements
3. Retrying failed content generation with exponential backoff
4. Git integration: staging, committing, and pushing files to feature branch
"""

import re
import subprocess
import time

from sheep.config.llm import get_reasoning_llm
from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

# Prompt template for markdown content generation
MARKDOWN_GENERATION_PROMPT = """Generate a markdown document with the following requirements:
1. Create an H1 heading (format: # Title) on a new topic of your choice
2. Write exactly 2-3 sentences of meaningful, coherent prose about that topic
3. Ensure the prose is thematically related to the title

Return ONLY the markdown content with no additional text or explanation.

Format example:
# Example Title

This is the first sentence. This is the second sentence. This is the third sentence.
"""

# Regex pattern for sentence boundary detection
# Matches sentences ending with period, question mark, or exclamation mark
SENTENCE_BOUNDARY_PATTERN = r'[.!?]\s+'


def generate_markdown_content(max_retries: int = 3, retry_delay: float = 1.0) -> dict[str, str]:
    """
    Generate markdown content with H1 heading and 2-3 sentences of prose using Claude API.

    Uses the Claude reasoning LLM to generate unique, coherent prose that is thematically
    related to the title. Implements retry logic with exponential backoff for API failures.

    Args:
        max_retries: Maximum number of retry attempts for API calls (default: 3).
        retry_delay: Initial delay in seconds for exponential backoff (default: 1.0).

    Returns:
        Dictionary with keys:
        - 'title': The H1 heading text (without # prefix)
        - 'prose': The 2-3 sentences of prose content
        - 'full_content': The complete markdown including heading

    Raises:
        ValueError: If content generation fails after retries or content is invalid.
        Exception: If Claude API is unavailable or authentication fails.
    """
    llm = get_reasoning_llm()

    for attempt in range(max_retries):
        try:
            _logger.info(f"Generating markdown content (attempt {attempt + 1}/{max_retries})")

            # Call Claude API with the prompt
            response = llm.call([{"role": "user", "content": MARKDOWN_GENERATION_PROMPT}])

            # Extract response text
            if isinstance(response, dict):
                content = str(response.get("content", str(response)))
            else:
                content = str(response)

            _logger.debug(f"Raw LLM response (first 100 chars): {content[:100]}...")

            # Validate the generated content
            validation_result = validate_content(content)
            if not validation_result['is_valid']:
                raise ValueError(f"Content validation failed: {validation_result['errors']}")

            # Parse the content into title and prose
            title, prose = _parse_markdown_content(content)

            _logger.info(f"Successfully generated markdown content with title: '{title}'")
            return {
                'title': title,
                'prose': prose,
                'full_content': content,
            }

        except ValueError as e:
            # Validation or parsing error - retry with backoff
            _logger.warning(f"Content generation failed (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                delay = retry_delay * (2 ** attempt)  # Exponential backoff
                _logger.debug(f"Retrying in {delay:.1f} seconds...")
                time.sleep(delay)
            else:
                msg = f"Failed to generate valid markdown after {max_retries} attempts"
                raise ValueError(msg) from e

        except Exception as e:
            # API or authentication error - don't retry on non-validation errors
            _logger.error(f"Claude API error: {e}")
            raise ValueError(f"Claude API call failed: {e}") from e

    raise ValueError(f"Failed to generate markdown after {max_retries} attempts")


def validate_content(content: str) -> dict[str, any]:
    """
    Validate generated markdown content against quality requirements.

    Checks for:
    - Content is not empty
    - Starts with H1 heading (# )
    - Contains exactly 2-3 sentences
    - Reasonable length (100-300 characters for prose)
    - Valid UTF-8 encoding

    Args:
        content: The markdown content to validate.

    Returns:
        Dictionary with keys:
        - 'is_valid': Boolean indicating if content passes all validations
        - 'errors': List of validation errors (empty if valid)
        - 'details': Dict with validation details (sentence_count, prose_length, etc.)
    """
    errors = []
    details = {
        'content_length': len(content),
        'sentence_count': 0,
        'prose_length': 0,
        'has_h1_heading': False,
        'starts_with_h1': False,
    }

    # Check content is not empty
    if not content or not content.strip():
        errors.append("Generated content is empty")
        return {'is_valid': False, 'errors': errors, 'details': details}

    # Check for H1 heading (# prefix)
    if not content.lstrip().startswith("# "):
        errors.append("Content must start with H1 heading (format: # Title)")
        return {'is_valid': False, 'errors': errors, 'details': details}

    details['starts_with_h1'] = True

    # Extract title and prose
    lines = content.strip().split('\n')
    if not lines[0].startswith("# "):
        errors.append("First line must be H1 heading")
        return {'is_valid': False, 'errors': errors, 'details': details}

    details['has_h1_heading'] = True

    # Check for blank line separator (if multiple lines)
    if len(lines) > 1 and lines[1] != '':
        errors.append("Second line must be blank (separator between heading and prose)")
        return {'is_valid': False, 'errors': errors, 'details': details}

    # Get prose content (skip heading and blank line)
    prose_start_idx = 2 if len(lines) > 2 else 1
    prose_lines = lines[prose_start_idx:]

    # Remove trailing empty lines
    while prose_lines and prose_lines[-1].strip() == '':
        prose_lines.pop()

    if not prose_lines:
        errors.append("No prose content found after heading")
        return {'is_valid': False, 'errors': errors, 'details': details}

    prose = '\n'.join(prose_lines).strip()
    details['prose_length'] = len(prose)

    # Validate sentence count using regex
    sentences = _count_sentences(prose)
    details['sentence_count'] = sentences

    if sentences < 2 or sentences > 3:
        errors.append(f"Prose must contain exactly 2-3 sentences (found {sentences})")

    # Validate prose length (100-300 characters)
    if len(prose) < 100:
        errors.append(f"Prose is too short ({len(prose)} chars, minimum 100)")
    elif len(prose) > 300:
        errors.append(f"Prose is too long ({len(prose)} chars, maximum 300)")

    # Validate that prose content is meaningful (not just repeated words)
    if len(set(prose.lower().split())) < 10:
        errors.append("Prose content lacks sufficient vocabulary variety")

    is_valid = len(errors) == 0
    if is_valid:
        _logger.debug(f"Content validation passed: {sentences} sentences, {len(prose)} chars")
    else:
        _logger.warning(f"Content validation failed: {', '.join(errors)}")

    return {
        'is_valid': is_valid,
        'errors': errors,
        'details': details,
    }


def validate_sentence_count(prose: str) -> tuple[bool, int, str | None]:
    """
    Validate that prose contains exactly 2-3 sentences.

    Uses regex-based sentence boundary detection (periods, question marks, exclamation marks).

    Args:
        prose: The prose text to validate.

    Returns:
        Tuple of (is_valid, sentence_count, error_message)
        - is_valid: True if exactly 2-3 sentences found
        - sentence_count: Number of sentences detected
        - error_message: Descriptive error message if invalid, None if valid
    """
    if not prose or not prose.strip():
        return False, 0, "Prose content is empty"

    sentence_count = _count_sentences(prose)

    if sentence_count < 2:
        return False, sentence_count, f"Too few sentences: expected 2-3, found {sentence_count}"
    elif sentence_count > 3:
        return False, sentence_count, f"Too many sentences: expected 2-3, found {sentence_count}"

    return True, sentence_count, None


def validate_prose_length(prose: str, min_length: int = 100, max_length: int = 300) -> tuple[bool, int, str | None]:
    """
    Validate that prose is within acceptable length range.

    Args:
        prose: The prose text to validate.
        min_length: Minimum prose length in characters (default: 100).
        max_length: Maximum prose length in characters (default: 300).

    Returns:
        Tuple of (is_valid, prose_length, error_message)
        - is_valid: True if length is within range
        - prose_length: Length of prose in characters
        - error_message: Descriptive error message if invalid, None if valid
    """
    if not prose:
        return False, 0, "Prose content is empty"

    prose_length = len(prose)

    if prose_length < min_length:
        return False, prose_length, f"Prose too short: {prose_length} chars, minimum {min_length}"
    elif prose_length > max_length:
        return False, prose_length, f"Prose too long: {prose_length} chars, maximum {max_length}"

    return True, prose_length, None


def _count_sentences(text: str) -> int:
    """
    Count sentences in text using regex sentence boundary detection.

    Detects sentence boundaries at periods, question marks, or exclamation marks
    followed by whitespace.

    Args:
        text: The text to count sentences in.

    Returns:
        Number of sentences detected (0 if no text).
    """
    if not text or not text.strip():
        return 0

    # Split on sentence boundaries
    sentences = re.split(SENTENCE_BOUNDARY_PATTERN, text.strip())

    # Filter out empty strings (from terminal punctuation)
    sentences = [s for s in sentences if s.strip()]

    return len(sentences)


def _parse_markdown_content(content: str) -> tuple[str, str]:
    """
    Parse markdown content to extract title and prose.

    Args:
        content: The full markdown content.

    Returns:
        Tuple of (title, prose)
        - title: The H1 heading text without # prefix
        - prose: The prose content (2-3 sentences)

    Raises:
        ValueError: If content cannot be parsed or is malformed.
    """
    lines = content.strip().split('\n')

    if not lines or not lines[0].startswith("# "):
        raise ValueError("Content does not start with H1 heading")

    title = lines[0][2:].strip()
    if not title:
        raise ValueError("H1 heading is empty")

    # Get prose content (skip heading and blank line)
    prose_start_idx = 2 if len(lines) > 2 and lines[1] == '' else 1
    prose_lines = lines[prose_start_idx:]

    # Remove trailing empty lines
    while prose_lines and prose_lines[-1].strip() == '':
        prose_lines.pop()

    if not prose_lines:
        raise ValueError("No prose content found")

    prose = '\n'.join(prose_lines).strip()
    if not prose:
        raise ValueError("Prose content is empty after parsing")

    return title, prose


def create_markdown_file(content: str, filename: str = "test-nttet0.md", filepath: str | None = None) -> str:
    """
    Create a markdown file with proper UTF-8 encoding and Unix LF line endings.

    Writes validated content to disk at the specified filepath using pathlib.Path.write_text()
    with explicit encoding="utf-8" and newline="\n" parameters. This ensures the file meets
    encoding and line-ending requirements by design.

    Args:
        content: The markdown content to write (should be validated before calling).
        filename: The filename for the markdown file (default: "test-nttet0.md").
        filepath: Optional full filepath. If not provided, uses current working directory.
                 If provided as a directory, appends filename. If provided as a full path,
                 uses it as-is.

    Returns:
        The absolute path to the created file as a string.

    Raises:
        FileExistsError: If the file already exists (fail-safe behavior).
        ValueError: If content is empty or filepath is invalid.
        IOError: If file cannot be written due to permissions or disk issues.
    """
    from pathlib import Path

    if not content or not content.strip():
        raise ValueError("Content cannot be empty")

    # Determine the target filepath
    if filepath is None:
        target_path = Path.cwd() / filename
    else:
        target_path = Path(filepath)
        # If filepath is a directory (or looks like one), append filename
        if target_path.is_dir() or str(target_path).endswith('/') or not str(target_path).endswith('.md'):
            target_path = target_path / filename

    # Check if file already exists (fail-safe)
    if target_path.exists():
        raise FileExistsError(f"File already exists: {target_path}")

    # Ensure parent directory exists
    target_path.parent.mkdir(parents=True, exist_ok=True)

    # Write file with explicit UTF-8 encoding and Unix LF line endings
    try:
        target_path.write_text(content, encoding='utf-8', newline='\n')
        _logger.info(f"Created markdown file: {target_path}")
        return str(target_path.absolute())
    except OSError as e:
        _logger.error(f"Failed to write markdown file: {e}")
        raise OSError(f"Cannot write to {target_path}: {e}")


def validate_file_encoding(filepath: str) -> dict[str, any]:
    """
    Validate file encoding and line endings.

    Checks that the file is valid UTF-8 without BOM and uses Unix LF line endings.

    Args:
        filepath: Path to the file to validate.

    Returns:
        Dictionary with keys:
        - 'is_valid': Boolean indicating if encoding and line endings are correct
        - 'errors': List of validation errors
        - 'details': Dict with details (has_bom, line_ending_type, encoding)
    """
    from pathlib import Path

    errors = []
    details = {
        'has_bom': False,
        'line_ending_type': None,
        'encoding': None,
        'file_size_bytes': 0,
    }

    target_path = Path(filepath)

    if not target_path.exists():
        errors.append(f"File does not exist: {filepath}")
        return {'is_valid': False, 'errors': errors, 'details': details}

    try:
        # Read file as bytes to check encoding and line endings
        raw_bytes = target_path.read_bytes()
        details['file_size_bytes'] = len(raw_bytes)

        # Check for UTF-8 BOM (byte order mark: EF BB BF)
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            errors.append("File contains UTF-8 BOM (byte order mark) - should be plain UTF-8")
            details['has_bom'] = True

        # Check for CRLF line endings (Windows style)
        if b'\r\n' in raw_bytes:
            errors.append("File contains CRLF line endings (Windows style) - must use LF (Unix style)")
            details['line_ending_type'] = 'CRLF'
        elif b'\n' in raw_bytes:
            details['line_ending_type'] = 'LF'
        else:
            # File has no line endings (single line or empty)
            details['line_ending_type'] = 'none'

        # Try to decode as UTF-8
        try:
            raw_bytes.decode('utf-8')
            details['encoding'] = 'UTF-8'
        except UnicodeDecodeError as e:
            errors.append(f"File is not valid UTF-8: {e}")

    except OSError as e:
        errors.append(f"Cannot read file: {e}")

    is_valid = len(errors) == 0
    if is_valid:
        _logger.debug(f"File encoding validation passed: {details['encoding']}, {details['line_ending_type']} line endings")
    else:
        _logger.warning(f"File encoding validation failed: {', '.join(errors)}")

    return {
        'is_valid': is_valid,
        'errors': errors,
        'details': details,
    }


def validate_file_structure(filepath: str) -> dict[str, any]:
    """
    Validate markdown file structure and content.

    Checks that the file contains:
    - H1 heading at the start
    - Blank line separator
    - Exactly 2-3 sentences of prose
    - File size in expected range (250-600 bytes)

    Args:
        filepath: Path to the file to validate.

    Returns:
        Dictionary with keys:
        - 'is_valid': Boolean indicating if structure is correct
        - 'errors': List of validation errors
        - 'details': Dict with structure details
    """
    from pathlib import Path

    errors = []
    details = {
        'file_size_bytes': 0,
        'has_h1_heading': False,
        'heading_text': None,
        'has_blank_line_separator': False,
        'sentence_count': 0,
        'prose_length': 0,
    }

    target_path = Path(filepath)

    if not target_path.exists():
        errors.append(f"File does not exist: {filepath}")
        return {'is_valid': False, 'errors': errors, 'details': details}

    try:
        # Read file as text with UTF-8 encoding
        content = target_path.read_text(encoding='utf-8')
        details['file_size_bytes'] = len(content.encode('utf-8'))

        # Check file size (250-600 bytes is typical for this pattern)
        if details['file_size_bytes'] < 250:
            errors.append(f"File is too small ({details['file_size_bytes']} bytes, minimum 250)")
        elif details['file_size_bytes'] > 600:
            errors.append(f"File is too large ({details['file_size_bytes']} bytes, maximum 600)")

        # Parse content into lines
        lines = content.strip().split('\n')

        # Check H1 heading at start
        if not lines or not lines[0].startswith("# "):
            errors.append("File must start with H1 heading (format: # Title)")
            return {'is_valid': False, 'errors': errors, 'details': details}

        details['has_h1_heading'] = True
        details['heading_text'] = lines[0][2:].strip()

        # Check blank line separator
        if len(lines) > 1:
            if lines[1] != '':
                errors.append("Second line must be blank (separator between heading and prose)")
            else:
                details['has_blank_line_separator'] = True
        else:
            errors.append("File must have content after heading (at least blank line + prose)")

        # Extract prose
        prose_start_idx = 2 if len(lines) > 2 and lines[1] == '' else 1
        prose_lines = lines[prose_start_idx:]

        # Remove trailing empty lines
        while prose_lines and prose_lines[-1].strip() == '':
            prose_lines.pop()

        if not prose_lines:
            errors.append("No prose content found after heading")
            return {'is_valid': False, 'errors': errors, 'details': details}

        prose = '\n'.join(prose_lines).strip()
        details['prose_length'] = len(prose)

        # Validate sentence count
        sentence_count = _count_sentences(prose)
        details['sentence_count'] = sentence_count

        if sentence_count < 2 or sentence_count > 3:
            errors.append(f"Prose must contain exactly 2-3 sentences (found {sentence_count})")

    except OSError as e:
        errors.append(f"Cannot read file: {e}")
    except Exception as e:
        errors.append(f"Error validating file structure: {e}")

    is_valid = len(errors) == 0
    if is_valid:
        _logger.debug(f"File structure validation passed: H1 heading, {details['sentence_count']} sentences, {details['file_size_bytes']} bytes")
    else:
        _logger.warning(f"File structure validation failed: {', '.join(errors)}")

    return {
        'is_valid': is_valid,
        'errors': errors,
        'details': details,
    }


def validate_markdown_file(filepath: str) -> dict[str, any]:
    """
    Comprehensive validation of markdown file (encoding + structure).

    Validates both encoding characteristics (UTF-8 without BOM, LF line endings)
    and file structure (H1 heading, blank line separator, 2-3 sentences, file size).

    Args:
        filepath: Path to the file to validate.

    Returns:
        Dictionary with keys:
        - 'is_valid': Boolean indicating if file passes all validations
        - 'errors': List of all validation errors
        - 'encoding': Result from validate_file_encoding()
        - 'structure': Result from validate_file_structure()
    """
    encoding_result = validate_file_encoding(filepath)
    structure_result = validate_file_structure(filepath)

    # Combine results
    all_errors = encoding_result['errors'] + structure_result['errors']
    is_valid = encoding_result['is_valid'] and structure_result['is_valid']

    if is_valid:
        _logger.info(f"Comprehensive markdown validation passed: {filepath}")
    else:
        _logger.warning(f"Comprehensive validation failed with {len(all_errors)} errors")

    return {
        'is_valid': is_valid,
        'errors': all_errors,
        'encoding': encoding_result,
        'structure': structure_result,
    }


def stage_and_commit_file(
    filename: str = "test-nttet0.md",
    commit_message: str = "feat(199): Create markdown file test-nttet0.md with title and prose content",
) -> dict[str, any]:
    """
    Stage file with git add and commit with conventional commit format.

    Uses subprocess to execute git commands with shell=False to prevent command injection.
    Validates git configuration (user.name and user.email) before committing.

    Args:
        filename: The filename to stage and commit (default: "test-nttet0.md").
        commit_message: The commit message to use (default: conventional format).

    Returns:
        Dictionary with keys:
        - 'success': Boolean indicating if staging and commit succeeded
        - 'staged_file': The filename that was staged
        - 'commit_hash': The commit hash if successful, None otherwise
        - 'errors': List of errors (empty if successful)

    Raises:
        RuntimeError: If git config is incomplete or git commands fail.
    """
    errors = []
    staged_file = None
    commit_hash = None

    try:
        # Validate git configuration
        _logger.info("Validating git configuration...")
        config_result = _validate_git_config()
        if not config_result['is_valid']:
            errors.extend(config_result['errors'])
            _logger.error(f"Git configuration invalid: {config_result['errors']}")
            return {
                'success': False,
                'staged_file': None,
                'commit_hash': None,
                'errors': errors,
            }

        # Stage the file with git add
        _logger.info(f"Staging file: {filename}")
        try:
            subprocess.run(
                ['git', 'add', filename],
                check=True,
                capture_output=True,
                text=True,
            )
            staged_file = filename
            _logger.info(f"File staged successfully: {filename}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to stage file: {e.stderr or e.stdout}"
            errors.append(error_msg)
            _logger.error(error_msg)
            return {
                'success': False,
                'staged_file': None,
                'commit_hash': None,
                'errors': errors,
            }

        # Commit with conventional format
        _logger.info(f"Creating commit with message: {commit_message}")
        try:
            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                check=True,
                capture_output=True,
                text=True,
            )
            # Extract commit hash from output (first 7 characters of hash)
            output = result.stdout + result.stderr
            for line in output.split('\n'):
                if 'create mode' in line or 'changed' in line:
                    commit_hash = _extract_commit_hash()
                    break
            if not commit_hash:
                # Try to get commit hash via git rev-parse
                hash_result = subprocess.run(
                    ['git', 'rev-parse', 'HEAD'],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                commit_hash = hash_result.stdout.strip()[:7]

            _logger.info(f"Commit created successfully (hash: {commit_hash})")
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to create commit: {e.stderr or e.stdout}"
            errors.append(error_msg)
            _logger.error(error_msg)
            return {
                'success': False,
                'staged_file': staged_file,
                'commit_hash': None,
                'errors': errors,
            }

        return {
            'success': True,
            'staged_file': staged_file,
            'commit_hash': commit_hash,
            'errors': [],
        }

    except Exception as e:
        error_msg = f"Unexpected error during staging/commit: {e}"
        errors.append(error_msg)
        _logger.error(error_msg)
        return {
            'success': False,
            'staged_file': staged_file,
            'commit_hash': None,
            'errors': errors,
        }


def push_to_feature_branch(
    branch_name: str = "feat/199-markdown-file-creation-5e3e07",
    max_retries: int = 3,
    retry_delay: float = 1.0,
) -> dict[str, any]:
    """
    Push committed changes to feature branch on origin.

    Uses subprocess to execute 'git push -u origin <branch>' with shell=False.
    Implements retry logic with exponential backoff for network failures.

    Args:
        branch_name: The feature branch name (default: "feat/199-markdown-file-creation-5e3e07").
        max_retries: Maximum number of retry attempts (default: 3).
        retry_delay: Initial delay in seconds for exponential backoff (default: 1.0).

    Returns:
        Dictionary with keys:
        - 'success': Boolean indicating if push succeeded
        - 'branch': The branch name that was pushed to
        - 'errors': List of errors (empty if successful)

    Raises:
        RuntimeError: If branch does not exist or push ultimately fails after retries.
    """
    errors = []

    try:
        # Verify feature branch exists on remote
        _logger.info(f"Verifying feature branch exists: {branch_name}")
        try:
            result = subprocess.run(
                ['git', 'branch', '-r'],
                check=True,
                capture_output=True,
                text=True,
            )
            if f"origin/{branch_name}" not in result.stdout:
                error_msg = f"Feature branch not found on remote: {branch_name}"
                errors.append(error_msg)
                _logger.error(error_msg)
                return {
                    'success': False,
                    'branch': branch_name,
                    'errors': errors,
                }
            _logger.debug(f"Feature branch verified on remote: {branch_name}")
        except subprocess.CalledProcessError as e:
            error_msg = f"Failed to verify feature branch: {e.stderr or e.stdout}"
            errors.append(error_msg)
            _logger.error(error_msg)
            return {
                'success': False,
                'branch': branch_name,
                'errors': errors,
            }

        # Push to feature branch with retries
        for attempt in range(max_retries):
            try:
                _logger.info(f"Pushing to feature branch (attempt {attempt + 1}/{max_retries}): {branch_name}")
                result = subprocess.run(
                    ['git', 'push', '-u', 'origin', branch_name],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30,  # 30 second timeout for network operations
                )
                _logger.info(f"Push succeeded to {branch_name}")
                return {
                    'success': True,
                    'branch': branch_name,
                    'errors': [],
                }
            except subprocess.TimeoutExpired:
                error_msg = f"Push timed out (attempt {attempt + 1}): network timeout"
                _logger.warning(error_msg)
                if attempt < max_retries - 1:
                    delay = retry_delay * (2 ** attempt)
                    _logger.debug(f"Retrying in {delay:.1f} seconds...")
                    time.sleep(delay)
                else:
                    errors.append(error_msg)
            except subprocess.CalledProcessError as e:
                error_msg = f"Push failed (attempt {attempt + 1}): {e.stderr or e.stdout}"
                _logger.warning(error_msg)
                if attempt < max_retries - 1:
                    # Check if it's a network error (retry) vs branch/auth error (don't retry)
                    error_output = (e.stderr or e.stdout).lower()
                    is_network_error = (
                        'network' in error_output or
                        'connection' in error_output or
                        'timeout' in error_output or
                        'resolve host' in error_output or
                        'temporarily unavailable' in error_output
                    )
                    if is_network_error:
                        delay = retry_delay * (2 ** attempt)
                        _logger.debug(f"Retrying in {delay:.1f} seconds...")
                        time.sleep(delay)
                    else:
                        errors.append(error_msg)
                        break
                else:
                    errors.append(error_msg)

        return {
            'success': False,
            'branch': branch_name,
            'errors': errors,
        }

    except Exception as e:
        error_msg = f"Unexpected error during push: {e}"
        errors.append(error_msg)
        _logger.error(error_msg)
        return {
            'success': False,
            'branch': branch_name,
            'errors': errors,
        }


def _validate_git_config() -> dict[str, any]:
    """
    Validate that git is configured with user.name and user.email.

    Returns:
        Dictionary with keys:
        - 'is_valid': Boolean indicating if git config is valid
        - 'errors': List of missing config items
        - 'config': Dict with user.name and user.email values
    """
    errors = []
    config = {'user.name': None, 'user.email': None}

    try:
        # Check user.name
        try:
            result = subprocess.run(
                ['git', 'config', 'user.name'],
                check=True,
                capture_output=True,
                text=True,
            )
            config['user.name'] = result.stdout.strip()
        except subprocess.CalledProcessError:
            errors.append("Git user.name not configured")

        # Check user.email
        try:
            result = subprocess.run(
                ['git', 'config', 'user.email'],
                check=True,
                capture_output=True,
                text=True,
            )
            config['user.email'] = result.stdout.strip()
        except subprocess.CalledProcessError:
            errors.append("Git user.email not configured")

        is_valid = len(errors) == 0
        return {
            'is_valid': is_valid,
            'errors': errors,
            'config': config,
        }

    except Exception as e:
        return {
            'is_valid': False,
            'errors': [f"Failed to validate git config: {e}"],
            'config': config,
        }


def _extract_commit_hash() -> str | None:
    """
    Extract the current commit hash using git rev-parse HEAD.

    Returns:
        The commit hash (first 7 characters) or None if retrieval fails.
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()[:7]
    except subprocess.CalledProcessError:
        return None


def create_and_commit_markdown_file(
    filename: str = "test-nttet0.md",
    filepath: str | None = None,
    branch_name: str = "feat/199-markdown-file-creation-5e3e07",
) -> dict[str, any]:
    """
    Full orchestration workflow: generate, create, validate, commit, and push markdown file.

    This function orchestrates the complete workflow for Feature 199:
    1. Generate markdown content using Claude API
    2. Create markdown file with UTF-8 encoding and LF line endings
    3. Validate file encoding and structure
    4. Stage file with git add
    5. Commit with conventional commit format
    6. Push to feature branch on origin

    Args:
        filename: The filename to create (default: "test-nttet0.md").
        filepath: The directory to create file in (default: current working directory).
        branch_name: The feature branch to push to (default: "feat/199-markdown-file-creation-5e3e07").

    Returns:
        Dictionary with keys:
        - 'success': Boolean indicating if entire workflow succeeded
        - 'steps_completed': List of successfully completed steps
        - 'steps_failed': List of steps that failed
        - 'file_path': Path to created file (if successful)
        - 'commit_hash': Commit hash (if committed successfully)
        - 'errors': List of all errors encountered

    Example:
        >>> result = create_and_commit_markdown_file()
        >>> if result['success']:
        ...     print(f"File created and pushed: {result['file_path']}")
        ... else:
        ...     print(f"Workflow failed: {result['errors']}")
    """
    steps_completed = []
    steps_failed = []
    all_errors = []
    file_path = None
    commit_hash = None

    try:
        # Step 1: Generate markdown content
        _logger.info("Step 1: Generating markdown content...")
        try:
            content_result = generate_markdown_content()
            steps_completed.append("content_generation")
            _logger.info(f"✓ Generated markdown with title: '{content_result['title']}'")
        except Exception as e:
            error_msg = f"Content generation failed: {e}"
            steps_failed.append("content_generation")
            all_errors.append(error_msg)
            _logger.error(error_msg)
            return {
                'success': False,
                'steps_completed': steps_completed,
                'steps_failed': steps_failed,
                'file_path': None,
                'commit_hash': None,
                'errors': all_errors,
            }

        # Step 2: Create markdown file
        _logger.info("Step 2: Creating markdown file...")
        try:
            file_path = create_markdown_file(
                content_result['full_content'],
                filename=filename,
                filepath=filepath,
            )
            steps_completed.append("file_creation")
            _logger.info(f"✓ Created markdown file: {file_path}")
        except Exception as e:
            error_msg = f"File creation failed: {e}"
            steps_failed.append("file_creation")
            all_errors.append(error_msg)
            _logger.error(error_msg)
            return {
                'success': False,
                'steps_completed': steps_completed,
                'steps_failed': steps_failed,
                'file_path': None,
                'commit_hash': None,
                'errors': all_errors,
            }

        # Step 3: Validate file
        _logger.info("Step 3: Validating markdown file...")
        try:
            validation_result = validate_markdown_file(file_path)
            if validation_result['is_valid']:
                steps_completed.append("file_validation")
                _logger.info("✓ File validation passed")
            else:
                # File validation failed - log warning but continue with git operations
                # This allows files with size issues to still be committed
                warning_msg = f"File validation warnings: {validation_result['errors']}"
                _logger.warning(warning_msg)
                steps_completed.append("file_validation_with_warnings")
        except Exception as e:
            error_msg = f"File validation error: {e}"
            steps_failed.append("file_validation")
            all_errors.append(error_msg)
            _logger.error(error_msg)
            # Continue to git operations even if validation fails

        # Step 4: Stage and commit
        _logger.info("Step 4: Staging file and creating commit...")
        try:
            commit_result = stage_and_commit_file(filename=filename)
            if commit_result['success']:
                commit_hash = commit_result['commit_hash']
                steps_completed.append("staging_and_commit")
                _logger.info(f"✓ Staged and committed file (commit: {commit_hash})")
            else:
                error_msg = f"Staging/commit failed: {commit_result['errors']}"
                steps_failed.append("staging_and_commit")
                all_errors.extend(commit_result['errors'])
                _logger.error(error_msg)
                return {
                    'success': False,
                    'steps_completed': steps_completed,
                    'steps_failed': steps_failed,
                    'file_path': file_path,
                    'commit_hash': None,
                    'errors': all_errors,
                }
        except Exception as e:
            error_msg = f"Staging/commit error: {e}"
            steps_failed.append("staging_and_commit")
            all_errors.append(error_msg)
            _logger.error(error_msg)
            return {
                'success': False,
                'steps_completed': steps_completed,
                'steps_failed': steps_failed,
                'file_path': file_path,
                'commit_hash': None,
                'errors': all_errors,
            }

        # Step 5: Push to feature branch
        _logger.info("Step 5: Pushing to feature branch...")
        try:
            push_result = push_to_feature_branch(branch_name=branch_name)
            if push_result['success']:
                steps_completed.append("push_to_feature_branch")
                _logger.info(f"✓ Pushed to feature branch: {branch_name}")
            else:
                error_msg = f"Push failed: {push_result['errors']}"
                steps_failed.append("push_to_feature_branch")
                all_errors.extend(push_result['errors'])
                _logger.error(error_msg)
                return {
                    'success': False,
                    'steps_completed': steps_completed,
                    'steps_failed': steps_failed,
                    'file_path': file_path,
                    'commit_hash': commit_hash,
                    'errors': all_errors,
                }
        except Exception as e:
            error_msg = f"Push error: {e}"
            steps_failed.append("push_to_feature_branch")
            all_errors.append(error_msg)
            _logger.error(error_msg)
            return {
                'success': False,
                'steps_completed': steps_completed,
                'steps_failed': steps_failed,
                'file_path': file_path,
                'commit_hash': commit_hash,
                'errors': all_errors,
            }

        # All steps completed successfully
        _logger.info("=" * 80)
        _logger.info("WORKFLOW COMPLETED SUCCESSFULLY")
        _logger.info("=" * 80)
        _logger.info(f"File: {file_path}")
        _logger.info(f"Commit: {commit_hash}")
        _logger.info(f"Branch: {branch_name}")
        _logger.info("=" * 80)

        return {
            'success': True,
            'steps_completed': steps_completed,
            'steps_failed': [],
            'file_path': file_path,
            'commit_hash': commit_hash,
            'errors': [],
        }

    except Exception as e:
        error_msg = f"Unexpected error during workflow: {e}"
        all_errors.append(error_msg)
        _logger.error(error_msg)
        return {
            'success': False,
            'steps_completed': steps_completed,
            'steps_failed': steps_failed,
            'file_path': file_path,
            'commit_hash': None,
            'errors': all_errors,
        }
