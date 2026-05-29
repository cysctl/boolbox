import pytest
import sys
from boolbox.io.loaders import load_sbox


# Test for parsing a pure decimal S-Box with brackets and spacing
#
def test_load_sbox_pure_decimal():
    sample_input = "[12, 5, 6, 11]"

    sbox = load_sbox(sample_input)

    """
    Manual trace for "[12, 5, 6, 11]":

        Brackets and commas are replaced by spaces -> " 12  5  6  11 "
        Split into tokens -> ["12", "5", "6", "11"]
        First item "12" does not start with "0x" -> Decimal mode
        All items are valid digits (isdigit() == True)
        
    So, the expected output is [12, 5, 6, 11]
    """

    expected_sbox = [12, 5, 6, 11]

    assert sbox == expected_sbox


# Test for parsing a pure hexadecimal S-Box with braces
#
def test_load_sbox_pure_hex():
    sample_input = "{0xC, 0x5, 0x6, 0xB}"

    sbox = load_sbox(sample_input)

    """
    Manual trace for "{0xC, 0x5, 0x6, 0xB}":

        Braces and commas are replaced by spaces -> " 0xC  0x5  0x6  0xB "
        Split into tokens -> ["0xC", "0x5", "0x6", "0xB"]
        First item "0xC" starts with "0x" -> Hexadecimal mode
        Parsed as base-16 integers: 12, 5, 6, 11
        
    So, the expected output is [12, 5, 6, 11]
    """

    expected_sbox = [12, 5, 6, 11]

    assert sbox == expected_sbox


# Test for the case where the input contains no valid items
#
def test_load_sbox_empty():
    sample_input = "[]"

    sbox = load_sbox(sample_input)

    """
    Empty input check:

    After cleaning the brackets, the string is empty
    The list of items remains empty

    The validation condition 'not sbox_items' is met, returning []
    """

    expected_sbox = []

    assert sbox == expected_sbox


# Test for a mixed format input (hex and decimal)
#
def test_load_sbox_mixed_format_raises_error():
    # The list contains "0xC" (hex) and "10" (decimal)
    #
    invalid_input = "[0xC, 10]"

    """
    Format constraint check:

        First item "0xC" triggers Hexadecimal mode
        Second item "10" does not start with "0x"
        
    The validation condition is violated.
    Expects ValueError with "Mixed formats are not allowed"
    """

    with pytest.raises(ValueError, match="Mixed formats are not allowed"):
        load_sbox(invalid_input)


# Test for an invalid data type in decimal mode
#
def test_load_sbox_invalid_data_type():
    # The list contains a non-digit character "A" in decimal mode
    #
    invalid_input = "12, A, 5"

    """
    Decimal mode strict check:

        First item "12" triggers Decimal mode
        Second item "A" is not a digit (isdigit() == False)
        
    The validation condition is violated.
    Expects ValueError starting with "Invalid data type"
    """

    with pytest.raises(ValueError, match="Invalid data type"):
        load_sbox(invalid_input)


# Test for an invalid hexadecimal value
#
def test_load_sbox_invalid_hex_value():
    # The list contains a non-hexadecimal character "0xG"
    #
    invalid_input = "0xC, 0xG"

    """
    Hexadecimal parse check:

        First item "0xC" triggers Hexadecimal mode
        Second item "0xG" fails int("0xG", 16)
        
    Python's int() throws ValueError, which is caught and re-raised
    """

    with pytest.raises(ValueError, match="Invalid hexadecimal value"):
        load_sbox(invalid_input)


# Test for reading the S-Box from a file
#
def test_load_sbox_from_file(tmp_path):
    # Create a temporary file using pytest's tmp_path fixture
    #
    test_file = tmp_path / "sbox.txt"
    test_file.write_text("0xC, 0x5\n0x6, 0xB")

    sbox = load_sbox(str(test_file))

    """
    File I/O check:

        os.path.isfile(_input) evaluates to True
        File contents are read -> "0xC, 0x5\n0x6, 0xB"
        Cleaned and parsed as Hexadecimal mode -> [12, 5, 6, 11]
    """

    expected_sbox = [12, 5, 6, 11]

    assert sbox == expected_sbox


# Test for reading the S-Box from standard input (UNIX I/O)
#
def test_load_sbox_from_stdin(monkeypatch):
    # Mock the sys.stdin.read() to simulate piped input
    # Example command: echo "12 5 6 11" | boolbox -
    #
    monkeypatch.setattr(sys.stdin, "read", lambda: "12 5 6 11")

    sbox = load_sbox("-")

    """
    UNIX I/O check:

        _input == "-" evaluates to True
        sys.stdin.read() provides "12 5 6 11"
        Parsed as Decimal mode -> [12, 5, 6, 11]
    """

    expected_sbox = [12, 5, 6, 11]

    assert sbox == expected_sbox
