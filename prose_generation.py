#!/usr/bin/env python3
"""
Generate diverse prose content for markdown files using Claude API.

This module provides functions to generate high-quality prose content via
Claude API using subprocess. Output includes a markdown-suitable title and
2-3 sentences of coherent prose.
"""

import json
import os
import subprocess
import sys


def generate_prose():
    """
    Generate diverse, high-quality prose content via Claude API.

    Returns:
        dict: Contains 'title' (str) and 'prose' (str) keys.
            - 'title': A suitable title for markdown heading
            - 'prose': 2-3 sentences of coherent, grammatically correct content

    Raises:
        ValueError: If ANTHROPIC_API_KEY environment variable is not set
        RuntimeError: If Claude API call fails or returns invalid response
    """
    # Validate API key is available
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Please set it before calling generate_prose()."
        )

    # Construct Claude API prompt for prose generation
    prompt = """Generate a short, engaging piece of content about any topic.
Your response MUST be valid JSON with exactly these two fields:
{
  "title": "A concise title for a markdown heading (1-10 words)",
  "prose": "Exactly 2-3 sentences of coherent, grammatically correct prose on the topic. Make it meaningful and diverse."
}

Important:
- The prose must contain exactly 2-3 sentences (separated by periods, exclamation marks, or question marks)
- The prose must be grammatically correct
- The prose must be meaningful and demonstrate semantic quality
- No lists, code blocks, or special formatting in the prose
- Return ONLY valid JSON, no other text

Generate the response now:"""

    # Call Claude API via subprocess using curl (standard library alternative)
    try:
        # Use curl to call Claude API (more portable than Python http.client for this use case)
        # Alternatively, we could use Python's http.client from standard library
        curl_cmd = [
            "curl",
            "-s",
            "https://api.anthropic.com/v1/messages",
            "-H", "Content-Type: application/json",
            "-H", f"x-api-key: {api_key}",
            "-H", "anthropic-version: 2023-06-01",
            "-d", json.dumps({
                "model": "claude-3-5-sonnet-20241022",
                "max_tokens": 300,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            })
        ]

        result = subprocess.run(
            curl_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Claude API call failed with return code {result.returncode}: {result.stderr}"
            )

        # Parse the API response
        api_response = json.loads(result.stdout)

        # Extract the prose from the API response
        if "error" in api_response:
            error_msg = api_response.get("error", {}).get("message", "Unknown error")
            raise RuntimeError(f"Claude API error: {error_msg}")

        # Extract content from response
        if "content" not in api_response or not api_response["content"]:
            raise RuntimeError("Claude API returned empty content")

        content = api_response["content"][0].get("text", "")
        if not content:
            raise RuntimeError("Claude API returned empty text content")

        # Parse the prose JSON from the response
        prose_data = json.loads(content)

        # Validate required fields
        if "title" not in prose_data:
            raise RuntimeError("Generated prose missing 'title' field")
        if "prose" not in prose_data:
            raise RuntimeError("Generated prose missing 'prose' field")

        # Basic validation of content
        if not isinstance(prose_data["title"], str) or not prose_data["title"].strip():
            raise RuntimeError("Generated title is empty or not a string")
        if not isinstance(prose_data["prose"], str) or not prose_data["prose"].strip():
            raise RuntimeError("Generated prose is empty or not a string")

        return {
            "title": prose_data["title"].strip(),
            "prose": prose_data["prose"].strip()
        }

    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse Claude API response as JSON: {e}") from e
    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude API call timed out after 30 seconds") from None
    except FileNotFoundError:
        raise RuntimeError(
            "curl command not found. Please ensure curl is installed and in PATH."
        ) from None


def main():
    """Main entry point: generate prose and display it."""
    try:
        result = generate_prose()
        print(f"Title: {result['title']}")
        print(f"Prose: {result['prose']}")
        return 0
    except ValueError as e:
        print(f"[ERROR] Configuration error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"[ERROR] API error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
