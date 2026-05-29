# Algebraic Normal Form is referred to as the ANF


def generate_anf_poly(coeffs: list[int]) -> str:
    """
    Converts a list of ANF coefficients into a readable boolean polynomial representation

    Args:
        coeffs: A one-dimensional list containing ANF coefficients (0s and 1s)

    Return:
        A string representing the boolean polynomial in ANF format

    Raises:
        ValueError: If the length of the ANF coefficient list is 0 or not a power of 2
    """

    n = len(coeffs)

    # This statement is not required within the scope of Boolbox, but it is mandatory if accessed from outside
    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError(
            f"Invalid ANF coefficient list size ({n}). It must be power of 2"
        )

    # ANF polynomial terms
    #
    terms = []

    """
    Mapping indices to polynomial terms:

    Reading the binary index from right to left
    so, a 3-bit number is expressed as (x_2)(x_1)(x_0):

        Index 0  ->  0 0 0  ->  1 (const)
        Index 1  ->  0 0 1  ->  x_0
        Index 2  ->  0 1 0  ->  x_1
        Index 3  ->  0 1 1  ->  x_0 x_1     (in-order, left2right: x_1 x_0)
        Index 5  ->  1 0 1  ->  x_0 x_2     (in-order, left2right: x_2 x_0)
    """

    for idx, coeff in enumerate(coeffs):
        if coeff == 1:
            if idx == 0:
                # constant
                terms.append("1")
            else:
                vars_in_term = []
                tmp_idx = idx
                bit_pos = 0

                # Evalautes the binary representation of the index bit by bit
                #
                while tmp_idx > 0:
                    if tmp_idx & 1 == 1:
                        vars_in_term.append(f"x_{bit_pos}")

                    # Next bit
                    #
                    tmp_idx >>= 1
                    bit_pos += 1

                # The terms are separated by the AND operator
                # So, AND operator is referred to as a whitespace (" ")
                #
                terms.append(" ".join(vars_in_term))

    return " XOR ".join(terms)


if __name__ == "__main__":
    sample_anf_coeffs = [1, 1, 0, 1]

    anf_poly = generate_anf_poly(sample_anf_coeffs)

    print(f"ANF Coeffs: {sample_anf_coeffs}")

    """
    Manual calculation for [1, 1, 0, 1]:

        Index 0  ->  0 0  ->  coeff 1  ->  1 (constant)
        Index 1  ->  0 1  ->  coeff 1  ->  x_0
        Index 2  ->  1 0  ->  coeff 0  ->  (skipped)
        Index 3  ->  1 1  ->  coeff 1  ->  x_0 x_1

        Resulting terms array: ["1", "x_0", "x_0 x_1"]
        Joined with " XOR ": 1 XOR x_0 XOR x_0 x_1

    So, the expected output is 1 XOR x_0 XOR x_0 x_1
    """

    print(f"ANF Polynomial: {anf_poly}")
