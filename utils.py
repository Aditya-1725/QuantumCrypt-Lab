"""
utils.py — QuantumCrypt Lab
Helper utilities for the simplified educational cryptography simulator.
"""

import hashlib
import base64

# ---------------------------------------------------------------------------
# Key Derivation
# ---------------------------------------------------------------------------

def derive_key_from_string(key_str: str) -> bytes:
    """
    Derive a 256-bit (32-byte) AES key from a human-readable string.
    Uses SHA-256 to hash the string.
    """
    if not key_str or not key_str.strip():
        raise ValueError("Key cannot be empty.")
    
    # Use SHA-256 to create a 32-byte key
    digest = hashlib.sha256(key_str.encode("utf-8")).digest()
    return digest

# ---------------------------------------------------------------------------
# Encoding helpers
# ---------------------------------------------------------------------------

def bytes_to_b64(data: bytes) -> str:
    """Encode bytes as a URL-safe base64 string."""
    return base64.urlsafe_b64encode(data).decode("utf-8")

def b64_to_bytes(b64_str: str) -> bytes:
    """Decode a URL-safe base64 string to bytes."""
    b64_str = b64_str.strip()
    try:
        return base64.urlsafe_b64decode(b64_str)
    except Exception as exc:
        raise ValueError("Invalid encrypted text (base64 decode failed).") from exc

# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_message(message: str) -> None:
    """Raise ValueError if message is empty."""
    if not message or not message.strip():
        raise ValueError("Message cannot be empty.")
