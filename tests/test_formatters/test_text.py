from boolbox.formatters.text import TextFormatter


# Test for TextFormatter class
#
def test_text_formatter():
    formatter = TextFormatter()

    sample_polys = {0: "x_0 XOR x_1", 1: "1 XOR x_2"}

    formatted = formatter.format(sample_polys)

    expected_output = "x_0 -> S_0 = x_0 XOR x_1\nx_1 -> S_1 = 1 XOR x_2"

    assert formatted == expected_output
