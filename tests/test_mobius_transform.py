import pytest
from boolbox.core.mobius_transform import fmt

# Fast Möbius Transform is referred to as the FMT


# Test for basic truth table
#
def test_fmt_basic_example():
    sample_truth_table = [1, 0, 1, 1]

    coeffs = fmt(sample_truth_table)

    # NOTE
    # Much of the explanation below has been copied directly from the boolbox/core/mobius_transform.py file

    """
    Manual calculation for example array [1, 0, 1, 1]:

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

    expected_coeffs = [1, 1, 0, 1]

    assert coeffs == expected_coeffs


# Test for an truth table with all elements set to zero
#
def test_fmt_all_zeros():
    zero_table = [0, 0, 0, 0]

    coeffs = fmt(zero_table)

    # 0 ^ 0 is always 0. The array remains unchanged
    # regardless of the number of butterfly operations
    #
    expected_coeffs = [0, 0, 0, 0]

    assert coeffs == expected_coeffs


# Test for an truth table with all elements set to one
#
def test_fmt_all_ones():
    ones_table = [1, 1, 1, 1]

    coeffs = fmt(ones_table)

    """
    Manual calculation:

        Step 1:
            anf[0] and anf[2] remain untouched
            anf[1] ^= anf[0] -> 1 ^ 1 = 0
            anf[3] ^= anf[2] -> 1 ^ 1 = 0
            Result: [1, 0, 1, 0]

        Step 2:
            anf[0] anf anf[1] remain untouched
            anf[2] ^= anf[0] -> anf[2] = 1 ^ 1 = 0
            anf[3] ^= anf[1] -> anf[3] = 0 ^ 0 = 0
            Result: [1, 0, 0, 0]

        The final result is [1, 0, 0, 0]
    """

    expected_coeffs = [1, 0, 0, 0]

    assert coeffs == expected_coeffs


# Test for an truth table whose length is not power of 2
#
def test_fmt_invalid_length_not_power_of_two():
    # The length of <invalid_truth_table> is 3
    # its not power of 2
    #
    invalid_truth_table = [1, 0, 1]

    """
    Manual check:

        n = 3
        Bitwise check: 3 & (3 - 1) = 3 & 2 = 2
        Since 2 != 0, it is not a power of 2  
    """

    with pytest.raises(ValueError):
        fmt(invalid_truth_table)


# Test for empty truth table
#
def test_fmt_empty_list():
    # The length of <invalid_truth_table> is 0
    #
    invalid_truth_table = []

    # The validation condition 'n == 0' is strictly met
    #
    with pytest.raises(ValueError):
        fmt(invalid_truth_table)
