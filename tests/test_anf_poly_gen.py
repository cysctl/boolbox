import pytest
from boolbox.generators.anf_poly_gen import generate_anf_poly


# Test for sample coefficients
#
def test_generate_anf_poly_basic():
    sample_coeffs = [1, 1, 0, 1]

    anf_poly = generate_anf_poly(sample_coeffs)

    # NOTE
    # The following explanation has been copied directly from the `boolbox/generators/anf_poly_gen.py` file

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

    expected_poly = "1 XOR x_0 XOR x_0 x_1"

    assert anf_poly == expected_poly


# Test for a larger and more complex coefficients list
#
def test_generate_anf_poly_complex():
    # 3-bit input space (8 elements)
    #
    complex_coeffs = [0, 1, 0, 0, 0, 1, 0, 1]

    anf_poly = generate_anf_poly(complex_coeffs)

    """
    Mathematical proof for [0, 1, 0, 0, 0, 1, 0, 1]:

        Index 1  ->  001  ->  coeff 1  ->  x_0
        Index 5  ->  101  ->  coeff 1  ->  x_0 x_2
        Index 7  ->  111  ->  coeff 1  ->  x_0 x_1 x_2

    The expected polynomial derived using this logic:
    """

    expected_poly = "x_0 XOR x_0 x_2 XOR x_0 x_1 x_2"

    assert anf_poly == expected_poly


# Test for the case where all coeffs are zero
#
def test_generate_anf_poly_all_zeros():
    zero_coeffs = [0, 0, 0, 0]

    anf_poly = generate_anf_poly(zero_coeffs)

    """
    All zeros

    No coefficient is 1

    The list of terms remains empty
    """

    expected_poly = ""

    assert anf_poly == expected_poly


# Test for an coeffs list whose length is not power of 2
#
def test_generate_anf_poly_invalid_length_not_power_of_two():
    # The length of <invalid_coeffs_list> is 3
    # its not power of 2
    #
    invalid_coeffs_list = [1, 0, 1]

    """
    Manual check:

        n = 3
        Bitwise check: 3 & (3 - 1) = 3 & 2 = 2
        Since 2 != 0, it is not a power of 2
    """

    with pytest.raises(ValueError):
        generate_anf_poly(invalid_coeffs_list)


# Test for empty coeffs list
#
def test_fmt_empty_list():
    # The length of <invalid_coeffs_list> is 0
    #
    invalid_coeffs_list = []

    # The validation condition 'n == 0' is strictly met
    #
    with pytest.raises(ValueError):
        generate_anf_poly(invalid_coeffs_list)
