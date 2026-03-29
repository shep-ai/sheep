#!/usr/bin/env python3
"""
Test execution for feature 272 phase 2 (Git Integration & Verification).

This script validates that the file is properly committed and can be pushed to remote.
It checks git state and validates the commit exists before attempting push.
"""

import sys
from pathlib import Path
import subprocess

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.observability.logging import get_logger

_logger = get_logger(__name__)

FEATURE_272_FILENAME = "test-4mg4tn.md"
FEATURE_NUMBER = 272
EXPECTED_COMMIT_MESSAGE = f"feat({FEATURE_NUMBER}): create markdown file {FEATURE_272_FILENAME} with title and prose content"


def check_file_tracked():
    """Check if the file is tracked in git."""
    try:
        result = subprocess.run(
            ["git", "ls-files", FEATURE_272_FILENAME],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
        )
        return FEATURE_272_FILENAME in result.stdout
    except Exception as e:
        _logger.error(f"Error checking git tracking: {e}")
        return False


def check_commit_exists():
    """Check if the feature commit exists in git history."""
    try:
        result = subprocess.run(
            ["git", "log", "--grep", FEATURE_272_FILENAME, "--oneline"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
        )
        return FEATURE_272_FILENAME in result.stdout
    except Exception as e:
        _logger.error(f"Error checking commit: {e}")
        return False


def check_upstream_tracking():
    """Check if the local branch has upstream tracking."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
        )
        return "origin" in result.stdout and "HEAD" not in result.stdout
    except subprocess.CalledProcessError:
        # Branch does not have upstream tracking yet
        return False
    except Exception as e:
        _logger.error(f"Error checking upstream tracking: {e}")
        return False


def check_file_exists():
    """Check if the markdown file exists."""
    file_path = Path(__file__).parent / FEATURE_272_FILENAME
    return file_path.exists()


def main():
    """Validate phase 2 git integration state."""
    _logger.info("=" * 80)
    _logger.info("Feature 272 Phase 2: Git Integration & Verification (Test Mode)")
    _logger.info("=" * 80)

    try:
        # Pre-checks
        _logger.info("\n[PRE-CHECKS] Validating git state...")

        # Check 1: File exists
        _logger.info("\n[CHECK 1] Verifying markdown file exists...")
        if check_file_exists():
            _logger.info(f"✓ File {FEATURE_272_FILENAME} exists")
        else:
            raise FileNotFoundError(f"File {FEATURE_272_FILENAME} not found")

        # Check 2: File is tracked in git
        _logger.info(f"\n[CHECK 2] Verifying {FEATURE_272_FILENAME} is tracked in git...")
        if check_file_tracked():
            _logger.info(f"✓ File is tracked in git")
        else:
            raise RuntimeError(f"File {FEATURE_272_FILENAME} is not tracked in git")

        # Check 3: Commit exists
        _logger.info(f"\n[CHECK 3] Verifying feature commit exists...")
        if check_commit_exists():
            _logger.info(f"✓ Feature commit found in git history")
        else:
            raise RuntimeError(f"Feature commit not found in git history")

        # Check 4: Upstream tracking
        _logger.info(f"\n[CHECK 4] Verifying upstream tracking...")
        if check_upstream_tracking():
            _logger.info(f"✓ Upstream tracking is enabled")
        else:
            _logger.warning(f"⚠ Upstream tracking not yet enabled (will be set by push)")

        # Summary
        _logger.info("\n" + "=" * 80)
        _logger.info("Phase 2 Validation Summary")
        _logger.info("=" * 80)
        _logger.info(f"✓ File exists: {FEATURE_272_FILENAME}")
        _logger.info(f"✓ File is git-tracked")
        _logger.info(f"✓ Commit exists in history")
        _logger.info(f"✓ Ready for push to remote")
        _logger.info("\nPhase 2 Validation Complete:")
        _logger.info(f"  - File: {FEATURE_272_FILENAME}")
        _logger.info(f"  - Tracked: Yes")
        _logger.info(f"  - Committed: Yes")
        _logger.info(f"  - Upstream: {'Enabled' if check_upstream_tracking() else 'Ready to enable'}")
        _logger.info("=" * 80)

        return 0

    except Exception as e:
        _logger.error(f"\n✗ Phase 2 validation failed: {e}")
        _logger.exception(f"Detailed error:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
