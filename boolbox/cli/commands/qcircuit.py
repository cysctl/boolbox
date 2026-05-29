import os
import sys
import math
import argparse

from boolbox.io.loaders import load_sbox
from boolbox.quantum.utils import require_qiskit
from boolbox.quantum.builder import QuantumCircuitBuilder

from boolbox.pipeline import sbox_to_poly


def register_parser(subparsers):
    """
    Registers the 'qcircuit' command and its arguments to the main CLI parser

    Args:
        subparsers: The subparser object from argparse used to add new CLI commands
    """
    parser = subparsers.add_parser(
        "qcircuit",
        help="Synthesize a quantum circuit from an S-Box ANF.",
    )

    parser.add_argument(
        "input", help="S-Box input. Can be '-', a file path, or a raw string."
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "image"],
        default="text",
        help="Output format for the quantum circuit (text/ASCII or image).",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Path to the output file. Defaults to stdout for 'text' and 'quantum_circuit.png' for 'image'.",
    )

    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    """
    Executes the 'qcircuit' command logic
    Validates Qiskit dependency, loads the S-Box, parses it into ANF polynomials
    using the core pipeline, builds the QuantumCircuit, and prints the output

    Args:
        args: The parsed command-line arguments containing user inputs

    Returns:
        An integer representing the system exit status code (0 = success, 1 = error)
    """
    
    # Graceful check for the optional Qiskit dependency
    #
    try:
        require_qiskit()
    except Exception as e:
        print(f"Dependency Error: {e}", file=sys.stderr)
        return 1

    # Load the S-Box
    #
    try:
        sbox_ints = load_sbox(args.input)
    except Exception as e:
        print(f"Error loading S-Box: {e}", file=sys.stderr)
        return 1

    # Mathematical Pipeline
    #
    try:
        polys = sbox_to_poly(sbox_ints)
        input_size = int(math.log2(len(sbox_ints)))
    except Exception as e:
        print(f"Error generating ANF polynomials: {e}", file=sys.stderr)
        return 1

    # Synthesize the Quantum Circuit
    #
    try:
        builder = QuantumCircuitBuilder(input_size=input_size, polys=polys)
        qc = builder.build()
    except Exception as e:
        print(f"Error building Quantum Circuit: {e}", file=sys.stderr)
        return 1

    # Output
    #
    if args.format == "text":
        ascii_circuit = qc.draw(output="text")
        
        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(str(ascii_circuit) + "\n")
                
                abs_path = os.path.abspath(args.output)
                print(f"Success: ASCII circuit saved to file://{abs_path}")
                
            except Exception as e:
                print(f"Error writing to file: {e}", file=sys.stderr)
                return 1
        else:
            print(ascii_circuit)

    elif args.format == "image":
        from boolbox.quantum.utils import require_quantum_drawing
        
        # Validate image generation dependencies
        #
        require_quantum_drawing()
        
        # Determine output filename and resolve absolute path for terminal hyperlinking
        #
        out_path = args.output if args.output else "quantum_circuit.png"
        abs_path = os.path.abspath(out_path)
        
        try:
            qc.draw(output="mpl", filename=abs_path)
            print(f"Success: Quantum circuit image saved to file://{abs_path}")
            
        except Exception as e:
            print(f"Error rendering image: {e}", file=sys.stderr)
            return 1

    return 0