import pytest
import argparse
import sys
import os
from unittest.mock import patch, MagicMock

from boolbox.cli.commands.qcircuit import run
from boolbox.quantum.utils import require_quantum_drawing


# Test for missing image generation dependencies
#
def test_require_quantum_drawing_missing(monkeypatch):
    """
    Test dependency check:
    
        Simulate an environment where 'matplotlib' is missing
        The function should catch ImportError and cleanly exit with code 1
    """

    # Simulate ImportError when importing matplotlib
    #
    monkeypatch.setitem(sys.modules, "matplotlib", None)
    
    with pytest.raises(SystemExit) as excinfo:
        require_quantum_drawing()
        
    assert excinfo.value.code == 1


# Test the default text output to stdout
#
@patch("boolbox.cli.commands.qcircuit.load_sbox")
@patch("boolbox.cli.commands.qcircuit.sbox_to_poly")
@patch("boolbox.cli.commands.qcircuit.QuantumCircuitBuilder")
def test_qcircuit_text_stdout(mock_builder_class, mock_sbox_to_poly, mock_load_sbox, capsys):
    """
    CLI routing check for stdout:
    
        Format is 'text', output path is None
        Should call qc.draw(output='text') and print to stdout
    """

    mock_load_sbox.return_value = [12, 5, 6, 11]
    mock_sbox_to_poly.return_value = {0: "x_0"}
    
    mock_qc = MagicMock()
    mock_qc.draw.return_value = "ASCII_CIRCUIT_DRAWING"
    mock_builder_class.return_value.build.return_value = mock_qc

    args = argparse.Namespace(input="mock_input", format="text", output=None)
    
    result = run(args)
    captured = capsys.readouterr()

    assert result == 0
    assert "ASCII_CIRCUIT_DRAWING" in captured.out


# Test routing the text output to a specific file
#
@patch("boolbox.cli.commands.qcircuit.load_sbox")
@patch("boolbox.cli.commands.qcircuit.sbox_to_poly")
@patch("boolbox.cli.commands.qcircuit.QuantumCircuitBuilder")
def test_qcircuit_text_file_output(mock_builder_class, mock_sbox_to_poly, mock_load_sbox, tmp_path):
    """
    Output Routing check (Text):
    
        Format is 'text', output path is provided
        Should write the ASCII circuit to the specified file
    """

    mock_load_sbox.return_value = [12, 5, 6, 11]
    mock_sbox_to_poly.return_value = {0: "x_0"}
    
    mock_qc = MagicMock()
    mock_qc.draw.return_value = "ASCII_CIRCUIT_DRAWING"
    mock_builder_class.return_value.build.return_value = mock_qc

    out_file = tmp_path / "circuit.txt"
    args = argparse.Namespace(input="mock_input", format="text", output=str(out_file))
    
    result = run(args)

    assert result == 0
    assert out_file.read_text(encoding="utf-8").strip() == "ASCII_CIRCUIT_DRAWING"


# Test routing the image output to a specific file
#
@patch("boolbox.quantum.utils.require_quantum_drawing")
@patch("boolbox.cli.commands.qcircuit.load_sbox")
@patch("boolbox.cli.commands.qcircuit.sbox_to_poly")
@patch("boolbox.cli.commands.qcircuit.QuantumCircuitBuilder")
def test_qcircuit_image_file_output(mock_builder_class, mock_sbox_to_poly, mock_load_sbox, mock_require_drawing, capsys):
    """
    Output Routing check (Image):
    
        Format is 'image', output path is provided
        Should call qc.draw(output='mpl', filename=abs_path)
    """

    mock_load_sbox.return_value = [12, 5, 6, 11]
    mock_sbox_to_poly.return_value = {0: "x_0"}

    mock_qc = MagicMock()
    mock_builder_class.return_value.build.return_value = mock_qc

    args = argparse.Namespace(input="mock_input", format="image", output="custom.png")

    result = run(args)
    captured = capsys.readouterr()
    
    # Calculate the expected absolute path dynamically
    #
    expected_abs_path = os.path.abspath("custom.png")

    assert result == 0
    assert f"Success: Quantum circuit image saved to file://{expected_abs_path}" in captured.out
    
    # The draw method should now receive the absolute path
    #
    mock_qc.draw.assert_called_once_with(output="mpl", filename=expected_abs_path)