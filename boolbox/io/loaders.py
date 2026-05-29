import sys, os, re


def load_sbox(_input: str) -> list[int]:
    """
    Loads and parses an S-Box from various sources
    All items must be pure decimal or all must be 0x-prefixed hex
    Ignores brackets [], braces {}, parentheses (), and commas

    Args:
        _input: The value entered by user

    Returns:
        An S-Box object compatible with the pipeline

    Raises:
        ValueError: Boolbox returns an ValueError when it encounters mixed formats or a invalid data type
    """

    raw_text = ""

    if _input == "-":
        # UNIX IO
        # Example command: cat sbox.json | boolbox -
        #
        raw_text = sys.stdin.read()
    elif os.path.isfile(_input):
        # The user may want to read the sbox list from a file
        #
        with open(_input, "r") as file:
            raw_text = file.read()
    else:
        # Default
        #
        raw_text = _input

    # Remove the brackets and commas
    # Replace with whitespace
    #
    cleaned_text = re.sub(r"[\[\]{}()\n\r\t,]", " ", raw_text)

    # cleaned_text = "0xC 0xD 0x1 ...", type="str"
    # sbox_items = [0xC, 0xD, 0x1], type="list[int]"
    #
    sbox_items = cleaned_text.split()

    # Empty
    #
    if not sbox_items:
        return []

    # Specifying the format of items
    # Example, prefix: 0x => Hexadecimal
    # Mixed formats are not allowed
    #
    is_hex_mode = sbox_items[0].lower().startswith("0x")

    sbox = []
    for item in sbox_items:
        if is_hex_mode:
            if not item.lower().startswith("0x"):
                raise ValueError("Mixed formats are not allowed")

            try:
                sbox.append(int(item, 16))
            except ValueError:
                raise ValueError(f"Invalid hexadecimal value: {item}")

        else:
            if not item.isdigit():
                raise ValueError(f"Invalid data type: {item} -> {type(item)}")

            sbox.append(int(item, 10))

    return sbox
