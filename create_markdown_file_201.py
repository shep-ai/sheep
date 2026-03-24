#!/usr/bin/env python3
"""
Implementation script for feature 201: markdown-file-creation-906d94
Creates test-lihjez.md with proper markdown structure and validation.

This script executes the complete workflow:
1. Generate markdown content using Claude API
2. Create markdown file with UTF-8 encoding and LF line endings
3. Validate file encoding, structure, and size constraints
4. Stage file with git add
5. Commit with conventional commit format
6. Push to feature branch on origin
"""

import sys
import subprocess
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from sheep.observability.logging import get_logger
from src.create_markdown import (
    generate_markdown_content,
    create_markdown_file,
    validate_markdown_file,
)

# Module-level constants
FILENAME = "test-lihjez.md"
COMMIT_MESSAGE = "feat(201): create markdown file test-lihjez.md"

# Initialize logger
_logger = get_logger(__name__)


def git_add(filename: str) -> dict:
    """
    Stage a file using 'git add'.

    Args:
        filename: The filename to stage

    Returns:
        Dictionary with keys:
        - 'success': Boolean indicating if add succeeded
        - 'filename': The filename that was staged
        - 'error': Error message if failed, None if successful
    """
    _logger.info(f"Staging file with git add: {filename}")
    try:
        result = subprocess.run(
            ['git', 'add', filename],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"File staged successfully: {filename}")
        return {
            'success': True,
            'filename': filename,
            'error': None,
        }
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to stage file: {e.stderr or e.stdout}"
        _logger.error(error_msg)
        return {
            'success': False,
            'filename': filename,
            'error': error_msg,
        }


def git_commit(filename: str, commit_message: str) -> dict:
    """
    Create a commit with the specified message.

    Args:
        filename: The filename being committed (for logging)
        commit_message: The commit message to use

    Returns:
        Dictionary with keys:
        - 'success': Boolean indicating if commit succeeded
        - 'commit_hash': The commit hash (short form) if successful, None otherwise
        - 'error': Error message if failed, None if successful
    """
    _logger.info(f"Creating commit with message: {commit_message}")
    try:
        result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            check=True,
            capture_output=True,
            text=True,
        )
        # Get the commit hash
        try:
            hash_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                check=True,
                capture_output=True,
                text=True,
            )
            commit_hash = hash_result.stdout.strip()[:7]
        except subprocess.CalledProcessError:
            commit_hash = None

        _logger.info(f"Commit created successfully (hash: {commit_hash})")
        return {
            'success': True,
            'commit_hash': commit_hash,
            'error': None,
        }
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to create commit: {e.stderr or e.stdout}"
        _logger.error(error_msg)
        return {
            'success': False,
            'commit_hash': None,
            'error': error_msg,
        }


def git_push(branch_name: str) -> dict:
    """
    Push commits to the feature branch on origin.

    Args:
        branch_name: The branch name to push to

    Returns:
        Dictionary with keys:
        - 'success': Boolean indicating if push succeeded
        - 'branch': The branch name
        - 'error': Error message if failed, None if successful
    """
    _logger.info(f"Pushing to feature branch: {branch_name}")
    try:
        result = subprocess.run(
            ['git', 'push', '-u', 'origin', branch_name],
            check=True,
            capture_output=True,
            text=True,
        )
        _logger.info(f"Push succeeded to {branch_name}")
        return {
            'success': True,
            'branch': branch_name,
            'error': None,
        }
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to push to {branch_name}: {e.stderr or e.stdout}"
        _logger.error(error_msg)
        return {
            'success': False,
            'branch': branch_name,
            'error': error_msg,
        }


def git_workflow(filename: str, commit_message: str, branch_name: str) -> dict:
    """
    Execute complete git workflow: add, commit, push.

    Args:
        filename: The filename to stage and commit
        commit_message: The commit message to use
        branch_name: The branch name to push to

    Returns:
        Dictionary with keys:
        - 'success': Boolean indicating if entire workflow succeeded
        - 'errors': List of error messages (empty if successful)
    """
    _logger.info("Starting git workflow: add, commit, push")
    errors = []

    # Stage file
    add_result = git_add(filename)
    if not add_result['success']:
        errors.append(add_result['error'])
        return {'success': False, 'errors': errors}

    # Commit
    commit_result = git_commit(filename, commit_message)
    if not commit_result['success']:
        errors.append(commit_result['error'])
        return {'success': False, 'errors': errors}

    # Push
    push_result = git_push(branch_name)
    if not push_result['success']:
        errors.append(push_result['error'])
        return {'success': False, 'errors': errors}

    _logger.info("Git workflow completed successfully")
    return {'success': True, 'errors': []}


