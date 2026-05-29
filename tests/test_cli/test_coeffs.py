import argparse
from boolbox.cli.commands.coeffs import run


# Test for a successful Coefficients generation using the default 'text' format
#
def test_coeffs_run_success_text(capsys):
    args = argparse.Namespace(input="[0xC, 0xD, 0x1, 0xA]", format="text")

    exit_code = run(args)

    """
    Integration check:

        Input is correctly loaded as [12, 13, 1, 10]
        Processed by get_truth_tables
        Fast Mobius Transform (FMT) is applied to each table
        Output formatted as text and printed to stdout
        Expected to print lines starting with 'C_0 = [...]'
    """

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "C_0 =" in captured.out
    assert "C_1 =" in captured.out


# Test for a successful Coefficients generation using the 'json' format
#
def test_coeffs_run_success_json(capsys):
    args = argparse.Namespace(input="[0xC, 0xD, 0x1, 0xA]", format="json")

    exit_code = run(args)

    """
    Integration check:

        Output formatted as JSON
        Expected to find "metadata" and "Mobius Coefficients" in standard output
    """

    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"type": "Mobius Coefficients"' in captured.out
    assert '"bit_count": 4' in captured.out


# Test for failure during the processing phase
#
def test_coeffs_run_error(capsys):
    # Invalid length to trigger fmt or parser error
    args = argparse.Namespace(input="[0xC, 0xD, 0x1]", format="text")

    exit_code = run(args)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error generating Coefficients" in captured.err
