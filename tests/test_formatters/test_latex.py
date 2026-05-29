from boolbox.formatters.latex import LaTeXFormatter


# Test for LaTeXFormatter class
#
def test_latex_formatter():
    formatter = LaTeXFormatter()

    sample_polys = {0: "x_0 XOR x_1", 1: "1 XOR x_2"}

    formatted = formatter.format(sample_polys)

    expected_output = "x_0 \\rightarrow S_0 = x_0 \\oplus x_1\nx_1 \\rightarrow S_1 = 1 \\oplus x_2"

    assert formatted == expected_output
