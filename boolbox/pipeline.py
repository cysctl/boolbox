from boolbox.parser.sbox_parser import parse_sbox
from boolbox.core.mobius_transform import fmt
from boolbox.generators.anf_poly_gen import generate_anf_poly

# Algebraic Normal Form is referred to as ANF


def sbox_to_poly(sbox: list[int]) -> dict[int, str]:
    """
    High-level pipeline that orchestrates the entire process from a raw S-Box
    to a set of ANF polynomials

    Args:
        sbox: A one-dimensional list of integers representing the S-Box

    Returns:
        A dictionary where keys are the output bit indices
        and values are the corresponding ANF polynomial strings
    """

    # Parse the S-Box into truth tables
    #
    truth_tables = parse_sbox(sbox)

    # The polynomials will be stored here
    #
    anf_poly_results = {}

    # Apply FMT and generate ANF string for each truth table
    #
    for idx, truth_table in enumerate(truth_tables):
        # Calculate ANF coeffs
        #
        anf_coeffs = fmt(truth_table)

        # Convert coeffs to a boolean poly
        #
        poly = generate_anf_poly(anf_coeffs)

        anf_poly_results[idx] = poly

    return anf_poly_results


if __name__ == "__main__":
    # PRESENT S-Box
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

    results = sbox_to_poly(present_sbox)

    print(results)
