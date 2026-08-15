"""
bb84.py — QuantumCrypt Lab
Simple BB84 Quantum Key Distribution simulation using Qiskit.
Demonstrates the concept for educational purposes without overwhelming the user.
"""

import random

try:
    from qiskit import QuantumCircuit
    from qiskit_aer import AerSimulator
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False
    QuantumCircuit = None   # type: ignore[assignment,misc]
    AerSimulator = None     # type: ignore[assignment,misc]


def _encode_qubit(bit: int, basis: str) -> QuantumCircuit:
    """Create a 1-qubit Qiskit circuit encoding `bit` in the given `basis`."""
    qc = QuantumCircuit(1, 1)
    if bit == 1:
        qc.x(0)
    if basis == "x":
        qc.h(0)
    return qc


def _measure_qubit(circuit: QuantumCircuit, basis: str) -> QuantumCircuit:
    """Append measurement operations to a qubit circuit in the given `basis`."""
    qc = circuit.copy()
    if basis == "x":
        qc.h(0)
    qc.measure(0, 0)
    return qc


def _run_circuit(circuit: QuantumCircuit, simulator: "AerSimulator") -> int:
    """Run a single-shot Qiskit circuit and return the measured bit (0 or 1)."""
    job = simulator.run(circuit, shots=1, memory=True)
    result = job.result()
    bit = int(result.get_memory()[0])
    return bit


def run_bb84_simulation(n_qubits: int = 8) -> bool:
    """
    Run a small conceptual BB84 simulation.
    Returns True if successful.
    """
    if not QISKIT_AVAILABLE:
        # Classical fallback simulation
        alice_bits = [random.randint(0, 1) for _ in range(n_qubits)]
        alice_bases = [random.choice(["+", "x"]) for _ in range(n_qubits)]
        bob_bases = [random.choice(["+", "x"]) for _ in range(n_qubits)]
        bob_bits = []
        for i in range(n_qubits):
            if bob_bases[i] == alice_bases[i]:
                bob_bits.append(alice_bits[i])
            else:
                bob_bits.append(random.randint(0, 1))
        return True

    # Qiskit simulation
    simulator = AerSimulator()
    alice_bits = [random.randint(0, 1) for _ in range(n_qubits)]
    alice_bases = [random.choice(["+", "x"]) for _ in range(n_qubits)]
    
    encoded_circuits = [
        _encode_qubit(b, basis) for b, basis in zip(alice_bits, alice_bases)
    ]
    
    bob_bases = [random.choice(["+", "x"]) for _ in range(n_qubits)]
    bob_bits = []
    
    for i, circuit in enumerate(encoded_circuits):
        measure_circuit = _measure_qubit(circuit, bob_bases[i])
        bit = _run_circuit(measure_circuit, simulator)
        bob_bits.append(bit)
        
    return True
