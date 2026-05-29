import argparse
from boolbox.cli.commands.anf import run


# Test for a successful ANF conversion using the default 'text' format
#
def test_anf_run_success_text(capsys):
    # Mocking the parsed arguments from argparse
    #
    args = argparse.Namespace(input="[0xC, 0xD, 0x1, 0xA]", format="text")

    exit_code = run(args)

    """
    Integration check:

        Input "[0xC, 0xD, 0x1, 0xA]" is correctly loaded as [12, 13, 1, 10]
        Processed by the pipeline without errors
        Output formatted as text and printed to stdout
        The command should return exit code 0 (success)
    """

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "S_0 =" in captured.out
    assert "x_0 XOR x_1" in captured.out


# Test for a successful ANF conversion using the 'json' format
#
def test_anf_run_success_json(capsys):
    args = argparse.Namespace(input="[0xC, 0xD, 0x1, 0xA]", format="json")

    exit_code = run(args)

    """
    Integration check:

        Output formatted as JSON
        Expected to find "metadata" and "equations" in standard output
    """

    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"type": "ANF Polynomials"' in captured.out
    assert '"bit_count": 4' in captured.out


# Test for failure during the S-Box loading phase
#
def test_anf_run_load_error(capsys):
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


# Test for failure during the mathematical pipeline phase
#
def test_anf_run_pipeline_error(capsys):
    # Valid syntax, but invalid length for an S-Box (length 3 is not a power of 2)
    #
    args = argparse.Namespace(input="[0xC, 0xD, 0x1]", format="text")

    exit_code = run(args)

    """
    Pipeline constraint check:

        Loader passes successfully (returns [12, 13, 1])
        Pipeline throws an error due to invalid input length
        The 'run' function catches this exception
        Prints the error to stderr
        Returns exit code 1
    """

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Error processing S-Box" in captured.err
