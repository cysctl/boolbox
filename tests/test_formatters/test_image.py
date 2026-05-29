import os
import pytest
from unittest.mock import patch
from boolbox.formatters.image import ImageFormatter


# Test for the output path extension enforcement
#
def test_image_formatter_extension_check():
    # Without .png extension
    #
    formatter_no_ext = ImageFormatter(output_path="my_equations")
    assert formatter_no_ext.output_path == "my_equations.png"

    # With .png extension
    #
    formatter_with_ext = ImageFormatter(output_path="my_equations.png")
    assert formatter_with_ext.output_path == "my_equations.png"

    # With uppercase .PNG extension
    #
    formatter_upper_ext = ImageFormatter(output_path="my_equations.PNG")
    assert formatter_upper_ext.output_path == "my_equations.PNG"


# Test for the successful formatting and rendering process
#
@patch("boolbox.formatters.image.plt")
def test_image_formatter_format_success(mock_plt):
    # Mock 'plt' to avoid actual file generation during tests
    #
    formatter = ImageFormatter(output_path="test_output.png")

    sample_polys = {0: "x_0 XOR x_1", 1: "1 XOR x_2"}

    result = formatter.format(sample_polys)

    expected_path = os.path.abspath("test_output.png")
    expected_result = f"Image successfully saved to: file://{expected_path}"

    assert result == expected_result
    
    # Verify that the core matplotlib methods were actually called
    #
    mock_plt.figure.assert_called_once()
    mock_plt.savefig.assert_called_once()
    mock_plt.close.assert_called_once()


# Test for missing matplotlib dependency
#
def test_image_formatter_missing_dependency():
    # Temporarily set plt to None to simulate a missing library
    #
    with patch("boolbox.formatters.image.plt", None):
        formatter = ImageFormatter()
        
        """
        Dependency constraint check:
        
            plt is None
            Expects ImportError with the specific warning message
        """
        
        with pytest.raises(ImportError, match="The 'matplotlib' library is required"):
            formatter.format({0: "x_0 XOR x_1"})