"""
quantum_crypto.py — QuantumCrypt Lab
Integrates a conceptual BB84 key distribution with AES encryption/decryption.
"""

from bb84 import run_bb84_simulation
from classical_crypto import aes_encrypt, aes_decrypt


def quantum_encrypt(message: str, key_str: str) -> str:
    """
    Simulate BB84 key distribution, then encrypt the message using AES-256-GCM.
    
    Parameters
    ----------
    message : str
        The plaintext message to encrypt.
    key_str : str
        The human-readable string key.
        
    Returns
    -------
    str — base64 ciphertext containing nonce + tag + ciphertext
    """
    # 1. Simulate the Quantum Key Distribution concept
    # (In a real system, the keys would be securely shared over a quantum channel here)
    run_bb84_simulation()
    
    # 2. Encrypt the message using AES
    return aes_encrypt(message, key_str)


def quantum_decrypt(encrypted_b64: str, key_str: str) -> str:
    """
    Decrypt a message encrypted with quantum_encrypt.
    """
    return aes_decrypt(encrypted_b64, key_str)
