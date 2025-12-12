from qiskit import QuantumCircuit

class ClassicalCircuit:
    def __init__(self,filename):
        self.n_inputs = 0
        self.n_outputs = 0
        self.n_internal = 0
        self.input_gates = [] # list with n_inputs numbers indicating which are the input gates
        self.output_gates = [] # list with n_outputs numbers indicating which are the output gates
        self.internal_gates = [] # list with n_internal numbers indicating which are the internal gates
        self.gates = []
        self.read(filename)
    
    def read(self,filename):
        with open(filename,'r') as file:
            lines = file.readlines()
        self.n_inputs = int(lines[0].strip())
        self.n_outputs = int(lines[1].strip())
        self.n_internal = int(lines[2].strip())
        self.input_gates = list(map(int,lines[3].strip().split()))
        self.output_gates = list(map(int,lines[4].strip().split()))
        self.internal_gates = list(map(int,lines[5].strip().split()))
        for line in lines[6:]:
            gate = line.strip().split()
            gate[0] = int(gate[0])
            if gate[1] == "and" or gate[1] == "or" or gate[1] == "xor" or gate[1]=="nand":
                gate[2] = int(gate[2])
                gate[3] = int(gate[3])
            elif gate[1] == "not":
                gate[2] = int(gate[2])
            self.gates.append(gate)
    def print(self):
        print(f"n_inputs: {self.n_inputs}")
        print(f"n_outputs: {self.n_outputs}")
        print(f"n_internal: {self.n_internal}")
        print(f"Input Gates: {self.input_gates}")
        print(f"Output Gates: {self.output_gates}")
        print(f"Internal Gates: {self.internal_gates}")
        print("Gates: ") # reads n_outputs + n_internal
        for gate in self.gates:
            print(gate)
        print()

    def convert_step_1(self,quantumCircuit):
        
        for gate in self.gates:
            a = gate[0]
            gate_type = gate[1]

            quantumCircuit.barrier()

            if gate_type == 'and':
                b = gate[2]
                c = gate[3]
                quantumCircuit.ccx(b, c, a)

            elif gate_type == 'not':
                b = gate[2]
                quantumCircuit.x(a)
                quantumCircuit.cx(b, a)

        return quantumCircuit
    
    def convert_step_2(self,quantumCircuit):

        for i in range(len(self.gates) - 1, -1, -1):
            gate = self.gates[i]
            a = gate[0]
            gate_type = gate[1]

            if gate_type == "and":
                b = gate[2]
                c = gate[3]
                quantumCircuit.ccx(b, c, a)

            elif gate_type == 'not':
                b = gate[2]
                quantumCircuit.cx(b, a)
                quantumCircuit.x(a)

        return quantumCircuit

    def convert(self,quantumCircuit):

        n_inputs = self.n_inputs
        aux_shift = self.n_outputs

        # From step 1
        for gate in self.gates:
            a = gate[0]
            gate_type = gate[1]

            quantumCircuit.barrier()

            a_mapped = a if a in self.input_gates else a + aux_shift

            if gate_type == 'and':

                b = gate[2]
                c = gate[3]

                b_mapped = b if b in self.input_gates else b + aux_shift
                c_mapped = c if c in self.input_gates else c + aux_shift

                quantumCircuit.ccx(b_mapped, c_mapped, a_mapped)

            elif gate_type == 'not':

                b = gate[2]
                b_mapped = b if b in self.input_gates else b + aux_shift

                quantumCircuit.x(a_mapped)
                quantumCircuit.cx(b_mapped, a_mapped)

        quantumCircuit.barrier()

        # Classical copied to output qubits
        for i in range(self.n_outputs):
            a = self.output_gates[i]
            a_aux = a + aux_shift
            a_prime = n_inputs + i
            quantumCircuit.cx(a_aux, a_prime)
        
        quantumCircuit.barrier()

        # From step 2
        for i in range(len(self.gates) - 1, -1, -1):

            gate = self.gates[i]
            a = gate[0]
            gate_type = gate[1]

            a_mapped = a if a in self.input_gates else a + aux_shift

            if gate_type == "and":
                b = gate[2]
                c = gate[3]

                b_mapped = b if b in self.input_gates else b + aux_shift
                c_mapped = c if c in self.input_gates else c + aux_shift

                quantumCircuit.ccx(b_mapped, c_mapped, a_mapped)

            elif gate_type == 'not':
                b = gate[2]

                b_mapped = b if b in self.input_gates else b + aux_shift

                quantumCircuit.cx(b_mapped, a_mapped)
                quantumCircuit.x(a_mapped)


        return quantumCircuit    


    
cc = ClassicalCircuit("hw3/circuit.txt")
cc.print()

n_wires = cc.n_inputs + cc.n_outputs + cc.n_internal
qc = QuantumCircuit(n_wires,0)
cc.convert_step_1(qc)
print(qc)
print()

n_wires = cc.n_inputs + cc.n_outputs + cc.n_internal
qc = QuantumCircuit(n_wires,0)
cc.convert_step_2(qc)
print(qc)
print()

n_wires = cc.n_inputs + 2*cc.n_outputs + cc.n_internal
qc = QuantumCircuit(n_wires,0)
cc.convert(qc)
print(qc)
print()