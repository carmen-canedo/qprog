from qiskit import QuantumCircuit
from qiskit.circuit.library import MCXGate # Necessary for multicontrolled gates

#Example of Oracle Circuit
def OracleCircuit(q_circuit,n_inputs,n_aux):
    # Computes the function
    # a3 AND (NOT a2) AND a1 AND (NOT a0)
    #Input qubits 0,1,2,3
    #Output qubit: 4
    #aux qubit: 5,6
    q_circuit.barrier()
    q_circuit.x(0) # negate bit a_0
    q_circuit.x(2) # negate bit a_2
    q_circuit.barrier()
    q_circuit.ccx(0,1,5)
    q_circuit.ccx(5,2,6)
    q_circuit.ccx(6,3,4) # output
    q_circuit.ccx(5,2,6) # reset aux bit a_6
    q_circuit.ccx(0,1,5) # reset aux bit a_5 
    q_circuit.barrier()
    q_circuit.x(2) # reset bit a_2
    q_circuit.x(0) # reset bit a_0
    q_circuit.barrier()

n_inputs = 4
n_outputs = 1
n_aux = 2
q_circuit = QuantumCircuit(n_inputs+n_outputs+n_aux,n_inputs)
OracleCircuit(q_circuit,n_inputs,n_aux)
print()
print(q_circuit)
print()
