"""Test execution of feature 236 with mocked LLM to validate the orchestration."""

from unittest.mock import patch
from pathlib import Path

# Sample valid markdown content that meets all requirements
SAMPLE_MARKDOWN = """# The Power of Curiosity

Curiosity is the driving force behind human progress and discovery across all domains of knowledge. It compels us to question, explore, and understand the world around us, leading to innovations that shape our future. By nurturing curiosity, we unlock our potential for growth and transformation.
"""

def execute_feature_236_with_mock():
    """Execute feature 236 with mocked LLM for testing."""
    with patch('sheep.features.feature_236_markdown_file_creation.generate_markdown_content') as mock_gen:
        mock_gen.return_value = SAMPLE_MARKDOWN
        
        from sheep.features.feature_236_markdown_file_creation import create_feature_236_markdown_file
        
        result = create_feature_236_markdown_file()
        return result

if __name__ == "__main__":
    result = execute_feature_236_with_mock()
    print("\n✓ Feature 236 execution successful!")
    print(f"  File: {result['filepath']}")
    print(f"  Content length: {len(result['content'])} bytes")
    print(f"  Commit message: {result['commit_message']}")
    
    # Verify file exists and properties
    filepath = Path(result['filepath'])
    if filepath.exists():
        print(f"\n✓ File created successfully at: {filepath}")
        print(f"  File size: {filepath.stat().st_size} bytes")
        
        # Verify line endings
        with open(filepath, 'rb') as f:
            content_bytes = f.read()
            if b'\r\n' in content_bytes:
                print(f"  ✗ ERROR: File has CRLF line endings (should have LF)")
            elif b'\n' in content_bytes:
                print(f"  ✓ File has LF line endings (correct)")
