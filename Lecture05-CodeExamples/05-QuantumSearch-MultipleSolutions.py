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

#Example of Oracle Circuit
def OracleCircuit(q_circuit,n_inputs,n_aux):
    # Computes the function
    # a3 AND (NOT a2) AND a1 NAND (NOT a0)
    #Input qubits 0,1,2,3
    #Output qubit: 4
    #aux qubit: 5,6
    q_circuit.barrier()
    q_circuit.x(0) # negate bit a_0
    q_circuit.x(2) # negate bit a_2
    q_circuit.x(5) # negate bit a_5 (to create multiple solutions)
    q_circuit.barrier()
    q_circuit.ccx(0,1,5)
    q_circuit.ccx(5,2,6)
    q_circuit.ccx(6,3,4) # output
    q_circuit.ccx(5,2,6) # reset aux bit a_6
    q_circuit.ccx(0,1,5) # reset aux bit a_5
    q_circuit.barrier()
    q_circuit.x(5) # reset bit a_5 (to create multiple solutions)
    q_circuit.x(2) # reset bit a_2
    q_circuit.x(0) # reset bit a_0
    q_circuit.barrier()

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

#k is the number of iterations. Default is 1 if not specified.
def quantum_search(q_circuit,n_inputs,n_aux,k=1):
    q_circuit.barrier()
    hadamards(q_circuit, n_inputs) 
    for i in range(k):
        q_circuit.barrier()
        OracleCircuit(q_circuit,n_inputs,n_aux)
        diffusion_operator(q_circuit,n_inputs)
    q_circuit.barrier()
    #Obs: When measuring most-significant bits are to the left 
    circ.measure(range(n_inputs), range(n_inputs)) 


######################################################
##################### SETUP #####################
######################################################

n_inputs = 4
n_outputs = 1
n_aux = 2
circ = QuantumCircuit(n_inputs+n_outputs+n_aux,n_inputs)
quantum_search(circ,n_inputs,n_aux,1)
print()
print(circ)
print()

######################################################
##################### SIMULATION #####################
######################################################

#Simulation using AerSimulator()
#The code below is generic and can be used with other quantum circuits with a small number of qubits. 
 
#Define the backend
from qiskit_aer import AerSimulator
backend = AerSimulator()

#Transpile 
from qiskit import transpile
compiled_circuit = transpile(circ, backend)

#Execute the circuit in the simulator
n_shots = 1024 #The default number of shots is 1024 
result = backend.run(compiled_circuit, shots=n_shots).result()

# Extract Information.
counts = result.get_counts(compiled_circuit)
probs = {key:value/n_shots for key,value in counts.items()}
print("Counts",counts)
print("Probabilities:", probs)
print()

from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
plot_histogram(probs,title="Histogram")
plt.show() 
