"""
End-to-end workflow orchestration for feature 235: markdown file creation.

This module orchestrates the complete workflow:
1. Create markdown file with proper format (pathlib)
2. Validate all file properties (encoding, line endings, size, structure)
3. Execute git operations (add, commit, push)

Provides comprehensive status reporting for each phase.
"""

import sys
from pathlib import Path
from datetime import datetime

from validate_markdown_file import validate_file, ValidationError, FILENAME
from git_workflow import GitWorkflow, GitWorkflowError


# ============================================================================
# Constants
# ============================================================================

FILENAME_CONSTANT = FILENAME
FEATURE_BRANCH = "feat/235-markdown-file-creation-4bcbca"


# ============================================================================
# Status Reporting
# ============================================================================


class WorkflowStatus:
    """Tracks workflow status with timestamps and detailed reporting."""

    def __init__(self):
        """Initialize status tracker."""
        self.phases = {}
        self.start_time = datetime.now()
        self.end_time = None
        self.overall_success = True
        self.error_message = None

    def start_phase(self, phase_name):
        """Mark the start of a phase."""
        self.phases[phase_name] = {
            "start": datetime.now(),
            "end": None,
            "success": None,
            "error": None,
        }

    def end_phase(self, phase_name, success=True, error=None):
        """Mark the end of a phase."""
        if phase_name in self.phases:
            self.phases[phase_name]["end"] = datetime.now()
            self.phases[phase_name]["success"] = success
            self.phases[phase_name]["error"] = error
            if not success:
                self.overall_success = False

    def report(self):
        """Generate comprehensive status report."""
        lines = []
        lines.append("\n" + "=" * 80)
        lines.append("FEATURE 235: MARKDOWN FILE CREATION - WORKFLOW STATUS REPORT")
        lines.append("=" * 80)

        for phase_name, phase_data in self.phases.items():
            status = "✓ SUCCESS" if phase_data["success"] else "✗ FAILED"
            duration = ""
            if phase_data["end"]:
                delta = phase_data["end"] - phase_data["start"]
                duration = f" ({delta.total_seconds():.2f}s)"
            lines.append(f"\n[Phase] {phase_name}{duration}")
            lines.append(f"Status: {status}")
            if phase_data["error"]:
                lines.append(f"Error: {phase_data['error']}")

        lines.append("\n" + "-" * 80)
        overall_status = "✓ ALL PHASES SUCCEEDED" if self.overall_success else "✗ WORKFLOW FAILED"
        lines.append(f"Overall Status: {overall_status}")

        if self.end_time:
            total_delta = self.end_time - self.start_time
            lines.append(f"Total Duration: {total_delta.total_seconds():.2f}s")

        lines.append("=" * 80 + "\n")

        return "\n".join(lines)


# ============================================================================
# Workflow Orchestration
# ============================================================================


def create_markdown_file(filepath=FILENAME_CONSTANT):
    """
    Create markdown file with H1 heading and prose content.

    Args:
        filepath (str): Path to create file at (default: test-qz1gsg.md)

    Returns:
        bool: True if file creation succeeds

    Raises:
        Exception: If file creation fails
    """
    filepath = Path(filepath)

    # Content: H1 heading + blank line + 2-3 sentences about resilience
    content = (
        "# The Nature of Resilience\n"
        "\n"
        "Resilience is the quiet strength that allows individuals and organizations "
        "to bend without breaking when faced with adversity and uncertainty. "
        "This capacity to adapt, recover, and even grow from challenges is not innate "
        "but cultivated through experience, support systems, and a commitment to continuous learning. "
        "In an increasingly complex world, resilience has become one of the most valuable assets we can develop.\n"
    )

    # Use pathlib with explicit encoding and line endings
    filepath.write_text(content, encoding="utf-8", newline="\n")
    return True


def validate_markdown_file(filepath=FILENAME_CONSTANT):
    """
    Validate markdown file properties.

    Args:
        filepath (str): Path to file to validate (default: test-qz1gsg.md)

    Returns:
        bool: True if all validations pass

    Raises:
        ValidationError: If any validation fails
    """
    return validate_file(filepath)


def execute_git_operations():
    """
    Execute git workflow: add, commit, push.

    Returns:
        bool: True if all git operations succeed

    Raises:
        GitWorkflowError: If any git operation fails
    """
    workflow = GitWorkflow()
    return workflow.execute_workflow()


# ============================================================================
# Main Workflow
# ============================================================================


def main():
    """
    Execute complete end-to-end workflow with comprehensive status reporting.

    Returns:
        int: 0 if all phases succeed, 1 if any phase fails
    """
    status = WorkflowStatus()

    # Phase 1: File Creation
    status.start_phase("Phase 1: File Creation")
    try:
        create_markdown_file()
        status.end_phase("Phase 1: File Creation", success=True)
        print("[✓] Phase 1 complete: Markdown file created")
    except Exception as e:
        status.end_phase("Phase 1: File Creation", success=False, error=str(e))
        print(f"[✗] Phase 1 failed: {e}")
        status.end_time = datetime.now()
        print(status.report())
        return 1

    # Phase 2: Validation
    status.start_phase("Phase 2: Validation")
    try:
        validate_markdown_file()
        status.end_phase("Phase 2: Validation", success=True)
        print("[✓] Phase 2 complete: All file properties validated")
    except ValidationError as e:
        status.end_phase("Phase 2: Validation", success=False, error=str(e))
        print(f"[✗] Phase 2 failed: {e}")
        status.end_time = datetime.now()
        print(status.report())
        return 1

    # Phase 3: Git Integration
    status.start_phase("Phase 3: Git Integration & Push")
    try:
        execute_git_operations()
        status.end_phase("Phase 3: Git Integration & Push", success=True)
        print("[✓] Phase 3 complete: Git operations succeeded (add, commit, push)")
    except GitWorkflowError as e:
        status.end_phase("Phase 3: Git Integration & Push", success=False, error=str(e))
        print(f"[✗] Phase 3 failed: {e}")
        status.end_time = datetime.now()
        print(status.report())
        return 1

    # All phases succeeded
    status.end_time = datetime.now()
    print(status.report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
