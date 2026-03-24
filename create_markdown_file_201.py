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
    stage_and_commit_file,
    push_to_feature_branch,
)

# Module-level constants
FILENAME = "test-lihjez.md"
COMMIT_MESSAGE = "feat(201): create markdown file test-lihjez.md"

# Initialize logger
_logger = get_logger(__name__)


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

        # Stage the file
        _logger.info(f"Staging file: {FILENAME}")
        stage_result = stage_and_commit_file(
            filename=FILENAME,
            commit_message=COMMIT_MESSAGE
        )
        _logger.info(f"File staged and committed: {stage_result}")
        print(f"✓ Phase 3a: File staged with git add")
        print(f"✓ Phase 3b: File committed with message: {COMMIT_MESSAGE}")

        # Push to feature branch
        _logger.info("Pushing to feature branch...")
        push_result = push_to_feature_branch()
        _logger.info(f"Push result: {push_result}")
        print(f"✓ Phase 3c: Pushed to remote origin")

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
