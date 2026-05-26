import pytest
from boolbox.parser.sbox_parser import parse_sbox


# Test for PRESENT S-Box
#
def test_parse_sbox_present_auto():
    present_sbox = [
        0xC,
        0x5,
        0x6,
        0xB,
        0x9,
        0x0,
        0xA,
        0xD,
        0x3,
        0xE,
        0xF,
        0x8,
        0x4,
        0x7,
        0x1,
        0x2,
    ]

    present_truth_tables = parse_sbox(present_sbox)

    # Since the maximum value is 15 (0xF), it must be 4 bits
    # <output_bits>-dimensional
    #
    assert len(present_truth_tables) == 4

    """
    Manual calculation for present_truth_tables[0] (S_0):

        0xC -> 1100 -> S_0: 0
        0x5 -> 0101 -> S_0: 1
        0x6 -> 0110 -> S_0: 0
        0xB -> 1011 -> S_0: 1
        0x9 -> 1001 -> S_0: 1
        0x0 -> 0000 -> S_0: 0
        0xA -> 1010 -> S_0: 0
        0xD -> 1101 -> S_0: 1
        0x3 -> 0011 -> S_0: 1
        0xE -> 1110 -> S_0: 0
        0xF -> 1111 -> S_0: 1
        0x8 -> 1000 -> S_0: 0
        0x4 -> 0100 -> S_0: 0
        0x7 -> 0111 -> S_0: 1
        0x1 -> 0001 -> S_0: 1
        0x2 -> 0010 -> S_0: 0

    The expected array derived using this logic:
    """

    expected_value = [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0]

    assert present_truth_tables[0] == expected_value


# Testing the case where <output_bits> is set manually
#
def test_parse_sbox_explicit_output_bits():
    sample_sbox = [0x3, 0x0, 0x1, 0x2]

    # Deliberately requesting 3 output bits
    #
    truth_tables = parse_sbox(sample_sbox, output_bits=3)

    # <output_bits>-dimensional
    #
    assert len(truth_tables) == 3

    """
    Manual calculation for S_0, S_1, and S_2:

        0x3 -> 011 -> S_0: 1
        0x0 -> 000 -> S_0: 0
        0x1 -> 001 -> S_0: 1
        0x2 -> 010 -> S_0: 0
                 
                   -> S_1: 1
                   -> S_1: 0
                   -> S_1: 0
                   -> S_1: 1

                   -> S_2: 0
                   -> S_2: 0
                   -> S_2: 0
                   -> S_2: 0
    """

    expected_val_s0 = [1, 0, 1, 0]
    expected_val_s1 = [1, 0, 0, 1]
    expected_val_s2 = [0, 0, 0, 0]

    assert truth_tables[0] == expected_val_s0
    assert truth_tables[1] == expected_val_s1
    assert truth_tables[2] == expected_val_s2


# Test for an S-Box with all elements set to zero
#
def test_parse_sbox_all_zeros():
    zero_sbox = [0x0, 0x0, 0x0, 0x0]

    truth_tables = parse_sbox(zero_sbox)

    """
        max_val = 0

        Since 0 <= 0, the program defaults to output_bits = 1

        0x0 -> 0 -> S_0: 0 (applied to all 4 elements)

        So, the expected result is [0, 0, 0, 0]
    """

    # <output_bits>-dimensional
    #
    assert len(truth_tables) == 1

    expected_val = [0, 0, 0, 0]

    assert truth_tables[0] == expected_val


# Test for an S-Box whose length is not a power of 2
#
def test_parse_sbox_invalid_length_not_power_of_two():
    # The length of <invalid_sbox> is 3, which is not a power of 2
    #
    invalid_sbox = [0x1, 0x2, 0x3]

    """
    Manual control:

        n = 3 (length of sbox)
        Bitwise check: 3 & (3 - 1) = 3 & 2
        Binary check: 011 & 010 = 010 (2)
        Since 2 != 0, it is not a power of 2    

    So, the expected behavior derived using this logic is raising a ValueError
    """

    with pytest.raises(ValueError):
        parse_sbox(invalid_sbox)


# Test for empty S-Box
#
def test_parse_sbox_empty_list():
    # The length of <invalid_sbox> is 0
    #
    invalid_sbox = []

    # The validation condition 'n == 0' is strictly met
    #
    with pytest.raises(ValueError):
        parse_sbox(invalid_sbox)
