from boolbox.formatters.unicode import UnicodeFormatter


# Test for UnicodeFormatter class
#
def test_unicode_formatter():
    formatter = UnicodeFormatter()

    sample_polys = {0: "x_0 XOR x_1", 1: "1 XOR x_2"}

    formatted = formatter.format(sample_polys)

    expected_output = "x₀ → S₀ = x₀ ⊕  x₁\nx₁ → S₁ = 1 ⊕  x₂"

    assert formatted == expected_output