def main():
    """
    Main entry point: orchestrate complete workflow.

    Executes the full feature 201 workflow:
    1. Phase 1: Generate markdown content using Claude API
    2. Phase 2: Create and validate markdown file with proper encoding and line endings
    3. Phase 3: Git integration (add, commit, push)

    Returns:
        0 on success, 1 on failure
    """
    _logger.info("Starting Feature 201: Markdown File Creation Workflow")
    _logger.info("=" * 80)

    try:
        # Phase 1: Content generation
        _logger.info("Phase 1: Generating markdown content using Claude API...")
        content_result = generate_markdown_content(max_retries=3, retry_delay=1.0)
        _logger.info(f"Successfully generated content with title: {content_result['title']}")
        _logger.debug(f"Generated prose: {content_result['prose']}")

        print("\n" + "=" * 60)
        print("Feature 201: Markdown File Creation")
        print("=" * 60)
        print("✓ Phase 1: Content generated successfully")
        print(f"  Title: {content_result['title']}")
        print(f"  Prose length: {len(content_result['prose'])} characters")

        # Phase 2: File creation and validation
        _logger.info("Phase 2: Creating markdown file with proper encoding and validation...")

        # Check for pre-existing file
        if Path(FILENAME).exists():
            raise FileExistsError(f"File already exists: {FILENAME}")

        # Create the markdown file with UTF-8 encoding and LF line endings
        full_content = content_result['full_content']
        filepath = create_markdown_file(
            content=full_content,
            filename=FILENAME,
            filepath=None  # Use current working directory
        )
        _logger.info(f"File created successfully: {filepath}")
        print(f"✓ Phase 2a: File created with UTF-8 encoding and LF line endings")

        # Validate the created file
        _logger.info("Phase 2b: Validating markdown file...")
        validation_result = validate_markdown_file(filepath)

        if not validation_result['is_valid']:
            error_messages = '\n  '.join(validation_result['errors'])
            raise ValueError(f"File validation failed:\n  {error_messages}")

        _logger.info(f"File validation passed for: {filepath}")
        print(f"✓ Phase 2b: File validation passed")
        print(f"  - Encoding: UTF-8 without BOM ✓")
        print(f"  - Line endings: LF only ✓")
        print(f"  - Structure: H1 heading, blank line, prose, final newline ✓")
        print(f"  - Sentence count: 2-3 sentences ✓")
        print(f"  - File size: {Path(filepath).stat().st_size} bytes (400-600 range) ✓")

        # Phase 3: Git integration
        _logger.info("Phase 3: Git integration (add, commit, push)...")

        # Get current branch name for pushing
        try:
            branch_result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                check=True,
                capture_output=True,
                text=True,
            )
            current_branch = branch_result.stdout.strip()
            _logger.info(f"Current branch: {current_branch}")
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(
                e.returncode,
                e.cmd,
                output=f"Failed to get current branch: {e.stderr or e.stdout}"
            )

        # Execute git workflow
        workflow_result = git_workflow(
            filename=FILENAME,
            commit_message=COMMIT_MESSAGE,
            branch_name=current_branch
        )

        if not workflow_result['success']:
            error_messages = '\n  '.join(workflow_result['errors'])
            raise subprocess.CalledProcessError(
                1,
                'git workflow',
                output=f"Git workflow failed:\n  {error_messages}"
            )

        print(f"✓ Phase 3a: File staged with git add")
        print(f"✓ Phase 3b: File committed with message: {COMMIT_MESSAGE}")
        print(f"✓ Phase 3c: Pushed to remote origin ({current_branch})")

        # Success
        print("\n" + "=" * 60)
        print("Successfully completed Feature 201")
        print(f"File {FILENAME} has been created, validated, staged, committed, and pushed.")
        print("=" * 60)

        return 0

    except FileExistsError as e:
        _logger.error(f"File already exists: {e}")
        print(f"✗ File creation failed: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        _logger.error(f"Validation or content generation failed: {e}")
        print(f"✗ Validation failed: {e}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        _logger.error(f"Git command failed: {e.cmd}")
        print(f"✗ Git command failed: {e.cmd}", file=sys.stderr)
        if e.stderr:
            print(f"  Error: {e.stderr}", file=sys.stderr)
        return 1
    except OSError as e:
        _logger.error(f"File I/O error: {e}")
        print(f"✗ File I/O error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        _logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
