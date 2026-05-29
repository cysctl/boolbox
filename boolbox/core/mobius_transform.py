# WARNING
# AI was used to reduce the time complexity from O(N^2) to O(N logN)
# In other words, the Fast Mobius Transform algorithm was developed with the aid of AI


# Fast Möbius Transform is referred to as the 'FMT'
# Algebraic Normal Form is referred to as the 'ANF'
#
def fmt(truth_table: list[int]) -> list[int]:
    """
    Applies the FMT to a given truth table to compute its ANF coefficients

    Args:
        truth_table: A one-dimensional list containing the binary values (0s and 1s) of a truth table

    Return:
        A list of integers representing the calculated ANF coefficients

    Raises:
        ValueError: If the length of the truth table is 0 or not a power of 2
    """

    n = len(truth_table)

    # This statement is not required within the scope of 'boolbox'
    # but it is mandatory if accessed from outside
    #
    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError(f"Invalid truth table size ({n}). It must be power of 2")

    # Copy the truth_table for in-place calculation
    #
    coeffs = truth_table[:]

    """
    Butterfly operations logic for an example array [1, 0, 1, 1]:

        Step 1 (step = 1): XOR adjacent elements
            anf[0] and anf[2] remain untouched
            anf[1] ^= anf[0]  ->  anf[1] = 0 ^ 1 = 1
            anf[3] ^= anf[2]  ->  anf[3] = 1 ^ 1 = 0

            The result is [1, 1, 1, 0]

        Step 2 (step = 2): XOR elements with distance of 2
            anf[0] and anf[1] remain untouched
            anf[2] ^= anf[0]  ->  anf[2] = 1 ^ 1 = 0
            anf[3] ^= anf[1]  ->  anf[3] = 0 ^ 1 = 1

            The result is [1, 1, 0, 1]

        End of Loop:
            The next step would be step = 4, but since step < n (4 < 4) is False, the loop terminates
            The final ANF coefficients are [1, 1, 0, 1]
    """

    step = 1
    while step < n:
        for i in range(0, n, step * 2):
            for j in range(step):
                coeffs[i + j + step] ^= coeffs[i + j]

        # Double the block size for the next pass
        # step in {1, 2, 4, ...}
        #
        step *= 2

    return coeffs


if __name__ == "__main__":
    sample_truth_table = [1, 0, 1, 1]

    # According to the explanation above
    # the expected output is [1, 1, 0, 1]
    #
    coeffs = fmt(sample_truth_table)

    print(f"Truth Table (input): {sample_truth_table}")
    print(f"ANF Coeffs (output) : {coeffs}")
