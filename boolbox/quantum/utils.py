import sys

def require_qiskit() -> None:
    """
    Checks if Qiskit is installed?
    Raises a clean SystemExit if not, guiding the user to install the optional dependency
    """

    try:
        import qiskit
    except ImportError:
        print("Error: The quantum module requires 'qiskit'.", file=sys.stderr)
        print("Please install it using the optional dependency flag:", file=sys.stderr)
        print("    pip install boolbox[quantum]", file=sys.stderr)
        print("Or manually:", file=sys.stderr)
        print("    pip install qiskit", file=sys.stderr)
        sys.exit(1)


def require_quantum_drawing() -> None:
    """
    Checks if matplotlib and pylatexenc are installed for rendering quantum circuits
    Raises a clean SystemExit if not
    """

    try:
        import matplotlib
        import pylatexenc
    except ImportError:
        print("Error: The 'image' format requires 'matplotlib' and 'pylatexenc'.", file=sys.stderr)
        print("Please install them using the optional dependency flag:", file=sys.stderr)
        print("    pip install boolbox[quantum-vis]", file=sys.stderr)
        print("Or manually:", file=sys.stderr)
        print("    pip install matplotlib pylatexenc", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    require_qiskit()