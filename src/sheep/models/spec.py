"""Spec intake data contract and validation utilities."""

import math
from collections import Counter

from pydantic import BaseModel, field_validator

from sheep.config.settings import get_settings


def compute_shannon_entropy(text: str) -> float:
    """Compute Shannon entropy (bits/character) for the given text.

    Returns 0.0 for empty or single-character-class strings.
    Formula: H = -sum(p_i * log2(p_i)) over unique character frequencies.
    """
    if not text:
        return 0.0
    counts = Counter(text)
    total = len(text)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())


class SpecInput(BaseModel):
    """Input contract for a spec submission.

    Validates that user_query meets minimum length and entropy requirements
    before any spec file is written to disk.
    """

    user_query: str

    @field_validator("user_query")
    @classmethod
    def validate_user_query(cls, value: str) -> str:
        """Enforce minimum length and Shannon entropy thresholds."""
        settings = get_settings()
        min_chars = settings.spec_min_chars
        min_entropy = settings.spec_min_entropy

        if len(value) < min_chars:
            raise ValueError(
                f"[input_too_short] Input is {len(value)} characters; "
                f"minimum is {min_chars}. "
                f"Describe the feature in plain English, at least {min_chars} characters."
            )

        entropy = compute_shannon_entropy(value)
        if entropy < min_entropy:
            raise ValueError(
                f"[input_low_entropy] Input appears to be gibberish or repetitive "
                f"(entropy {entropy:.2f} bits/char; minimum is {min_entropy}). "
                f"Describe the feature in plain English with varied, meaningful words."
            )

        return value
