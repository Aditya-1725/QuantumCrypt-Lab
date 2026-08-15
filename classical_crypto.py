"""
classical_crypto.py — QuantumCrypt Lab
AES-256-GCM encryption and decryption.
Packs the nonce and tag into the ciphertext so the user only sees one string.
"""

from Crypto.Cipher import AES
from utils import (
    bytes_to_b64,
    b64_to_bytes,
    validate_message,
    derive_key_from_string,
)


def aes_encrypt(message: str, key_str: str) -> str:
    """
    Encrypt a plaintext message using AES-256-GCM.
    
    Parameters
    ----------
    message : str
        The plaintext message to encrypt.
    key_str : str
        The human-readable string key.
        
    Returns
    -------
    str
        A single base64 string containing: nonce (16 bytes) + tag (16 bytes) + ciphertext
    """
    validate_message(message)

    # Derive 32-byte AES key from the user's string key
    aes_key = derive_key_from_string(key_str)

    cipher = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode("utf-8"))

    # Pack everything together: 16 bytes nonce + 16 bytes tag + N bytes ciphertext
    packed_data = cipher.nonce + tag + ciphertext

    return bytes_to_b64(packed_data)


def aes_decrypt(encrypted_b64: str, key_str: str) -> str:
    """
    Decrypt an AES-256-GCM packed ciphertext.

    Parameters
    ----------
    encrypted_b64 : str
        The base64 string containing nonce + tag + ciphertext.
    key_str : str
        The human-readable string key.

    Returns
    -------
    str — the decrypted plaintext message
    
    Raises
    ------
    ValueError — if decryption fails or data is malformed
    """
    if not encrypted_b64 or not encrypted_b64.strip():
        raise ValueError("Encrypted text cannot be empty.")

    # Derive the exact same 32-byte AES key
    aes_key = derive_key_from_string(key_str)

    try:
        packed_data = b64_to_bytes(encrypted_b64)
    except ValueError as exc:
        raise ValueError("Invalid encrypted text or corrupted data.") from exc

    if len(packed_data) < 32:
        raise ValueError("Invalid encrypted text (too short).")

    # Unpack
    nonce = packed_data[:16]
    tag = packed_data[16:32]
    ciphertext = packed_data[32:]

    try:
        cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode("utf-8")
    except (ValueError, KeyError):
        raise ValueError("Invalid key or encrypted text.")
