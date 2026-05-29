import pytest
from boolbox.quantum.builder import QuantumCircuitBuilder


# Test for allocating the correct number of qubits based on input and output sizes
#
def test_circuit_dimensions():
    polys = {0: "x_0", 1: "1 XOR x_1"}
    builder = QuantumCircuitBuilder(input_size=3, polys=polys)
    
    qc = builder.build()

    """
    Manual trace for qubit allocation:

        Input size is explicitly set to 3
        The polys dictionary has 2 items, meaning 2 target outputs
        Total qubits required = 3 (inputs) + 2 (outputs) = 5
        
    So, the expected total qubits is 5, and output_size is 2
    """

    expected_total_qubits = 5
    expected_output_size = 2

    assert qc.num_qubits == expected_total_qubits
    assert builder.output_size == expected_output_size


# Test for the correct mapping of ANF terms to quantum gates
#
def test_gate_assignments():
    polys = {0: "1 XOR x_0 XOR x_1 x_2 XOR x_0 x_1 x_2 x_3"}
    builder = QuantumCircuitBuilder(input_size=4, polys=polys)
    
    qc = builder.build()
    ops = qc.count_ops()

    """
    Manual trace for "1 XOR x_0 XOR x_1 x_2 XOR x_0 x_1 x_2 x_3":

        Split by " XOR " -> ["1", "x_0", "x_1 x_2", "x_0 x_1 x_2 x_3"]
        "1" creates a Pauli-X gate (x)
        "x_0" (1 control) creates a CNOT gate (cx)
        "x_1 x_2" (2 controls) creates a Toffoli gate (ccx)
        "x_0 x_1 x_2 x_3" (4 controls) creates a Multi-Controlled X gate (mcx)
        
    So, we expect exactly 1 of each: x, cx, ccx, mcx
    """

    assert ops.get("x") == 1
    assert ops.get("cx") == 1
    assert ops.get("ccx") == 1
    assert ops.get("mcx") == 1


# Test for safely ignoring empty strings and isolated zero terms
#
def test_skip_zero_and_empty():
    polys = {0: "0", 1: "", 2: "0 XOR x_0"}
    builder = QuantumCircuitBuilder(input_size=2, polys=polys)
    
    qc = builder.build()
    ops = qc.count_ops()

    """
    Manual trace for empty and zero polynomials:
    
        Target 0: "0" is skipped (continue)
        Target 1: "" is skipped (continue)
        Target 2: "0" is skipped, "x_0" creates a CNOT gate (cx)
        
    Since the isolated "0" is ignored, no Pauli-X gates are added
    Expected ops should only contain 1 cx gate
    """

    assert ops.get("cx") == 1
    assert "x" not in ops


# Test for out-of-bounds qubit index references
#
def test_out_of_bounds_qubit():
    polys = {0: "x_0 x_2"}
    builder = QuantumCircuitBuilder(input_size=2, polys=polys)

    """
    Defensive bounds check:

        input_size is 2, so valid variables are x_0 and x_1
        The term "x_0 x_2" contains x_2
        max_var evaluates to 2
        Since max_var (2) >= input_size (2), the check fails
    
    The validation condition is violated
    Expects ValueError indicating the input_size limit
    """

    with pytest.raises(ValueError, match="but input_size is only 2"):
        builder.build()


# Test for handling unrecognized or garbage tokens in the ANF polynomial
#
def test_unrecognized_term():
    polys = {0: "x_0 XOR GARBAGE"}
    builder = QuantumCircuitBuilder(input_size=3, polys=polys)

    """
    Token recognition check:

        "x_0" is successfully parsed
        "GARBAGE" does not equal "1", "0", and does not start with "x_"
        Falls through to the final else block
        
    The validation condition is violated
    Expects ValueError indicating an unrecognized ANF term
    """

    with pytest.raises(ValueError, match="Unrecognized ANF term"):
        builder.build()