from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate
# Create a quantum circuit with at least 8 qubits
qc = QuantumCircuit(8)
# Define the number of control qubits
num_controls = 3
# Create an MCX gate
mcx_gate = MCXGate(num_controls)
# Apply the MCX gate (control qubits 2, 3, 4 and target qubit 7)
qc.append(mcx_gate, qargs=[2, 3, 4, 7])
# Draw the circuit
print(qc)
