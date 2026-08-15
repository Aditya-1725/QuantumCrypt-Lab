"""
test_app.py — Smoke tests for the Simplified QuantumCrypt Lab
"""

import sys

def test_utils():
    print("Testing utils...")
    from utils import derive_key_from_string
    key1 = derive_key_from_string("main")
    key2 = derive_key_from_string("main")
    assert key1 == key2, "KDF must be deterministic"
    assert len(key1) == 32, "KDF must produce 32 bytes"
    try:
        derive_key_from_string("")
        assert False, "Empty key should fail"
    except ValueError:
        pass
    print("  [PASS] Utils")


def test_classical():
    print("Testing classical AES...")
    from classical_crypto import aes_encrypt, aes_decrypt
    msg = "Hello world"
    key = "main"

    cipher = aes_encrypt(msg, key)
    assert isinstance(cipher, str), "Ciphertext must be a base64 string"
    assert len(cipher) > 10, "Ciphertext seems too short"

    plain = aes_decrypt(cipher, key)
    assert plain == msg, "Decrypted message must match original"

    try:
        aes_decrypt(cipher, "wrong_key")
        assert False, "Wrong key should fail"
    except ValueError:
        pass

    print("  [PASS] Classical AES")


def test_quantum():
    print("Testing quantum/BB84 integration...")
    from quantum_crypto import quantum_encrypt, quantum_decrypt
    msg = "Hello world"
    key = "main"

    cipher = quantum_encrypt(msg, key)
    plain = quantum_decrypt(cipher, key)
    assert plain == msg, "Decrypted message must match original"

    print("  [PASS] Quantum Integration")


if __name__ == "__main__":
    try:
        test_utils()
        test_classical()
        test_quantum()
        print("\nALL TESTS PASSED")
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)
