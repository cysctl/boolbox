import pytest
from boolbox.pipeline import sbox_to_poly


# General Test for PRESENT S-Box
#
def test_pipeline_present_sbox():
    # PRESENT S-Box
    #
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

    polys = sbox_to_poly(present_sbox)

    # We are inputting a 4-bit S-box
    # 4 equations must be generated
    # <output_bits>-dimensional
    #
    assert len(polys) == 4

    """
    WARNING

    It was observed that the ANF polynomial for S_0 was calculated correctly
    It was assumed that the remaining S_1, S_2, and S_3 polynomials were generated correctly
    """

    expected_s0 = "x_0 XOR x_2 XOR x_1 x_2 XOR x_3"

    assert polys[0] == expected_s0


# Test for invalid S-Box size
#
def test_pipeline_invalid_sbox_size():
    # The length of <invalid_sbox> is 3
    #
    invalid_sbox = [1, 2, 3]

    # According to the pipeline.py file, the parse_sbox function is executed first
    # Since the S-Box length is not a multiple of 2, the error "Invalid S-Box size..." is encountered
    #
    with pytest.raises(ValueError, match="Invalid S-Box size"):
        sbox_to_poly(invalid_sbox)
