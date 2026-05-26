def parse_sbox(sbox: list[int], output_bits: int | None = None) -> list[int]:
    """
    Takes the S-Box table for the Möbius transform and
    generates independent truth tables for each output bit

    Args:
        sbox_table: A one-dimensional list containing S-Box output values
        output_bits: The number of bits produced by the S-Box output

    Return:
        A <output_bits>-dimensional list containing truth tables

    Raises:
        ValueError: If the length of the S-Box table is 0 or not a power of 2
    """

    n = len(sbox)

    if n == 0 or (n & (n - 1)) != 0:
        raise ValueError(f"Invalid S-Box size ({n}). It must be power of 2")

    #  Find the largest number in the S-Box and calculate the minimum number of bits required to represent that number
    #
    if output_bits is None:
        max_val = max(sbox)

        # If the S-Box consists entirely of 0s, a 1 is assigned by default
        #
        if max_val <= 0:
            output_bits = 1
        else:
            output_bits = max_val.bit_length()

    # All truth tables will be stored here
    #
    truth_tables = []

    for bit_pos in range(output_bits):
        curr_truth_table = []

        for val in sbox:
            # x_0s, x_1s, x_2s, ...
            #
            bit = (val >> bit_pos) & 0x1  # Masking to select just one bit

            curr_truth_table.append(bit)

        truth_tables.append(curr_truth_table)

    return truth_tables


if __name__ == "__main__":
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

    """
    After the calculation, output_bits is found to be 4, because:
    
        max_value in present_sbox = 0xF (base-16) = 1111 (base-2)
    
    So, the bit count (output_bits) is 4
    """

    present_truth_tables = parse_sbox(present_sbox)

    print(present_truth_tables)
