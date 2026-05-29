import argparse
from boolbox.cli.commands.tts import run


# Test for a successful Truth Table generation using the default 'text' format
#
def test_tts_run_success_text(capsys):
    # Mocking the parsed arguments from argparse
    # Input: [12, 13, 1, 10]
    #
    args = argparse.Namespace(input="[0xC, 0xD, 0x1, 0xA]", format="text")

    exit_code = run(args)

    """
    Integration check:

        Input "[0xC, 0xD, 0x1, 0xA]" is correctly loaded as [12, 13, 1, 10]
        Processed by the parser to extract Truth Tables
        Output formatted as text and printed to stdout
        The command should return exit code 0 (success)

        Manual trace for S_0 (LSB):
        12 (1100) -> LSB is 0
        13 (1101) -> LSB is 1
        1  (0001) -> LSB is 1
        10 (1010) -> LSB is 0
        Resulting S_0 array: [0, 1, 1, 0]
    """

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "S_0 = [0, 1, 1, 0]" in captured.out
    assert "S_1 =" in captured.out


# Test for a successful Truth Table generation using the 'json' format
#
def test_tts_run_success_json(capsys):
    args = argparse.Namespace(input="[0xC, 0xD, 0x1, 0xA]", format="json")

    exit_code = run(args)

    """
    Integration check:

        Output formatted as JSON
        Expected to find "metadata" and "Truth Tables" in standard output
    """

    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"type": "Truth Tables"' in captured.out
    assert '"bit_count": 4' in captured.out
    assert '"length": 4' in captured.out


# Test for failure during the S-Box loading phase
#
def test_tts_run_load_error(capsys):
    # Invalid mixed format to trigger the loader error
    #
    args = argparse.Namespace(input="[0xC, 10]", format="text")

    exit_code = run(args)

    """
    Error handling check:

        Loader throws a ValueError ("Mixed formats are not allowed")
        The 'run' function catches this exception
        Prints the error to standard error (stderr)
        Returns exit code 1
    """

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error loading S-Box" in captured.err


# Test for failure during the parsing phase
#
def test_tts_run_parser_error(capsys):
    # Valid syntax, but invalid length for an S-Box (length 3 is not a power of 2)
    # This assumes get_truth_tables validates the length/format of the S-Box
    #
    args = argparse.Namespace(input="[0xC, 0xD, 0x1]", format="text")

    exit_code = run(args)

    """
    Parser constraint check:

        Loader passes successfully (returns [12, 13, 1])
        Parser throws an error due to invalid input length
        The 'run' function catches this exception
        Prints the error to stderr
        Returns exit code 1
    """

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error generating truth tables" in captured.err
