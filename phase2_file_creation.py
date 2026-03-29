#!/usr/bin/env python3
"""
Phase 2 Implementation: File Creation and Validation for Feature 271

This script demonstrates Phase 2 of the feature 271 implementation:
- Generate markdown content via Claude API
- Write to test-y1zgop.md at repository root
- Validate the file meets all format requirements
"""

import os
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from sheep.feature_271_phase2 import execute_phase_2_file_creation_and_validation


def main():
    """Execute Phase 2: Create file and validate format."""
    try:
        result = execute_phase_2_file_creation_and_validation()

        print("\n" + "=" * 80)
        print("SUCCESS: Phase 2 - File Creation and Validation Complete")
        print("=" * 80)
        print(f"\nFile created: {result['filepath']}")
        print(f"File size: {result['file_size']} bytes")
        print(f"Validation passed: {result['validation_passed']}")
        print("\nReady for Phase 3: Git Integration and Push")

        return True

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
