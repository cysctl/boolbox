from qiskit import QuantumCircuit

class QuantumCircuitBuilder:
    """
    Synthesizes a QuantumCircuit from Algebraic Normal Form (ANF) polynomials
    
    Convention: 
        
        Input qubits map to q_0 ... q_{input_size-1} (top wires, LSB)
        Target (output) qubits map to q_{input_size} ... q_{input_size + output_size - 1}
        The circuit is strictly out-of-place (inputs are preserved)
    """

    def __init__(self, input_size: int, polys: dict[int, str]):
        self.input_size = input_size
        self.polys = polys
        self.output_size = len(polys)

    def build(self) -> QuantumCircuit:
        """
        Builds and returns the configured QuantumCircuit
        """

        # Calculate the total number of qubits required for the circuit
        #
        total_qubits = self.input_size + self.output_size
        qc = QuantumCircuit(total_qubits)

        for out_idx, poly_str in self.polys.items():
            # Map the output index to its corresponding target qubit
            #
            target_qubit = self.input_size + out_idx

            # Skip empty or explicit zero polynomials
            #
            if not poly_str or poly_str == "0":
                continue

            # Split the polynomial into its constituent terms
            #
            terms = poly_str.split(" XOR ")

            for term in terms:
                term = term.strip()
                
                if term == "1":
                    # Constant value 1 applies a Pauli-X (NOT) gate to the target
                    #
                    qc.x(target_qubit)
                elif term == "0":
                    # Explicitly skip isolated "0" terms to prevent parsing them as x_0
                    #
                    continue
                elif term.startswith("x_"):
                    # Extract control qubit indices from the term
                    #
                    variables = term.split(" ")
                    controls = [int(v.replace("x_", "")) for v in variables]

                    # Defensively validate that variables do not exceed the defined input_size
                    #
                    max_var = max(controls)
                    if max_var >= self.input_size:
                        raise ValueError(
                            f"Polynomial references x_{max_var} but input_size is only {self.input_size}."
                        )

                    num_controls = len(controls)

                    # Apply the appropriate gate based on the number of control qubits
                    # Delegating multi-control synthesis to Qiskit's compiler
                    #
                    if num_controls == 1:
                        qc.cx(controls[0], target_qubit)
                    elif num_controls == 2:
                        qc.ccx(controls[0], controls[1], target_qubit)
                    else:
                        qc.mcx(controls, target_qubit)
                else:
                    # Raise a controlled error for completely unrecognized tokens
                    #
                    raise ValueError(f"Unrecognized ANF term: {term!r}")

        return qc