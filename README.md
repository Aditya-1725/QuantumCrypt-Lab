# QuantumCrypt Lab

**Comparative Study of Classical vs Quantum Cryptographic Schemes**

A simple educational Python desktop application demonstrating end-to-end encryption workflows for a semester project.

---

## Features

The application uses a simple, clean UI with two main tabs:
1. **Classical AES**: Demonstrates symmetric encryption using AES-256-GCM.
2. **Quantum / BB84**: Demonstrates the concept of quantum-assisted key distribution using a conceptual BB84 simulation, followed by AES encryption.

Both modes use the exact same simplified workflow:
- Enter a human-readable key (e.g. `main`, `123456`)
- Encrypt a message to get a single encrypted text string
- Decrypt the encrypted text string using the same key to recover the message

---

## Installation & Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

*(Note: The application will attempt to automatically use the `venv` virtual environment if it exists in the project folder.)*

---

## Technical Details

- **UI Framework**: CustomTkinter
- **Classical Crypto**: PyCryptodome (AES-256-GCM). The application internally hashes the user's string key using SHA-256 to derive a secure 256-bit AES key. The AES nonce and authentication tag are packed directly into the base64 ciphertext for simplicity.
- **Quantum Simulation**: Qiskit. A basic BB84 circuit is simulated conceptually when generating the encrypted message in Quantum mode.
