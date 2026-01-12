from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate # Necessary for multicontrolled gates

def hadamards(q_circuit, n_inputs=0):
    # Applies the Hadamard gate to qubits 0...n_inputs
    # If n_inputs=0, no gate is applied
    for i in range(0, n_inputs):
        q_circuit.h(i)

def X_gates(q_circuit, n_inputs=0):
    # Applies the X gate to qubits 0...n_inputs
    # If n_inputs=0, no gate is applied
    for i in range(0, n_inputs):
        q_circuit.x(i)

#Diffusion Operator
def diffusion_operator(q_circuit, n_inputs):
    hadamards(q_circuit, n_inputs)
    q_circuit.barrier()
    X_gates(q_circuit, n_inputs)
    q_circuit.barrier()
    
    
    q_circuit.h(n_inputs-1)
    # Create an MCX gate with n_inputs-1 controls and one target
    mcx_gate = MCXGate(n_inputs-1)
    # Apply the MCX gate with controls 0...n_inputs-2 and target n_inputs-1
    q_circuit.append(mcx_gate, qargs=list(range(n_inputs)))
    q_circuit.h(n_inputs-1)
    

    q_circuit.barrier()
    X_gates(q_circuit, n_inputs)
    q_circuit.barrier()
    hadamards(q_circuit, n_inputs)

n_inputs = 4
n_outputs = 1
n_aux = 2
q_circuit = QuantumCircuit(n_inputs+n_outputs+n_aux,n_inputs)
diffusion_operator(q_circuit, n_inputs)
print()
print(q_circuit)
print()
